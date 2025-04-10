from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import models
from app.api import deps
from app.services import user_service
from app.schemas.user import User, UserCreate
from app.schemas.response import APIResponse
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter()

@router.get("/", response_model=APIResponse)
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = user_service.get_multi(db, skip=skip, limit=limit)
    return APIResponse(success=True, message="Users retrieved successfully", data=users)

@router.post("/", response_model=APIResponse)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = user_service.get_by_email(db, email=user_in.email)
    if user:
        raise BadRequestException(message="The user with this email already exists in the system.")
    user = user_service.create(db, obj_in=user_in)
    return APIResponse(success=True, message="User created successfully", data=user)

@router.get("/me", response_model=APIResponse)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return APIResponse(success=True, message="Current user retrieved", data=current_user)

@router.get("/{user_id}", response_model=APIResponse)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = user_service.get(db, id=user_id)
    if not user:
        raise NotFoundException(message="User not found")
    if user.id != current_user.id and not current_user.is_superuser:
        raise BadRequestException(message="Not enough permissions")
    return APIResponse(success=True, message="User retrieved successfully", data=user)

