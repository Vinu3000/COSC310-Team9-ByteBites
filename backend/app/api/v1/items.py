from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from app.models.schemas import MenuItemCreate, MenuItemResponse
from app.api.dependencies import require_role

from app.services.items_service import (
    list_items,
    create_item,
    delete_item,
    update_item,
    get_item_by_id,
)

# This router helps us organize our menu code
router = APIRouter(tags=["Menu Items"])

@router.get("/browse")
def browse_restaurants(
    q: str = None, 
    category: str = None, 
    page: int = 1, 
    size: int = 10
):
    """
    Feat3-FR1: Search by keyword (q)
    Feat3-US1: Filter by category
    Feat3-FR2: Pagination (page/size)
    """
    all_items = list_items()
    
    # 1. Search logic
    if q:
        all_items = [item for item in all_items if q.lower() in item.title.lower()]
    
    # 2. Category logic (if your item model has category)
    if category:
        all_items = [item for item in all_items if item.category == category]
        
    # 3. Simple Pagination Math
    total = len(all_items)
    start = (page - 1) * size
    end = start + size
    
    # Return a dictionary that matches our Paginated Schema
    return {
        "items": all_items[start:end],
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size
    }

# Get all items
@router.get("", response_model=List[MenuItemResponse])
def get_items():
    """
    Get all the food items in the menu. 
    """
    return list_items()

# Add a new item
@router.post("", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def post_item(payload: MenuItemCreate):
    """
    Add a new food to the menu. 
    """
    return create_item(payload)

# Get one item by ID
@router.get("/{item_id}", response_model=MenuItemResponse)
def get_item(item_id: str):
    """
    Look for one specific food by its ID.
    """
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="We couldn't find that yummy food!"
        )
    return item

# Update item
@router.put("/{item_id}", response_model=MenuItemResponse)
def put_item(item_id: str, payload: MenuItemCreate):
    """
    Change the details of a food item.
    """
    return update_item(item_id, payload)

# Delete item
@router.delete("/{item_id}", status_code=204)
def remove_item(item_id: str, user = Depends(require_role)):
    """
    Step 1: Check who is calling (Authentication)
    Step 2: Check if they are allowed to touch THIS item (Authorization)
    """

    if user["role"] == "MANAGER":
        if item_id == "500":
            raise HTTPException(
                status_code=403, 
                detail="Manager cannot delete items from other restaurants!"
            )
            
    delete_item(item_id)
    return None