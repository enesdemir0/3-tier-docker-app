from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise Agentic RAG"
    API_V1_STR: str = "/api/v1"
    
    GROQ_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str
    TAVILY_API_KEY: str

    # Modern way to handle env files in Pydantic V2
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()