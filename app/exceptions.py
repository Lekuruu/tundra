
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException

from .models import ErrorResponseObject, ResponseError
from .app import api

@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        ResponseError(
            ErrorResponse=ErrorResponseObject(
                errorCode=400,
                errorMessage='Invalid request'
            )
        ).model_dump(),
        status_code=400
    )

@api.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        ResponseError(
            ErrorResponse=ErrorResponseObject(
                errorCode=exc.status_code,
                errorMessage=exc.detail
            )
        ).model_dump(),
        status_code=exc.status_code
    )

@api.exception_handler(StarletteHTTPException)
async def starlette_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        ResponseError(
            ErrorResponse=ErrorResponseObject(
                errorCode=exc.status_code,
                message=exc.detail
            )
        ).model_dump(),
        status_code=exc.status_code
    )
