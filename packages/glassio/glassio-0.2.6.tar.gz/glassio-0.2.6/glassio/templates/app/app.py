import os.path

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

app = FastAPI()
app.add_middleware(SessionMiddleware)
app.include_router(account_ctrl)
