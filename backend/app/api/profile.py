"""
User Profile Router
Manages user profile viewing, name updates, and secure password changes.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, PasswordChange

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Returns the current user profile.
    """
    return current_user


@router.put("", response_model=UserResponse)
def update_profile(
    profile_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates the user's display name.
    """
    current_user.name = profile_in.name.strip()
    current_user.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.put("/password", status_code=status.HTTP_200_OK)
def change_password(
    pwd_in: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Changes user password after verifying their current password.
    """
    if not verify_password(pwd_in.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password entered is incorrect."
        )

    current_user.password_hash = get_password_hash(pwd_in.new_password)
    current_user.updated_at = datetime.now(timezone.utc)
    db.commit()

    return {"message": "Password updated successfully."}
