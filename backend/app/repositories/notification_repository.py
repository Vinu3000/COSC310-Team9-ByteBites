import uuid


class NotificationRepository:
    def __init__(self):
        self.notifications = []

    def create(self, notification_data):
        notification_data["id"] = str(uuid.uuid4())
        self.notifications.append(notification_data)
        return notification_data

    def get_all(self):
        return self.notifications