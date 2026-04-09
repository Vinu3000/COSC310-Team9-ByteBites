from fastapi import APIRouter
from typing import List
from app.api.v1.shared_data import mock_notifications_db
from app.schemas.notification import NotificationResponse

router = APIRouter(tags=["Notifications"])

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications():
    """
    Returns all notifications. 
    Ensures a list is returned even if the mock database is empty.
    """
    # Defensive check: ensure we return a list to satisfy the response_model
    if not mock_notifications_db:
        return []
        
    return mock_notifications_db