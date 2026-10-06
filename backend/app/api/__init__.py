from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.resumes import router as resumes_router
from app.api.jobs import router as jobs_router
from app.api.analysis import router as analysis_router
from app.api.dashboard import router as dashboard_router
from app.api.profile import router as profile_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(resumes_router)
api_router.include_router(jobs_router)
api_router.include_router(analysis_router)
api_router.include_router(dashboard_router)
api_router.include_router(profile_router)
