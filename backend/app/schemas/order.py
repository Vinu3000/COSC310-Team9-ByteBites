from pydantic import BaseModel
from typing import List, Optional
from app.models.enums import OrderStatus

class OrderCreate(BaseModel):
    restaurant_id: Optional[int] = 1
    items: List
    delivery_address: Optional[str] = "Standard Address"
    total_price: Optional[float] = 0.0

class OrderResponse(BaseModel):
    id: int
    restaurant_id: int
    items: List
    total_price: float
    subtotal: float
    status: str

    class Config:
        from_attributes = True

class TrackingResponse(BaseModel):
    order_id: str
    status: str
    display_message: str

    class Config:
        from_attributes = True