from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.schemas.response import APIResponse
from app.models.user import User
from app.api import deps
from app.services import item_service
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter()

@router.get("/", response_model=List[Item])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    if current_user.is_superuser:
        items = item_service.get_multi(db, skip=skip, limit=limit)
    else:
        items = item_service.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return items

@router.post("/", response_model=Item)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: ItemCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = item_service.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return item

@router.get("/{id}", response_model=Item)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = item_service.get(db=db, id=id)
    if not item:
        raise NotFoundException(message="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise BadRequestException(message="Not enough permissions")
    return item

@router.get("/public", response_model=APIResponse)
def get_items_public(db: Session = Depends(deps.get_db)):
    """
    Get all public items without authentication
    """
    items = item_service.get_multi(db)
    return APIResponse(success=True, message="Items retrieved successfully", data=items)

@router.get("/public/{item_id}", response_model=APIResponse)
def get_item_public(item_id: int, db: Session = Depends(deps.get_db)):
    """
    Get a public item by ID without authentication
    """
    item = item_service.get(db=db, id=item_id)
    if not item:
        raise NotFoundException(message="Item not found")
    return APIResponse(success=True, message="Item retrieved successfully", data=item)

@router.put("/{id}", response_model=Item)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: ItemUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    item = item_service.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = item_service.update(db=db, db_obj=item, obj_in=item_in)
    return item

@router.delete("/{id}", response_model= Item)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = item_service.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = item_service.remove(db=db, id=id)
    return item

