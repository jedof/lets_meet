from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TG_TOKEN: SecretStr
    DB_URL: SecretStr
    photo_path: str = "bot/images"


settings = Settings()