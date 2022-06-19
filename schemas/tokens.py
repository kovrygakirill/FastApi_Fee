from typing import Optional
from pydantic import UUID4, BaseModel, Field, validator
from datetime import datetime


class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(cls, value):
        """ Конвертирует UUID в hex строку """
        return value.hex
