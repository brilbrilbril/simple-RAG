from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str

    EMBEDDING_MODEL: str

    QDRANT_COLLECTION_NAME: str

    CHAT_MODEL: str

    API_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
