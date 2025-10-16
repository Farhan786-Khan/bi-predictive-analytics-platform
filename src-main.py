"""
Main application entry point for the Business Intelligence Platform.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from src.api.dependencies import get_settings
from src.api.routes import predictions, anomaly, prescriptive, dashboard
from src.core.config import get_settings as core_get_settings
from src.core.database import create_tables, close_db_connection
from src.core.logging import setup_logging
from src.utils.exceptions import BusinessIntelligenceException


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    setup_logging()
    await create_tables()
    
    yield
    
    # Shutdown
    await close_db_connection()


# Create FastAPI application
app = FastAPI(
    title="Business Intelligence Platform API",
    description="End-to-End Business Intelligence Dashboard with Predictive & Prescriptive Analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Get settings
settings = core_get_settings()

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts
)


# Exception handlers
@app.exception_handler(BusinessIntelligenceException)
async def business_intelligence_exception_handler(
    request: Request, 
    exc: BusinessIntelligenceException
) -> JSONResponse:
    """Handle custom business intelligence exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "details": str(exc) if settings.debug else None
        }
    )


# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Business Intelligence Platform API",
        "version": "1.0.0"
    }


@app.get("/health/detailed", tags=["Health"])
async def detailed_health_check():
    """Detailed health check with component status."""
    from src.core.database import check_database_connection
    from src.integrations.slack_bot import check_slack_connection
    
    checks = {
        "database": await check_database_connection(),
        "slack": await check_slack_connection(),
        "redis": True,  # TODO: Implement Redis health check
    }
    
    overall_status = "healthy" if all(checks.values()) else "unhealthy"
    
    return {
        "status": overall_status,
        "service": "Business Intelligence Platform API",
        "version": "1.0.0",
        "checks": checks
    }


# Metrics endpoint for Prometheus
@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Include API routers
app.include_router(
    predictions.router,
    prefix="/api/v1/predict",
    tags=["Predictions"]
)

app.include_router(
    anomaly.router,
    prefix="/api/v1/anomaly",
    tags=["Anomaly Detection"]
)

app.include_router(
    prescriptive.router,
    prefix="/api/v1/prescribe",
    tags=["Prescriptive Analytics"]
)

app.include_router(
    dashboard.router,
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the Business Intelligence Platform API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }


if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"],
        log_level="info"
    )