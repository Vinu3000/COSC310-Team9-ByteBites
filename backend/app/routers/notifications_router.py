from fastapi import APIRouter

router = APIRouter()

notification_service = None


def set_notification_service(service):
    global notification_service
    notification_service = service


@router.get("/notifications")
def get_notifications():
    return notification_service.get_notifications()