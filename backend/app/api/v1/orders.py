from fastapi import APIRouter, status, HTTPException
from typing import List, Dict
from pydantic import BaseModel

# --- Schemas ---

class OrderCreate(BaseModel):
    """Schema for placing a new order (Feat4-US1)."""
    restaurant_id: int
    items: List[str]
    total_price: float

class OrderResponse(BaseModel):
    """Basic order info returned after creation."""
    id: int
    status: str
    total_price: float

class TrackingResponse(BaseModel):
    """Detailed tracking info for the user (Feat5-US1)."""
    order_id: int
    status: str
    display_message: str

# --- Mock Database ---
# Using a global dictionary to store order state in memory.
mock_orders_db: Dict[int, dict] = {}
order_id_counter = 1

router = APIRouter(tags=["Orders"])

# --- Feature 4: Order Creation ---

@router.post("/place", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(payload: OrderCreate):
    """
    Feat4-US1: As a user, I want to place an order from a restaurant.
    Initial status is always 'PENDING'.
    """
    global order_id_counter
    
    new_order = {
        "id": order_id_counter,
        "restaurant_id": payload.restaurant_id,
        "items": payload.items,
        "total_price": payload.total_price,
        "status": "PENDING"
    }
    
    mock_orders_db[order_id_counter] = new_order
    order_id_counter += 1
    return new_order

# --- Feature 5: Delivery & Status Updates ---

@router.put("/{order_id}/status")
async def update_order_status(order_id: int, new_status: str):
    """
    Feat4-FR1 & Feat5-FR1: Update order/delivery status.
    Strictly prevents modification if the current status is 'COMPLETED'.
    """
    if order_id not in mock_orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    
    # FR1: Lock logic - check current status before updating
    if mock_orders_db[order_id]["status"] == "COMPLETED":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Order is completed and cannot be modified!"
        )

    mock_orders_db[order_id]["status"] = new_status
    
    return {"message": f"Order {order_id} updated to {new_status}"}

@router.get("/{order_id}/tracking", response_model=TrackingResponse)
async def get_tracking(order_id: int):
    """
    Feat5-US1: As a user, I want to see if my order is 'Out for Delivery'.
    Returns a human-readable message based on the internal status.
    """
    if order_id not in mock_orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    
    current_status = mock_orders_db[order_id]["status"]
    
    # Default message for PENDING or PREPARING
    msg = "Your meal is being prepared with love!"
    
    # Specific message for Feat5-US1 requirement
    if current_status == "OUT_FOR_DELIVERY":
        msg = "Your driver is on the way! Get ready!"
    elif current_status == "DELIVERED" or current_status == "COMPLETED":
        msg = "Enjoy your meal! It has been delivered."
        
    return {
        "order_id": order_id,
        "status": current_status,
        "display_message": msg
    }