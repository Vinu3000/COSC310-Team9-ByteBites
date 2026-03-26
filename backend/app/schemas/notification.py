from pydantic import BaseModel, ConfigDict

class NotificationResponse(BaseModel):
    """
    Schema for User notifications.
    """
    id: int
    order_id: int
    message: str
    timestamp: str

    model_config = ConfigDict(from_attributes=True)