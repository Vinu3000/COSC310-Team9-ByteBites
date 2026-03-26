from fastapi import APIRouter, status, HTTPException
from typing import List, Dict
from datetime import datetime

from app.schemas.order import OrderCreate, OrderResponse, TrackingResponse
from app.schemas.notification import NotificationResponse

# --- In-Memory Databases ---
# These store data while the server is running
mock_orders_db: Dict[int, dict] = {}
mock_notifications_db: List[dict] = []

# Counters for IDs
order_id_counter = 1
notification_id_counter = 1

router = APIRouter(tags=["Orders"])

# --- Helper Function ---

def send_notification(order_id: int, message: str):
    """
    Feat8-FR1: Create a notification event in the system.
    This is a simple helper to add messages to our list.
    """
    global notification_id_counter
    notif = {
        "id": notification_id_counter,
        "order_id": order_id,
        "message": message,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    mock_notifications_db.append(notif)
    notification_id_counter += 1

# --- Order Logic ---

@router.post("/place", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(payload: OrderCreate):
    """
    Feat4-US1: Create a new order for the user.
    Feat8-US1: Make sure user gets a notification when it is accepted.
    """
    global order_id_counter
    
    new_order = {
        "id": order_id_counter,
        "restaurant_id": payload.restaurant_id,
        "items": payload.items,
        "total_price": payload.total_price,
        "status": "ACCEPTED" 
    }
    
    mock_orders_db[order_id_counter] = new_order
    
    # Create the first notification for the new order
    send_notification(
        order_id_counter, 
        f"Order #{order_id_counter} has been accepted by the restaurant!"
    )
    
    order_id_counter += 1
    return new_order

@router.put("/{order_id}/status")
async def update_order_status(order_id: int, new_status: str):
    """
    Feat4-FR1: If an order is 'COMPLETED', do not let anyone change it.
    Feat8-FR1: Send a notification every time the status changes.
    """
    if order_id not in mock_orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    current_status = mock_orders_db[order_id].get("status")

    # Lock the order if it is already finished
    if current_status == "COMPLETED":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Order is completed and cannot be modified!"
        )

    # Change the status in the database
    mock_orders_db[order_id]["status"] = new_status
    
    # Create a notification for this status update
    send_notification(
        order_id, 
        f"Your order status is now: {new_status}"
    )
    
    return {"message": f"Order {order_id} updated to {new_status}"}

# --- Tracking & Notification Logic ---

@router.get("/{order_id}/tracking", response_model=TrackingResponse)
async def get_tracking(order_id: int):
    """
    Feat5-US1: Show the user a nice message about their delivery.
    """
    if order_id not in mock_orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    current_status = mock_orders_db[order_id]["status"]
    msg = "Your meal is being prepared!"
    
    if current_status == "OUT_FOR_DELIVERY":
        msg = "Your driver is on the way! Watch the door!"
    elif current_status == "COMPLETED" or current_status == "DELIVERED":
        msg = "Enjoy your meal! Delivery finished."
        
    return {
        "order_id": order_id,
        "status": current_status,
        "display_message": msg
    }

@router.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications():
    """
    Feat8-US1: Show the list of notifications to the user.
    """
    return mock_notifications_db