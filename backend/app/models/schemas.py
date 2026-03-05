from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

class RestaurantResponse(BaseModel):
    id: UUID
    name: str
    location: str

class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float = Field(..., gt=0)
    restaurant_id: UUID

class PaginatedRestaurants(BaseModel):
    items: List[RestaurantResponse]
    total: int
    page: int
    size: int