from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from core.config import settings
from core.logging import get_logger
from models.database import create_tables
from routers import summarize, articles, feedback, feeds, news

# Set up logging
logger = get_logger(__name__)

# CORS middleware and routers will be added after app creation

# Create database tables on startup
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Technonews API...")
    logger.info(f"CORS origins: {settings.cors_origins_list}")
    create_tables()
    logger.info("Technonews API started successfully")
    yield
    # Shutdown
    logger.info("Shutting down Technonews API...")

# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="AI-powered news summarization and categorization API",
    lifespan=lifespan
)

# CORS middleware for React front-end integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Include routers
app.include_router(summarize.router)
app.include_router(articles.router)
app.include_router(feedback.router)
app.include_router(feeds.router)
app.include_router(news.router)

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    """Redirect to the frontend."""
    return RedirectResponse(url="/static/index.html")

@app.get("/api/")
def api_status():
    """API status endpoint."""
    return {
        "message": "Technonews API is running",
        "version": settings.api_version,
        "endpoints": {
            "summarize": "/summarize",
            "store": "/store", 
            "articles": "/articles",
            "feedback": "/feedback",
            "feeds": "/feeds",
            "news": "/news/{theme}"
        }
    }

@app.get("/health")
def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "api": settings.api_title,
        "version": settings.api_version
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Running in development mode")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 