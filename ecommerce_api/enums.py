from enum import Enum


class OrderStatus(str, Enum):
    """
    Enums for customer order status
    """

    PENDING = "pending"
    COMPLETED = "completed"
    REFUNDED = "refunded"
