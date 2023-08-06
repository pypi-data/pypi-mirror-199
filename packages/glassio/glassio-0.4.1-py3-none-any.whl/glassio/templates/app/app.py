import os.path
import importlib
from fastapi import FastAPI
from glassio.config import BaseConfig
from glassio import ctx
from .controllers.api.v1.account import account_ctrl
from .middleware import SessionMiddleware


# You can add your app-specific configuration bits here
class Config(BaseConfig):
    pass


app_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.abspath(os.path.join(app_dir, ".."))
ctx.setup(project_dir, Config)

ctx.log.info("context configured")

# import tasks
tasks_dir = os.path.join(app_dir, "tasks")
for filename in os.listdir(tasks_dir):
    if filename.endswith(".py"):
        module_name = filename[:-3]
        _ = importlib.import_module(f"app.tasks.{module_name}")

app = FastAPI()
app.add_middleware(SessionMiddleware)
app.include_router(account_ctrl)
