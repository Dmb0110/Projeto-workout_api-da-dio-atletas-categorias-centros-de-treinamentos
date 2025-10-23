from typing import Annotated
from pydantic import UUID4, BaseModel, Field
from sqlalchemy import DateTime
from datetime import datetime

class BaseSchema(BaseModel):
    class Config:
        extra = 'forbid'
        from_attributes = True

class OutMixin(BaseModel):
    id: Annotated[UUID4, Field(description='identificador')]
    created_at: Annotated[datetime, Field(description='Data de criaçao')]

        