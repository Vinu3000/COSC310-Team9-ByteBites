from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID

class MenuItemSchema(BaseModel):
    id: int
    name: str
    price: float
    model_config = ConfigDict(from_attributes=True)

class RestaurantResponse(BaseModel):
    id: UUID
    name: str
    title: str
    location: str
    cuisine_type: str
    category: str
    rating: float
    menu: List[MenuItemSchema] = [] # 确保这里有 menu
    model_config = ConfigDict(from_attributes=True)

class PaginatedRestaurants(BaseModel):
    items: List[RestaurantResponse]
    total: int
    page: int
    size: int
    pages: int