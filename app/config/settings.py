import os

from pydantic_settings import BaseSettings, SettingsConfigDict

APP_ENV = os.getenv("APP_ENV", "local")
ENV_FILE = f".env.{APP_ENV}"


class Settings(BaseSettings):
    APP_ENV: str
    SECRET_KEY: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    SWAGGER_NAME: str
    SWAGGER_PASSWORD: str
    CORS_ORIGINS: str

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")


settings = Settings()
print("Settings loaded:", settings)
