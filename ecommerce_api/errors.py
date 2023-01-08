from fastapi import status

from ecommerce_api.enums import ErrorTypes


class AppException(Exception):
    """
    Base app exception class
    """
    http_status_code: status = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_type: ErrorTypes = ErrorTypes.UNKNOWN
    details: str = None

    def __init__(
        self,
        http_status_code: status = None,
        error_type: str = None,
        details: str = None
    ):
        self.http_status_code = http_status_code or self.http_status_code
        self.error_type = error_type or self.error_type
        self.details = details or self.details
        super(AppException, self).__init__()


class ApiException(AppException):
    pass


class Unauthorized(ApiException):
    http_status_code: status = status.HTTP_401_UNAUTHORIZED
    error_type: ErrorTypes = ErrorTypes.UNAUTHORIZED
    details: str = "Unauthorized. Invalid or expired token"


class Forbidden(ApiException):
    http_status_code: status = status.HTTP_403_FORBIDDEN
    error_type: ErrorTypes = ErrorTypes.FORBIDDEN
    details: str = "Access forbidden"


class BadRequest(ApiException):
    http_status_code: status = status.HTTP_400_BAD_REQUEST
    error_type: ErrorTypes = ErrorTypes.BAD_REQUEST
    details: str = "Bad request"


class NotFound(ApiException):
    http_status_code: status = status.HTTP_404_NOT_FOUND
    error_type: ErrorTypes = ErrorTypes.NOT_FOUND
    details: str = "Bad request"


class RedisException(AppException):
    error_type: ErrorTypes = ErrorTypes.REDIS_ERROR
    details: str = "Redis error"


class MongoDbError(AppException):
    error_type: ErrorTypes = ErrorTypes.MONGO_DB_ERROR
    details: str = "Mongo DB error"


class MongoDbNoUser(AppException):
    error_type: ErrorTypes = ErrorTypes.MONGO_DB_NO_USER
    details: str = "No user with this email"
