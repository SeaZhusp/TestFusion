from fastapi import FastAPI

from app.config import settings
from app.core.global_exc import register_exception


def register_routers(app: FastAPI) -> None:
    from app.api import auth, user
    app.include_router(auth.router, prefix=settings.prefix, tags=["认证"])
    app.include_router(user.router, prefix=settings.prefix, tags=["用户"])


def register_middleware(app: FastAPI) -> None:
    from app.core.middlewares import init_cors_middleware
    init_cors_middleware(app)


def create_app() -> FastAPI:
    app = FastAPI()

    # 注册中间件
    register_middleware(app)
    # 注册全局异常
    register_exception(app)
    # 注册路由
    register_routers(app)

    return app
