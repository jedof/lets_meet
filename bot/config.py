from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TG_TOKEN: SecretStr
    DB_URL: SecretStr


settings = Settings()