from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.core.exceptions import (
    CustomHTTPException,
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
    InternalServerErrorException,
)

async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    """
    Handler untuk custom HTTP exception.
    Mengembalikan respons JSON yang konsisten untuk semua error yang berasal dari CustomHTTPException.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,  # Kode error khusus aplikasi
            "detail": exc.detail,          # Pesan error yang deskriptif
        },
    )


async def validation_exception_handler(request: Request, exc: Exception):
    """
    Handler untuk error validasi (misalnya, Pydantic validation error).
    Mengembalikan respons JSON yang konsisten untuk error validasi.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error_code": "VALIDATION_ERROR",
            "detail": "Invalid request data. Please check your input.",
            "errors": str(exc),  # Detail error validasi
        },
    )


async def not_found_exception_handler(request: Request, exc: NotFoundException):
    """
    Handler khusus untuk NotFoundException.
    Mengembalikan respons JSON yang konsisten untuk error 404.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error_code": exc.error_code,
            "detail": exc.detail,
        },
    )


async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    """
    Handler khusus untuk BadRequestException.
    Mengembalikan respons JSON yang konsisten untuk error 400.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_code": exc.error_code,
            "detail": exc.detail,
        },
    )


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    """
    Handler khusus untuk UnauthorizedException.
    Mengembalikan respons JSON yang konsisten untuk error 401.
    """
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error_code": exc.error_code,
            "detail": exc.detail,
        },
    )


async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    """
    Handler khusus untuk ForbiddenException.
    Mengembalikan respons JSON yang konsisten untuk error 403.
    """
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error_code": exc.error_code,
            "detail": exc.detail,
        },
    )


async def internal_server_error_handler(request: Request, exc: InternalServerErrorException):
    """
    Handler untuk error internal server (500).
    Mengembalikan respons JSON yang konsisten untuk error yang tidak terduga.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "INTERNAL_ERROR",
            "detail": "An unexpected error occurred. Please try again later.",
        },
    )