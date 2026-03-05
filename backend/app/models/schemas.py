from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

# Restaurant Response
class RestaurantResponse(BaseModel):
    id: UUID
    name: str
    location: str

    class Config:
        from_attributes = True

# Menu Item Creation
class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    restaurant_id: UUID

# Menu Item Response
class MenuItemResponse(MenuItemCreate):
    id: UUID

    class Config:
        from_attributes = True

# Pagination
class PaginatedRestaurants(BaseModel):
    items: List[RestaurantResponse]
    total: int
    page: int
    size: int