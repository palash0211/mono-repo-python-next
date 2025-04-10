from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

class AppException(Exception):
    """Base exception for application errors."""
    def __init__(self, status_code: int, message: str, errors: list = None):
        self.status_code = status_code
        self.message = message
        self.errors = errors or []
        super().__init__(message)

class NotFoundException(AppException):
    """Resource not found exception."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(status_code=404, message=message)

class UnauthorizedException(AppException):
    """Unauthorized access exception."""
    def __init__(self, message: str = "Authentication required"):
        super().__init__(status_code=401, message=message)

class ForbiddenException(AppException):
    """Forbidden access exception."""
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(status_code=403, message=message)

class BadRequestException(AppException):
    """Bad request exception."""
    def __init__(self, message: str = "Bad request", errors: list = None):
        super().__init__(status_code=400, message=message, errors=errors)

async def app_exception_handler(request: Request, exc: AppException):
    """Handler for application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "errors": exc.errors,
            "data": None,
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for request validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "errors": jsonable_encoder(exc.errors()),
            "data": None,
        },
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    """Handler for unhandled exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error",
            "errors": [],
            "data": None,
        },
    )
