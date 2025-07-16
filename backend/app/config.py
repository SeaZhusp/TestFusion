from pydantic_settings import BaseSettings
from pydantic import Field, AnyUrl


class Settings(BaseSettings):
    # 项目基本配置
    project_name: str = "TestPlatform"
    prefix: str = "/api"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # CORS 跨域资源共享
    cors_allow_origins: str = '["*"]'

    # MySQL 数据库连接，推荐用下面格式
    database_url: str
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_token_expire_minutes: int = 60 * 24

    # OpenAI 配置
    openai_api_key: str | None = None

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
