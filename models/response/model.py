# Pydantic
from pydantic import BaseModel, Field

# models
from models.response.data import ResponseData


class ResponseModel(BaseModel):
    code: int = Field(...)
    data: ResponseData = Field(...)