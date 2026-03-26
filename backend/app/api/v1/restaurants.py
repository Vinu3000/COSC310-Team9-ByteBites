from fastapi import APIRouter, Query
from app.schemas.restaurant import PaginatedRestaurants
from app.services.items_service import list_items 
from app.services.restaurant_service import (
    filter_restaurants, 
    paginate_data, 
    map_to_restaurant_schema
)

router = APIRouter(tags=["Restaurants"])

@router.get("/", response_model=PaginatedRestaurants)
async def list_restaurants(
    q: str = Query(None),
    category: str = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100)
):
    """
    Feat3: Search and browse restaurants.
    The logic is now handled by the restaurant_service for better testing.
    """
    # 1. Get the raw data from the main list
    all_raw_data = list_items() 
    
    # 2. Use the service to filter based on user search or category
    filtered_data = filter_restaurants(all_raw_data, q, category)
    
    # 3. Use the service to cut the list into the right page
    sliced_data, total_pages = paginate_data(filtered_data, page, size)
    
    # 4. Use the service to change the format to match our Schema
    formatted_restaurants = map_to_restaurant_schema(sliced_data)
    
    # 5. Return the clean dictionary
    return {
        "items": formatted_restaurants,
        "total": len(filtered_data),
        "page": page,
        "size": size,
        "pages": total_pages
    }