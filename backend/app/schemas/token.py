from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Schema returned upon successful authentication containing JWT and basic user info."""
    access_token: str
    token_type: str = "bearer"
    user: dict


class TokenData(BaseModel):
    """Payload decoded from JWT token claims."""
    user_id: Optional[int] = None
    email: Optional[str] = None
