from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Reads values from environment variables and the .env file (like Laravel's config + .env)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "TaskSense"
    database_url: str = "sqlite:///./tasks.db"


settings = Settings()
