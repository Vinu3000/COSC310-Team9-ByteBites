from fastapi import APIRouter
from typing import List
from app.api.v1.shared_data import mock_notifications_db
from app.schemas.notification import NotificationResponse

router = APIRouter(tags=["Notifications"])

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications():
    """
    Returns all notifications. 
    Ensures the response is always a list to satisfy the Pydantic schema.
    """
    # 1. Handle Case: Database is None or empty
    if mock_notifications_db is None:
        return []

    # 2. Handle Case: Database is a dictionary (common if using ID-based mapping)
    if isinstance(mock_notifications_db, dict):
        return list(mock_notifications_db.values())

    # 3. Handle Case: Database is already a list (standard)
    if isinstance(mock_notifications_db, list):
        return mock_notifications_db

    # Fallback for unexpected types to prevent 500 Internal Server Error / Validation Error
    return []