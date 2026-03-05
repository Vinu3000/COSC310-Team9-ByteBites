from typing import List, Optional
from uuid import UUID
from app.models.schemas import RestaurantResponse

class RestaurantRepository:
    def __init__(self):
        # Using a mock list to simulate database records for M3 demo
        self._restaurants = [] 

    def get_all_paginated(self, skip: int, limit: int) -> List[dict]:
        """Fetch restaurants with pagination logic[cite: 356]."""
        return self._restaurants[skip : skip + limit]

    def get_by_id(self, restaurant_id: UUID) -> Optional[dict]:
        """Find a specific restaurant to ensure referential integrity[cite: 354]."""
        return next((r for r in self._restaurants if r["id"] == restaurant_id), None)

    def search(self, query: str) -> List[dict]:
        """Filter restaurants by keyword in name or location[cite: 355]."""
        return [
            r for r in self._restaurants 
            if query.lower() in r["name"].lower() or query.lower() in r["location"].lower()
        ]