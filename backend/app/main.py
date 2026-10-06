"""
AI Resume Analyzer — FastAPI Application Entry Point
Initializes the FastAPI application, configures CORS middleware,
ensures database schema creation on startup, and attaches all API routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import Base, engine
# Import all models so SQLAlchemy metadata registers all tables
import app.models
from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager that handles startup and shutdown events.
    Creates all database tables automatically if they do not yet exist.
    """
    # Startup: Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown logic (if needed)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Production-grade RESTful API for AI-assisted resume screening and job description analysis. "
        "Provides transparent multi-metric matching, skill gap detection, and actionable suggestions."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach API routers
app.include_router(api_router)


@app.get("/", tags=["Health"])
def root():
    """Root health check returning service name and status."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "healthy",
        "documentation": "/docs"
    }


@app.get("/health", tags=["Health"])
def health():
    """Health check endpoint for container orchestrators and monitoring probes."""
    return {"status": "ok"}
