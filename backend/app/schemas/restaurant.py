from pydantic import BaseModel, ConfigDict
from typing import List
from uuid import UUID

# Restaurant Response
class RestaurantResponse(BaseModel):
    id: UUID
    name: str
    location: str
    model_config = ConfigDict(from_attributes=True)

# Pagination
class PaginatedRestaurants(BaseModel):
    items: List[RestaurantResponse]
    total: int
    page: int
    size: int
    pages: int