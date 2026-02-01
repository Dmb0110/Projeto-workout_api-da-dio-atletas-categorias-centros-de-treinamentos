from typing import Annotated
from pydantic import UUID4, BaseModel, Field
from sqlalchemy import DateTime
from datetime import datetime 

class BaseSchema(BaseModel):
    # Classe base para todos os schemas da aplicação.
    # Herda de BaseModel do Pydantic.
    # Configurações:
    class Config:
        extra = 'forbid'          # Proíbe campos extras não definidos no schema.
        from_attributes = True    # Permite criar instâncias a partir de objetos ORM (atributos).

class OutMixin(BaseModel):
    # Mixin usado em schemas de saída.
    # Adiciona campos padrão que geralmente existem em todos os recursos.
    
    id: Annotated[UUID4, Field(description='identificador')]
    # Campo "id" → identificador único do recurso, do tipo UUID.

    created_at: Annotated[datetime, Field(description='Data de criação')]
    # Campo "created_at" → data e hora em que o recurso foi criado.
