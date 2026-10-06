"""
AI Resume Analyzer — FastAPI Application Entry Point
Initializes the FastAPI application, configures CORS middleware,
ensures database schema creation on startup, and attaches all API routers.
"""

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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

frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
frontend_index = frontend_dist / "index.html"
assets_dir = frontend_dist / "assets"

if assets_dir.is_dir():
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


@app.get("/", tags=["Health"])
def root():
    """Serve the frontend when built, otherwise return the API health summary."""
    if frontend_index.is_file():
        return FileResponse(frontend_index)
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


@app.get("/{path:path}", include_in_schema=False)
def frontend_routes(path: str):
    """Serve the single-page app on client-side routes in production."""
    if path == "api" or path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not Found")
    if frontend_index.is_file():
        return FileResponse(frontend_index)
    raise HTTPException(status_code=404, detail="Not Found")
