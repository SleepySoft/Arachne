import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "arachne123")

    # Optional separate Neo4j instance for arachne-flow engine.
    # If not configured, the flow engine shares the main Neo4j instance
    # but uses distinct relationship types/labels (:ARACHNE_FLOW, etc.).
    NEO4J_FLOW_URI: str = os.getenv("NEO4J_FLOW_URI", NEO4J_URI)
    NEO4J_FLOW_USER: str = os.getenv("NEO4J_FLOW_USER", NEO4J_USER)
    NEO4J_FLOW_PASSWORD: str = os.getenv("NEO4J_FLOW_PASSWORD", NEO4J_PASSWORD)

    POSTGRES_URL: str = os.getenv(
        "POSTGRES_URL",
        "postgresql://postgres:postgres@localhost:5433/arachne"
    )

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Arachne Industrial Ontology Graph"

    # Permission framework: "disabled" (standalone, all allowed),
    # "header" (read scope from integrating system via HTTP header),
    # "custom" (reserved for future token-based integration).
    AUTH_MODE: str = os.getenv("AUTH_MODE", "disabled")
    AUTH_SCOPE_HEADER: str = os.getenv("AUTH_SCOPE_HEADER", "X-Arachne-Scope")

    # JWT verification (used when AUTH_MODE="jwt").
    # Arachne is the resource server; the integrating system signs tokens.
    JWT_ISSUER: str = os.getenv("JWT_ISSUER", "")
    JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "arachne")
    JWT_JWKS_URL: str = os.getenv("JWT_JWKS_URL", "")
    JWT_JWKS_REFRESH_SECONDS: int = int(os.getenv("JWT_JWKS_REFRESH_SECONDS", "3600"))



    class Config:
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
