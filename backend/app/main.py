from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import close_async_driver, init_db
from app.database_postgres import close_postgres_pool, init_postgres_tables
from app.routers import batches, business_batches, companies, company_exploration, company_material, company_view, computation_jobs, edges, industries, nodes, query

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nodes.router, prefix=f"{settings.API_V1_STR}/nodes", tags=["Nodes"])
app.include_router(edges.router, prefix=f"{settings.API_V1_STR}/edges", tags=["Edges"])
app.include_router(industries.router, prefix=f"{settings.API_V1_STR}/industries", tags=["Industries"])
app.include_router(company_view.router, prefix=f"{settings.API_V1_STR}/company-view", tags=["Company View"])
app.include_router(companies.router, prefix=f"{settings.API_V1_STR}/companies", tags=["Companies"])
app.include_router(company_material.router, prefix=f"{settings.API_V1_STR}/companies", tags=["Company Material Connections"])
app.include_router(company_exploration.router, prefix=f"{settings.API_V1_STR}/companies", tags=["Company Exploration"])
app.include_router(computation_jobs.router, prefix=f"{settings.API_V1_STR}/computation-jobs", tags=["Computation Jobs"])
app.include_router(batches.router, prefix=f"{settings.API_V1_STR}/batches", tags=["Batches"])
app.include_router(business_batches.router, prefix=f"{settings.API_V1_STR}/business-batches", tags=["Business Batches"])
app.include_router(query.router, prefix=f"{settings.API_V1_STR}/query", tags=["Query"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}
