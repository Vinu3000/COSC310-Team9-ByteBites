from fastapi import APIRouter, status, HTTPException
from typing import List, Dict
from pydantic import BaseModel

# --- Simple Data Models ---

class OrderCreate(BaseModel):
    """Data required to place an order."""
    restaurant_id: int
    items: List[str]
    total_price: float

class OrderResponse(BaseModel):
    """Response showing the basic order info."""
    id: int
    status: str
    total_price: float

class TrackingResponse(BaseModel):
    """Response for user tracking (Feat5-US1)."""
    order_id: int
    status: str
    display_message: str

# --- In-Memory Database ---
# We use a global dictionary to store orders during the test session.
mock_orders_db: Dict[int, dict] = {}
order_id_counter = 1

router = APIRouter(tags=["Orders"])

# --- Feature 4: Order Logic ---

@router.post("/place", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(payload: OrderCreate):
    """
    Feat4-US1: Create a new order. 
    All new orders start with 'PENDING' status.
    """
    global order_id_counter
    
    new_order = {
        "id": order_id_counter,
        "restaurant_id": payload.restaurant_id,
        "items": payload.items,
        "total_price": payload.total_price,
        "status": "PENDING"
    }
    
    # Save directly to the global dictionary
    mock_orders_db[order_id_counter] = new_order
    order_id_counter += 1
    return new_order

@router.put("/{order_id}/status")
async def update_order_status(order_id: int, new_status: str):
    """
    Feat4-FR1: If status is 'COMPLETED', prevent any further changes.
    This fulfills the requirement to lock finished orders.
    """
    if order_id not in mock_orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    
    # Get current status from our mock database
    current_status = mock_orders_db[order_id].get("status")

    # If it is already COMPLETED, block the update with 403.
    if current_status == "COMPLETED":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Order is completed and cannot be modified!"
        )

    # Update the status in the global dictionary
    mock_orders_db[order_id]["status"] = new_status
    return {"message": f"Order {order_id} updated to {new_status}"}

# --- Feature 5: Tracking Logic ---

@router.get("/{order_id}/tracking", response_model=TrackingResponse)
async def get_tracking(order_id: int):
    """
    Feat5-US1: Show tracking messages like 'Out for Delivery'.
    """
    if order_id not in mock_orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    current_status = mock_orders_db[order_id]["status"]
    
    # Default message
    msg = "Your meal is being prepared!"
    
    # Special message for Feat5-US1 requirement
    if current_status == "OUT_FOR_DELIVERY":
        msg = "Your driver is on the way! Watch the door!"
    elif current_status == "COMPLETED" or current_status == "DELIVERED":
        msg = "Enjoy your meal! Delivery finished."
        
    return {
        "order_id": order_id,
        "status": current_status,
        "display_message": msg
    }