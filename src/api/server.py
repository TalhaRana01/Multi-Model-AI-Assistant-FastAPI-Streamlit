"""
FastAPI application setup
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, chat, health
from .database.db import create_tables
from ..config import settings
from ..utils.logger import logger

# Create FastAPI app
app = FastAPI(
    title="AI Assistant API",
    description="Multi-LLM AI Assistant with Authentication",
    version="1.0.0",
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(chat.router)


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("Starting AI Assistant API...")
    create_tables()
    logger.info("Database tables created/verified")
    logger.info(f"API running on http://{settings.api_host}:{settings.api_port}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down AI Assistant API...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Assistant API",
        "version": "1.0.0",
        "docs": "/docs"
    }