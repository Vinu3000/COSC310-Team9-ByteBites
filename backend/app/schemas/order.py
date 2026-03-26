from pydantic import BaseModel, ConfigDict
from typing import List

class OrderCreate(BaseModel):
    """
    Data needed to place a new order.
    Used in POST /orders/place
    
    """
    restaurant_id: int
    items: List[str]
    total_price: float

class OrderResponse(BaseModel):
    """
    Basic order information returned to the user.
    """
    id: int
    status: str
    total_price: float

    # allow working with ORM/Dict objects
    model_config = ConfigDict(from_attributes=True)

class TrackingResponse(BaseModel):
    """
    Response for order tracking status and messages.
    Used in GET /orders/{id}/tracking
    """
    order_id: int
    status: str
    display_message: str

    model_config = ConfigDict(from_attributes=True)