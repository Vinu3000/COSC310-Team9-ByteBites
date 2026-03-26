from fastapi import APIRouter
from typing import List
# Import the shared list from orders.py so we see the same data
from app.api.v1.orders import mock_notifications_db
from app.schemas.notification import NotificationResponse

router = APIRouter(tags=["Notifications"])

@router.get("/", response_model=List[NotificationResponse])
async def get_all_notifications():
    """
    Feat8-US1: Get the list of all system notifications.
    """
    return mock_notifications_db