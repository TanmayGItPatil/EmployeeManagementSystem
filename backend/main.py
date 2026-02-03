"""
Main FastAPI application for Employee Management System
"""
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.db.database import initialize_database, DatabaseConnection
from app.routes.employees import router as employee_router

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    print("Starting Employee Management System API...")
    
    # Initialize database
    if initialize_database():
        print("Database initialized successfully")
    else:
        print("Warning: Database initialization failed")
    
    yield
    
    # Shutdown
    print("Shutting down Employee Management System API...")
    db = DatabaseConnection()
    db.close_connection()


# Create FastAPI app
app = FastAPI(
    title="Employee Management System API",
    description="A comprehensive API for managing employee records with CRUD operations",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(employee_router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Employee Management System API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/api/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    try:
        from app.db.database import get_db_connection
        connection = get_db_connection()
        if connection.is_connected():
            return {
                "status": "healthy",
                "database": "connected"
            }
        else:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "status": "unhealthy",
                    "database": "disconnected"
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )