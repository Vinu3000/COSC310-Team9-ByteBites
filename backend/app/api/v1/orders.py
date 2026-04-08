from fastapi import APIRouter, status, HTTPException, Depends
from app.schemas.order import OrderCreate, OrderResponse
from app.models.enums import OrderStatus
from app.services.order_service import OrderService
from app.api.v1.shared_data import mock_notifications_db, mock_orders_db
from datetime import datetime

router = APIRouter(tags=["Orders"])

def get_service():
    from app.main import order_service
    return order_service

# --- Create Order ---
@router.post("/place", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(payload: OrderCreate, service: OrderService = Depends(get_service)):
    my_items = payload.items
    res = service.create_order(my_items, payload.delivery_address)
    
    mock_notifications_db.append({
        "id": len(mock_notifications_db) + 1, 
        "order_id": 1, 
        "message": "Order has been accepted!", 
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

    return {
        "id": 1,
        "restaurant_id": 1,
        "items": my_items,
        "subtotal": res.get("subtotal", 0.0),
        "total_price": res.get("total_price", 0.0),
        "status": "PENDING"
    }

# --- Simulated Payment (Real Implementation) ---
@router.post("/{order_id}/pay")
async def process_payment(order_id: int):
    """
    Handles Feature 7: Real backend update for payment status.
    Updates the shared database so the frontend sees the change.
    """
    if order_id not in mock_orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order = mock_orders_db[order_id]
    order["payment_status"] = "Success"
    
    # Feature 5 & 8
    order["status"] = "Preparing"
    
    mock_notifications_db.append({
        "id": len(mock_notifications_db) + 1,
        "order_id": order_id,
        "message": f"Payment for Order #{order_id} was successful!",
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    return {
        "message": f"Payment for Order #{order_id} successful!",
        "new_payment_status": "Success",
        "new_order_status": "Preparing"
    }

# --- Delivery Tracking ---
@router.get("/{order_id}/tracking")
async def get_tracking(order_id: str):
    return {
        "order_id": order_id, 
        "status": "OUT_FOR_DELIVERY", 
        "display_message": "On the way"
    }

# --- Update Order Status ---
@router.put("/{order_id}/status")
async def update_status(order_id: str, new_status: str, service: OrderService = Depends(get_service)):
    lookup = {"COMPLETED": OrderStatus.COMPLETED, "OUT_FOR_DELIVERY": OrderStatus.SHIPPING}
    target = lookup.get(new_status.upper(), OrderStatus.PENDING)
    try:
        updated_order = service.update_order_status(order_id, target)
        
        mock_notifications_db.append({
            "id": len(mock_notifications_db) + 1,
            "order_id": order_id,
            "message": f"Order #{order_id} status updated to {new_status}",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        return updated_order
    except Exception as e:
        if "cannot be modified" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# --- List Orders ---
@router.get("/")
async def get_all_orders():
   return list(mock_orders_db.values())