from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Optional

class MenuItemCreate(BaseModel):
    """Schema for adding a new item (Feat2-US1)."""
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    # Prevent invalid values (price must be positive)
    price: float = Field(..., gt=0) 
    restaurant_id: UUID

class MenuItemResponse(MenuItemCreate):
    """Schema for returning item details (Feat3-FR1)."""
    id: UUID
    model_config = ConfigDict(from_attributes=True)