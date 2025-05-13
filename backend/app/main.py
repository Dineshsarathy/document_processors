# from fastapi import FastAPI, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from app.routes import auth, documents
# from app.core.database import get_database
# from app.core.config import settings

# app = FastAPI(title=settings.app_name)

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include routers
# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(documents.router, prefix="/documents", tags=["documents"])

# @app.on_event("startup")
# async def startup_db_client():
#     # Test the database connection
#     db = get_database()
#     try:
#         await db.command("ping")
#         print("Connected to MongoDB")
#     except Exception as e:
#         print(f"Error connecting to MongoDB: {e}")

# @app.get("/")
# async def root():
#     return {"message": "Document Processor API"}


import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.routes import router as api_router
from app.core.database import get_database
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="Document Processing API with OCR and data extraction",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include API routes
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection"""
    db = get_database()
    try:
        await db.command("ping")
        logger.info("Successfully connected to MongoDB")
        
        # Create indexes
        await db.users.create_index("username", unique=True)
        await db.documents.create_index("owner_id")
        logger.info("Created database indexes")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection"""
    logger.info("Shutting down database connections")
    # Motor handles connection pooling, so no explicit close needed

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": settings.app_name}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    db = get_database()
    try:
        await db.command("ping")
        return {
            "status": "ok",
            "database": "connected",
            "service": settings.app_name
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        }, 503