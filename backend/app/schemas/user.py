from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's unique email address")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100, description="User password (min 8 chars)")
    confirm_password: str = Field(..., min_length=8, max_length=100, description="Confirm password field")

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, values):
        password = values.data.get("password")
        if password and v != password:
            raise ValueError("Passwords do not match")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class UserUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class PasswordChange(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=100)
    confirm_new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("confirm_new_password")
    @classmethod
    def new_passwords_match(cls, v: str, values):
        new_pass = values.data.get("new_password")
        if new_pass and v != new_pass:
            raise ValueError("New passwords do not match")
        return v


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
