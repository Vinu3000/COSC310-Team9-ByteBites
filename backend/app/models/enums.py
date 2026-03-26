from enum import Enum

class OrderStatus(str, Enum):
    """
    Enum to replace magic strings for order states.
    This prevents typos and improves type safety.
    """
    PENDING = "Pending"
    PREPARING = "Preparing"
    SHIPPING = "OutForDelivery"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"