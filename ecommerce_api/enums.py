from enum import Enum


class OrderStatus(str, Enum):
    """
    Enums for customer order status
    """

    PENDING = "pending"
    COMPLETED = "completed"
    REFUNDED = "refunded"


class ErrorTypes(str, Enum):
    """
    Enums for custom error types
    """
    # App errors
    UNKNOWN = "unknown"

    # API errors
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    BAD_REQUEST = "bad_request"

    # Redis errors
    REDIS_ERROR = "redis_error"

    # Mongo db errors
    MONGO_DB_ERROR = "mongo_db_error"
