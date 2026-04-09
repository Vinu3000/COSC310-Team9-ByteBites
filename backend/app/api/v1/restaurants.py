from fastapi import APIRouter, Query, HTTPException
from app.schemas.restaurant import PaginatedRestaurants, RestaurantResponse
from app.api.v1.shared_data import mock_restaurants_db 
from app.services.restaurant_service import (
    filter_restaurants, 
    paginate_data, 
    map_to_restaurant_schema
)

router = APIRouter(tags=["Restaurants"])

@router.get("/", response_model=PaginatedRestaurants)
async def list_restaurants(
    q: str = Query(None, description="Search by name or cuisine"),
    category: str = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100)
):
    all_raw_data = mock_restaurants_db 
    
    # Filter by both search term and category
    filtered_data = filter_restaurants(all_raw_data, q, category)
    sliced_data, total_pages = paginate_data(filtered_data, page, size)
    
    # Map raw data to the schema format
    formatted_restaurants = map_to_restaurant_schema(sliced_data)
    
    return {
        "items": formatted_restaurants,
        "total": len(filtered_data),
        "page": page,
        "size": size,
        "pages": total_pages
    }

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant_details(restaurant_id: str):
    """
    Handles both integer IDs and UUID-formatted strings by extracting 
    the trailing integer used in the mock database.
    """
    target_id = None

    # Handle UUID format (e.g., 0000-000000000001)
    if "-" in restaurant_id:
        try:
            # Extract the last part after the hyphen and convert to int
            target_id = int(restaurant_id.split("-")[-1])
        except (ValueError, IndexError):
            raise HTTPException(status_code=404, detail="Invalid ID format")
    
    # Handle plain integer string (e.g., "1")
    elif restaurant_id.isdigit():
        target_id = int(restaurant_id)
    
    else:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Search in the mock database using the extracted integer ID
    raw_restaurant = next((r for r in mock_restaurants_db if r["id"] == target_id), None)
    
    if not raw_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Ensure the 'menu' and other fields are mapped correctly to the response schema
    formatted_list = map_to_restaurant_schema([raw_restaurant])
    return formatted_list[0]