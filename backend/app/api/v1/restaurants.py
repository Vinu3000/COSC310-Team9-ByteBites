from fastapi import APIRouter, Query, HTTPException
from app.schemas.restaurant import PaginatedRestaurants
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

    # 1. Get raw data from the shared database
    all_raw_data = mock_restaurants_db 
    
    # 2. Apply filtering logic through the service layer
    filtered_data = filter_restaurants(all_raw_data, q, category)
    
    # 3. Apply pagination logic through the service layer
    sliced_data, total_pages = paginate_data(filtered_data, page, size)
    
    # 4. Map data to schema format (this ensures all required Pydantic fields exist)
    formatted_restaurants = map_to_restaurant_schema(sliced_data)
    
    # 5. Return the payload. Ensure 'pages' matches the schema field name exactly.
    return {
        "items": formatted_restaurants,
        "total": len(filtered_data),
        "page": page,
        "size": size,
        "pages": total_pages
    }

@router.get("/{restaurant_id}")
async def get_restaurant_details(restaurant_id: int):
    """
    Feature 2: Menu Management and Data Integrity.
    Retrieves a single restaurant and its nested menu items.
    """
    restaurant = next((r for r in mock_restaurants_db if r["id"] == restaurant_id), None)
    
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
        
    return restaurant

@router.get("/menu/search")
async def search_menu_items(q: str = Query(..., min_length=1)):
    """
    Feature 3: Keyword search across all restaurant menus.
    """
    results = []
    for res in mock_restaurants_db:
        # Check if 'menu' exists and is a list to avoid 500 errors
        menu = res.get("menu", [])
        if not isinstance(menu, list):
            continue
            
        for item in menu:
            if q.lower() in item.get("name", "").lower():
                results.append({
                    "restaurant_name": res["name"],
                    "item": item
                })
    return results