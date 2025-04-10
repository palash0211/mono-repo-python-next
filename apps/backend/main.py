from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app import app as application
from app.db.base import Base
from database import engine
from app.core.exceptions import (
    AppException, 
    app_exception_handler, 
    validation_exception_handler,
    unhandled_exception_handler
)
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.security_middleware import SecurityHeadersMiddleware

__all__ = ["Base"]

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure exception handlers
application.add_exception_handler(AppException, app_exception_handler)
application.add_exception_handler(RequestValidationError, validation_exception_handler)
application.add_exception_handler(Exception, unhandled_exception_handler)

# Add middleware
application.add_middleware(LoggingMiddleware)
application.add_middleware(SecurityHeadersMiddleware)

# Re-export the FastAPI app
app = application

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

