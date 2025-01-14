
from pydantic import BaseModel

class ErrorResponseObject(BaseModel):
    errorCode: int
    message: str

class ResponseError(BaseModel):
    errorResponse: ErrorResponseObject
    userSuggestion: str = ""
