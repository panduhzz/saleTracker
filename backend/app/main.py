"""
FastAPI main application for Sale Tracker API.
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from app.api import sales, dashboard
from app.auth.swa_auth import get_current_user

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Sale Tracker API",
    description="Backend API for sales tracking application with Azure Cosmos DB",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
allowed_origins_env = os.getenv("ALLOWED_ORIGINS")
allow_origins = (
    [origin.strip() for origin in allowed_origins_env.split(",")]
    if allowed_origins_env else ["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(sales.router)
app.include_router(dashboard.router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Sale Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "sale-tracker-api"}


@app.get("/api/user")
async def get_user_info(user: dict = Depends(get_current_user)):
    """Get current user information."""
    return {
        "userId": user["userId"],
        "userDetails": user["userDetails"],
        "provider": user["provider"]
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status_code": 500}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
