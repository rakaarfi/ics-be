import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from src.infrastructure.config.database import drop_table, init_db
from src.infrastructure.api.routers import configure_routers
from src.infrastructure.api.exception_handlers import (
    custom_http_exception_handler,
    validation_exception_handler,
    not_found_exception_handler,
    bad_request_exception_handler,
    unauthorized_exception_handler,
    forbidden_exception_handler,
    internal_server_error_handler,
)
from src.core.exceptions import (
    CustomHTTPException,
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
)


app = FastAPI()

# Configurate CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://172.28.49.140:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurate logging
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set SQLAlchemy log level to WARNING
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


# Run the database setup on startup
@app.on_event("startup")
async def on_startup():
    # await drop_table()  # Uncomment this line if you want to drop the table when starting up
    await init_db()


# Add router to FastAPI
configure_routers(app)

# Add exception handlers
app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
app.add_exception_handler(ForbiddenException, forbidden_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, internal_server_error_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)