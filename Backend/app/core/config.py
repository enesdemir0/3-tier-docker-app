from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Handles Environment Variables for the whole app."""
    PROJECT_NAME: str = "Enterprise Agentic RAG"
    API_V1_STR: str = "/api/v1"
    
    # These will be automatically pulled from your .env file
    GROQ_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str
    TAVILY_API_KEY: str

    class Config:
        # This tells Pydantic where to find the .env file
        env_file = ".env"

settings = Settings()