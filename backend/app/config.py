import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "arachne123")

    POSTGRES_URL: str = os.getenv(
        "POSTGRES_URL",
        "postgresql://postgres:postgres@localhost:5432/arachne"
    )

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Arachne Industrial Ontology Graph"

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
