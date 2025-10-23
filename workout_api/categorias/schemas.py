from typing import Annotated,Optional
from pydantic import UUID4,Field
from workout_api.contrib.schemas import BaseSchema

class CategoriaIn(BaseSchema):
    nome: Annotated[str,Field(description='Nome da categoria',example='Scale',max_length=30)]
    
class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4,Field(description='Identificador de categoria')]    


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro", example="CT Cruzília")]
    endereco: Annotated[str, Field(description="Endereço", example="Rua A, 123")]

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description="Identificador único do centro")]


class CategoriaUpdate(BaseSchema):
    nome: Annotated[Optional[str],Field(None,description='Nome do centro_treinamento',example='CT king',max_length=50)]
    endereco: Annotated[str, Field(None,description="Endereço", example="Rua A, 123")]

    