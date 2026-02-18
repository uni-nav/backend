

# app/main.py
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api import floors, waypoints, navigation, rooms, kiosks, auth
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.database import get_db

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load resources
    logger.info("Starting University Navigation API...")
    instrumentator.expose(app)
    yield
    # Shutdown: clean up resources (if any)
    logger.info("Shutting down University Navigation API...")

app = FastAPI(
    title="University Navigation API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

CORS_ALLOW_METHODS = "GET,POST,PUT,PATCH,DELETE,OPTIONS,HEAD"
CORS_ALLOW_HEADERS = "Authorization,Content-Type,Accept,Origin,User-Agent,DNT,Cache-Control,X-Requested-With,If-Modified-Since"


@app.middleware("http")
async def permissive_cors_middleware(request: Request, call_next):
    """
    Fully permissive CORS for multi-client environment (web/mobile/kiosk).
    Always returns CORS headers and answers preflight locally.
    """
    if request.method == "OPTIONS":
        response = Response(status_code=200)
    else:
        response = await call_next(request)

    origin = request.headers.get("origin")
    if origin:
        # Reflect any requesting origin.
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
    else:
        response.headers["Access-Control-Allow-Origin"] = "*"

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = CORS_ALLOW_METHODS
    response.headers["Access-Control-Allow-Headers"] = request.headers.get(
        "Access-Control-Request-Headers", CORS_ALLOW_HEADERS
    )
    response.headers["Access-Control-Max-Age"] = "86400"
    return response

# Uploads papkani yaratish
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/api/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# API routes
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(floors.router, prefix="/api/floors", tags=["floors"])
app.include_router(waypoints.router, prefix="/api/waypoints", tags=["waypoints"])
app.include_router(navigation.router, prefix="/api/navigation", tags=["navigation"])
app.include_router(rooms.router, prefix="/api/rooms", tags=["rooms"])
app.include_router(kiosks.router, prefix="/api/kiosks", tags=["kiosks"])

@app.get("/api")
def root():
    return {"message": "University Navigation API", "version": "1.0.0"}

# Prometheus Metrics
instrumentator = Instrumentator().instrument(app)


@app.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint that verifies database connectivity
    """
    try:
        # Simple query to check DB connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "detail": str(e)
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
