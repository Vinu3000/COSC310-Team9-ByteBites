from fastapi import APIRouter, Query
from typing import List
import uuid
from app.schemas.restaurant import PaginatedRestaurants
from app.services.items_service import list_items 

router = APIRouter(tags=["Restaurants"])

@router.get("/", response_model=PaginatedRestaurants)
async def list_restaurants(
    q: str = Query(None),
    category: str = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100)
):
    all_raw_data = list_items() 
    if q:
        all_raw_data = [r for r in all_raw_data if q.lower() in r.title.lower()]
    if category:
        all_raw_data = [r for r in all_raw_data if r.category == category]
        
    total = len(all_raw_data)
    start = (page - 1) * size
    end = start + size
    sliced_data = all_raw_data[start:end]
    
    formatted_restaurants = []
    for item in sliced_data:
        fake_uuid = uuid.UUID(int=int(item.id)) 
        formatted_restaurants.append({
            "id": fake_uuid,
            "name": item.title,
            "location": "UBCO Campus",
            "category": item.category
        })
    
    total_pages = (total + size - 1) // size
    return {
        "items": formatted_restaurants,
        "total": total,
        "page": page,
        "size": size,
        "pages": total_pages
    }
