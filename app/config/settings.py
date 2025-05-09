from pydantic_settings import BaseSettings, SettingsConfigDict


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

    model_config = SettingsConfigDict(env_file=".env.local")
