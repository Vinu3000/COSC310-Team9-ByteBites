from fastapi import APIRouter, status, HTTPException, Depends
from typing import List, Dict
from pydantic import BaseModel

# --- Simple Schemas for Orders ---

class OrderCreate(BaseModel):
    """Data needed to place a new order."""
    restaurant_id: int
    items: List[str]
    total_price: float

class OrderResponse(BaseModel):
    """What the user sees after creating an order."""
    id: int
    status: str
    total_price: float

# --- Mock Database ---
# use a dictionary to store orders in memory.
mock_orders_db: Dict[int, dict] = {}
order_id_counter = 1

router = APIRouter(tags=["Orders"])

@router.post("/place", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(payload: OrderCreate):
    """
    Feat4-US1: As a user, I want to place an order from a restaurant.
    This function saves the order details into our mock database.
    """
    global order_id_counter
    
    new_order = {
        "id": order_id_counter,
        "restaurant_id": payload.restaurant_id,
        "items": payload.items,
        "total_price": payload.total_price,
        "status": "PENDING"  # All new orders start as Pending
    }
    
    # Save to our "database"
    mock_orders_db[order_id_counter] = new_order
    order_id_counter += 1
    
    return new_order

@router.put("/{order_id}/status")
async def update_order_status(order_id: int, new_status: str):
    """
    Feat4-FR1: The system shall prevent modification once an order is COMPLETED.
    This ensures that once a meal is delivered, nobody can change the price or items.
    """
    # Check if order exists
    if order_id not in mock_orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found!"
        )
    
    current_order = mock_orders_db[order_id]

    # If status is already 'COMPLETED', block any changes
    if current_order["status"] == "COMPLETED":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This order is already COMPLETED and cannot be modified."
        )

    # Update the status if it wasn't completed yet
    current_order["status"] = new_status
    return {"message": f"Order {order_id} updated to {new_status}"}

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_details(order_id: int):
    """Helper route to check order status."""
    if order_id not in mock_orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return mock_orders_db[order_id]