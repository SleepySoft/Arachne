from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import close_async_driver, init_db
from app.database_postgres import close_postgres_pool, init_postgres_tables
from app.routers import (
    admin,
    admin_checks,
    batches,
    business_batches,
    companies,
    company_exploration,
    company_material,
    computation_jobs,
    edges,
    explore,
    factual_graph,
    industries,
    nodes,
    prov,
    query,
    reasoning,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_postgres_tables()
    yield
    await close_async_driver()
    await close_postgres_pool()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)


@app.exception_handler(ConnectionResetError)
@app.exception_handler(BrokenPipeError)
async def connection_error_handler(_request: Request, exc: Exception):
    return JSONResponse(
        status_code=503,
        content={"detail": "Database connection was reset, please retry."},
    )

try:
    from neo4j.exceptions import ServiceUnavailable, SessionExpired

    @app.exception_handler(ServiceUnavailable)
    @app.exception_handler(SessionExpired)
    async def neo4j_unavailable_handler(_request: Request, exc: Exception):
        return JSONResponse(
            status_code=503,
            content={"detail": "Neo4j is temporarily unavailable, please retry."},
        )
except ImportError:
    pass

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nodes.router, prefix=f"{settings.API_V1_STR}/nodes", tags=["Nodes"])
app.include_router(prov.router, prefix=f"{settings.API_V1_STR}/prov", tags=["PROV"])
app.include_router(edges.router, prefix=f"{settings.API_V1_STR}/edges", tags=["Edges"])
app.include_router(industries.router, prefix=f"{settings.API_V1_STR}/industries", tags=["Industries"])
app.include_router(companies.router, prefix=f"{settings.API_V1_STR}/companies", tags=["Companies"])
app.include_router(company_material.router, prefix=f"{settings.API_V1_STR}/companies", tags=["Company Material Connections"])
app.include_router(company_exploration.router, prefix=f"{settings.API_V1_STR}/companies", tags=["Company Exploration"])
app.include_router(computation_jobs.router, prefix=f"{settings.API_V1_STR}/computation-jobs", tags=["Computation Jobs"])
app.include_router(batches.router, prefix=f"{settings.API_V1_STR}/batches", tags=["Batches"])
app.include_router(business_batches.router, prefix=f"{settings.API_V1_STR}/business-batches", tags=["Business Batches"])
app.include_router(factual_graph.router, prefix=f"{settings.API_V1_STR}/factual-graph", tags=["Factual Graph"])
app.include_router(explore.router, prefix=f"{settings.API_V1_STR}/explore", tags=["Explore"])
app.include_router(query.router, prefix=f"{settings.API_V1_STR}/query", tags=["Query"])
app.include_router(reasoning.router, prefix=f"{settings.API_V1_STR}/reasoning", tags=["Reasoning"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])
app.include_router(admin_checks.router, prefix=f"{settings.API_V1_STR}/admin/db-checks", tags=["Admin"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}
