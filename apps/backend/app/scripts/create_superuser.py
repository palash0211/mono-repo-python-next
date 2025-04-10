import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.services.user_service import user_service

def create_superuser(email: str, password: str, full_name: str) -> None:
    db = SessionLocal()
    try:
        # Check if user exists
        user = user_service.get_by_email(db, email=email)
        if user:
            print(f"User with email {email} already exists")
            return
        
        # Create new superuser
        user_in = UserCreate(
            email=email,
            password=password,
            full_name=full_name,
            is_superuser=True,
        )
        user = user_service.create(db, obj_in=user_in)
        print(f"Superuser {email} created successfully")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_superuser.py <email> <password> <full_name>")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    full_name = sys.argv[3]
    
    create_superuser(email, password, full_name)

