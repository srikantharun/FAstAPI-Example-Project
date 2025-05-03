from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy.orm import Session

from app.api.api import api_router
from app.core.config import get_settings
from app.db.init_db import init_db
from app.db.session import get_db

settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint with HTML response
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Root endpoint that returns an HTML page.
    
    Args:
        request: FastAPI request object
        
    Returns:
        HTML response with template
    """
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": settings.PROJECT_NAME}
    )

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    """
    Initialize database tables and seed data on application startup.
    """
    db = next(get_db())
    init_db(db)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)