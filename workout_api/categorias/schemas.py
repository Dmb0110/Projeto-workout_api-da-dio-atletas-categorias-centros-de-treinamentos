from typing import Annotated,Optional
from pydantic import UUID4,Field
from workout_api.contrib.schemas import BaseSchema

class CategoriaIn(BaseSchema):
    # Schema de entrada para criação de uma nova categoria.
    # Contém apenas o campo "nome", obrigatório, com limite de 30 caracteres.
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=30)]
    

class CategoriaOut(CategoriaIn):
    # Schema de saída para retornar dados de categoria.
    # Herda o campo "nome" de CategoriaIn e adiciona o identificador único (UUID).
    id: Annotated[UUID4, Field(description='Identificador de categoria')]    


class CentroTreinamentoIn(BaseSchema):
    # Schema de entrada para criação de um novo centro de treinamento.
    # Contém os campos "nome" e "endereco", ambos obrigatórios.
    nome: Annotated[str, Field(description="Nome do centro", example="CT Cruzília")]
    endereco: Annotated[str, Field(description="Endereço", example="Rua A, 123")]


class CentroTreinamentoOut(CentroTreinamentoIn):
    # Schema de saída para retornar dados de centro de treinamento.
    # Herda os campos de CentroTreinamentoIn e adiciona o identificador único (UUID).
    id: Annotated[UUID4, Field(description="Identificador único do centro")]


class CategoriaUpdate(BaseSchema):
    # Schema para atualização parcial de categoria.
    # Permite alterar opcionalmente o "nome" e o "endereco".
    nome: Annotated[Optional[str], Field(None, description='Nome do centro_treinamento', example='CT king', max_length=50)]
    endereco: Annotated[str, Field(None, description="Endereço", example="Rua A, 123")]



