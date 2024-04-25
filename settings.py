from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./icodes.db"
    OPENAI_API_KEY: str


settings = Settings()
