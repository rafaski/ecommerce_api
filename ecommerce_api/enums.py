from enum import Enum


class UserType(str, Enum):
    """
    User type
    """
    ADMIN = "admin"
    CUSTOMER = "customer"


class ProductCategory(str, Enum):
    """
    Enums for product category
    """
    PHONES = "phones"
    LAPTOPS = "laptops"
    TABLETS = "tablets"
    ACCESSORIES = "accessories"


class OrderStatus(str, Enum):
    """
    Enums for customer order status
    """

    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
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
    NOT_FOUND = "not_found"

    # Redis errors
    REDIS_ERROR = "redis_error"

    # Mongo db errors
    MONGO_DB_ERROR = "mongo_db_error"
    MONGO_DB_NO_USER = "mongo_db_no_user"
