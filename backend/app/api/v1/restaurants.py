from fastapi import APIRouter, Query
from app.models.schemas import PaginatedRestaurants

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.get("/", response_model=PaginatedRestaurants)
async def list_restaurants(
    page: int = Query(1, ge=1),   # making sure page >= 1
    size: int = Query(10, le=100) # limit amount of each page
):
    #restaurant_service
    return {"items": [], "total": 0, "page": page, "size": size}

@router.get("/search")
async def search_restaurants(q: str = Query(..., min_length=1)):
    # keyword
    return []