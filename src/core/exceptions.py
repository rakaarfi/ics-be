from fastapi import HTTPException
from fastapi import status

class CustomHTTPException(HTTPException):
    """
    Custom HTTPException class that extends FastAPI's HTTPException.
    Adds an error_code field for more detailed error handling.
    """
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None,
        headers: dict = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code


# Contoh error yang sering digunakan
class NotFoundException(CustomHTTPException):
    """Exception raised when a resource is not found."""
    def __init__(self, detail: str = "Resource not found", error_code: str = "NOT_FOUND"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code=error_code,
        )


class BadRequestException(CustomHTTPException):
    """Exception raised for bad request errors."""
    def __init__(self, detail: str = "Bad request", error_code: str = "BAD_REQUEST"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code,
        )


class UnauthorizedException(CustomHTTPException):
    """Exception raised when a user is not authorized."""
    def __init__(self, detail: str = "Unauthorized", error_code: str = "UNAUTHORIZED"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code=error_code,
        )


class ForbiddenException(CustomHTTPException):
    """Exception raised when access is forbidden."""
    def __init__(self, detail: str = "Forbidden", error_code: str = "FORBIDDEN"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code=error_code,
        )


class InternalServerErrorException(CustomHTTPException):
    """Exception raised for internal server errors."""
    def __init__(self, detail: str = "Internal server error", error_code: str = "INTERNAL_ERROR"):

        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code,
        )