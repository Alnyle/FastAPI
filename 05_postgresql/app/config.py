from pydantic_settings import BaseSettings, SettingsConfigDict

# This file is responsible for loading your database configuration from environment variables

# BaseSettings is a special Pydantic class that automatically reads values from:
    # Environment variables
    # A .env file
    # SettingsConfigDict configures how BaseSettings behaves.


_base_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore" # ignore any extra environment variables that are not defined in this class
)

# This class represents your application's database configuration.
class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER:str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRS_DB: str

    REDIS_HOST: str
    REDIS_PORT: str

    # This tells Pydantic how to load the settings.
    model_config = _base_config
    # This creates a computed attribute.
    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRS_DB}"


class SecuritySettings(BaseSettings):

    JWT_SECRET: str
    JWT_ALGORITHM: str

    model_config = _base_config


db_settings = DatabaseSettings()
security_settings = SecuritySettings()