import logging

from sqlalchemy.orm import Session

from app import schemas, models
from app.db import base  # noqa: F401
from app.services import user_service

logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    # Create initial superuser
    user = user_service.get_by_email(db, email="admin@example.com")
    if not user:
        user_in = schemas.UserCreate(
            email="admin@example.com",
            password="admin",
            full_name="Initial Admin",
            is_superuser=True,
        )
        user = user_service.create(db, obj_in=user_in)
        logger.info("Initial superuser created")

