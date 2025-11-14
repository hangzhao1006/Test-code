"""
SkinCare AI Assistant - FastAPI Backend
主应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import routers
from api.routes import analysis, chat, products, search, image_analysis, weather

# Create FastAPI app
app = FastAPI(
    title="SkinCare AI Assistant API",
    description="AI-powered skincare analysis and product recommendation system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",  # Frontend dev server
        "http://localhost:3000",
        os.getenv("FRONTEND_URL", "*")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(search.router, prefix="/api", tags=["Search"])
app.include_router(image_analysis.router, prefix="/api", tags=["Image Analysis"])
app.include_router(weather.router, prefix="/api", tags=["Weather"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "skincare-ai-backend",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "SkinCare AI Assistant API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
