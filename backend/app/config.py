from pydantic_settings import BaseSettings
from pydantic import Field, AnyUrl


class Settings(BaseSettings):
    # 项目基本配置
    project_name: str = "TestPlatform"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # MySQL 数据库连接，推荐用下面格式
    database_url: AnyUrl  # 对应环境变量 DATABASE_URL
    jwt_secret_key: str  # 对应环境变量 JWT_SECRET_KEY
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60 * 24

    # OpenAI 配置
    openai_api_key: str | None = None  # 对应环境变量 OPENAI_API_KEY

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings(_env_file='../.env')
