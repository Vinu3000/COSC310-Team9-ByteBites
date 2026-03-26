class NotificationService:
    def __init__(self, notification_repository):
        self.notification_repository = notification_repository

    def create_notification(self, order_id, message):
        notification = {
            "order_id": order_id,
            "message": message
        }
        return self.notification_repository.create(notification)

    def get_notifications(self):
        return self.notification_repository.get_all()