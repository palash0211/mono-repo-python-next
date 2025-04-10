from typing import Generic, Optional, TypeVar, Any, Dict, List
from pydantic import BaseModel

T = TypeVar('T')

class APIResponse(BaseModel):
    """Standard API response model."""
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[Dict[str, Any]]] = None

class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response model."""
    success: bool
    message: str
    data: List[T]
    page: int
    page_size: int
    total: int
    total_pages: int
    errors: Optional[List[Dict[str, Any]]] = None
