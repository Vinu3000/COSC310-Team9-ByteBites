from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class MenuItemCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    # Prevent invalid values (price must be positive)
    price: float = Field(..., gt=0) 
    restaurant_id: UUID

class MenuItemResponse(MenuItemCreate):
    id: UUID
    class Config:
        from_attributes = True