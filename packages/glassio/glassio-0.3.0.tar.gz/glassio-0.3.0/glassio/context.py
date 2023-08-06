import logging
import logging.handlers
import os
import sys
from logging import Logger, getLogger
from typing import Generic, TypeVar, Type
from .types import EnvironmentType
from .config import BaseConfig
from .taskq.types import TBaseQueue

_LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

C = TypeVar("C", bound=BaseConfig)
CT = Type[C]


# To avoid initialization issues Context must be fully synchronous
# i.e. no properties requiring async initialization are allowed.
# Thus, db moved out. It's not going to be needed anywhere besides
# StorableModel anyway.
class Context(Generic[C]):
    _env: EnvironmentType
    _cfg: C
    _log: Logger
    _queue: TBaseQueue

    _project_dir: str
    _initialized = False

    @property
    def project_dir(self):
        return self._project_dir

    @property
    def env(self) -> EnvironmentType:
        if not self._initialized:
            raise RuntimeError("attempted to use uninitialized context")
        return self._env

    @property
    def cfg(self) -> C:
        if not self._initialized:
            raise RuntimeError("attempted to use uninitialized context")
        return self._cfg

    @property
    def log(self) -> Logger:
        if not self._initialized:
            raise RuntimeError("attempted to use uninitialized context")
        return self._log

    @property
    def queue(self) -> TBaseQueue:
        if not self._initialized:
            raise RuntimeError("attempted to use uninitialized context")
        return self._queue

    def setup(self, project_dir: str, cfgcls: CT) -> None:
        self._project_dir = project_dir
        self._setup_env()
        self._setup_config(cfgcls)
        self._setup_logging()
        self._setup_queue()
        self._initialized = True

    def _setup_queue(self):
        if self._cfg.queue.type == "mongo":
            from .taskq.mongo_queue import MongoQueue
            self._queue = MongoQueue(self._cfg.mongo_queue)
        else:
            raise TypeError(f"queue type {self._cfg.queue.type} is invalid")

    def _setup_config(self, cfgcls: CT) -> None:
        config_filename = os.path.join(self._project_dir, f"{self._env}.toml")
        self._cfg = cfgcls.parse(config_filename)

    def _setup_env(self):
        env: EnvironmentType = "development"
        ext_env = os.getenv("GLASS_ENV")

        if ext_env in ["development", "testing", "staging", "production"]:
            env = ext_env
        self._env = env

    def _setup_logging(self):
        logger = getLogger(__name__)
        logger.propagate = False

        lvl = _LOG_LEVELS.get(
            self._cfg.logging.level.lower(),
            logging.DEBUG
        )
        logger.setLevel(lvl)

        for handler in logger.handlers:
            logger.removeHandler(handler)

        log_format = logging.Formatter(
            "[%(asctime)s] %(levelname)s %(filename)s:%(lineno)d %(message)s"
        )

        if self._cfg.logging.stdout:
            handler = logging.StreamHandler(stream=sys.stdout)
            handler.setLevel(lvl)
            handler.setFormatter(log_format)
            logger.addHandler(handler)

        if self._cfg.logging.filename is not None:
            handler = logging.handlers.WatchedFileHandler(self.cfg.logging.filename)
            handler.setLevel(lvl)
            handler.setFormatter(log_format)
            logger.addHandler(handler)

        self._log = logger


ctx = Context()
