from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


def init_cors_middleware(app: FastAPI):
    """初始化 CORS（跨域资源共享）中间件"""
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=settings.cors_allow_origins,
        allow_headers=['*'],
        allow_methods=['OPTIONS', 'GET', 'POST', 'DELETE', 'PUT'],
        max_age=3600
    )
