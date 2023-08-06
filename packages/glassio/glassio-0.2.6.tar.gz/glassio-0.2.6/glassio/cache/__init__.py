from typing import TypeVar
from .abc import AbstractCache
from .no_cache import NoCache
from .simple import SimpleCache

CacheType = TypeVar("CacheType", bound=AbstractCache)
