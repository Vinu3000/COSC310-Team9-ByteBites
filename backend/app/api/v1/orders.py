from fastapi import APIRouter, status, HTTPException
from typing import List, Dict
from pydantic import BaseModel

# --- Schemas ---

class OrderCreate(BaseModel):
    restaurant_id: int
    items: List[str]
    total_price: float

class OrderResponse(BaseModel):
    id: int
    status: str
    total_price: float

class TrackingResponse(BaseModel):
    """Schema for Feat5-US1: User tracking view"""
    order_id: int
    status: str
    display_message: str

# --- Mock Database ---
mock_orders_db: Dict[int, dict] = {}
order_id_counter = 1

router = APIRouter(tags=["Orders"])

# Feat4-US1: Place an order
@router.post("/place", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(payload: OrderCreate):
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

# Feat5-FR1: Update delivery status (Real-time tracking)
@router.put("/{order_id}/status")
async def update_order_status(order_id: int, new_status: str):
    """
    Feat4-FR1 & Feat5-FR1: Update status and lock if COMPLETED.
    """
    if order_id not in mock_orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    current_order = mock_orders_db[order_id]

    # FR1 Lock logic
    if current_order["status"] == "COMPLETED":
        raise HTTPException(
            status_code=403, 
            detail="Order is completed and cannot be modified!"
        )

    current_order["status"] = new_status
    return {"message": f"Order {order_id} updated to {new_status}"}

# Feat5-US1: User tracking endpoint
@router.get("/{order_id}/tracking", response_model=TrackingResponse)
async def get_tracking(order_id: int):
    """
    As a user, I want to see if my order is 'Out for Delivery'.
    """
    if order_id not in mock_orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    current_status = mock_orders_db[order_id]["status"]
    
    # Custom message based on status for the UI
    msg = "Your meal is being prepared with love!"
    if current_status == "OUT_FOR_DELIVERY":
        msg = "Your driver is on the way! Get ready!"
    elif current_status == "DELIVERED":
        msg = "Enjoy your meal!"
        
    return {
        "order_id": order_id,
        "status": current_status,
        "display_message": msg
    }