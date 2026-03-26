from fastapi import APIRouter
from typing import List
from app.api.v1.shared_data import mock_notifications_db
from app.schemas.notification import NotificationResponse

router = APIRouter(tags=["Notifications"])

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications():
    return mock_notifications_db