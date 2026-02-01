from typing import Annotated
from pydantic import Field, UUID4
from workout_api.contrib.schemas import BaseSchema

class CentroTreinamentoIn(BaseSchema):
    # Schema de entrada para criação de um novo centro de treinamento.
    # Contém os campos obrigatórios: nome, endereço e proprietário.
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='Ct king', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Rua x.002', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietario do centro de treinamento', example='Marcos', max_length=30)]
    

class CentroTreinamentoAtleta(BaseSchema):
    # Schema usado dentro do Atleta para referenciar o centro de treinamento.
    # Contém apenas o campo "nome" do centro.
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT king', max_length=20)]


class CentroTreinamentoOut(CentroTreinamentoIn):
    # Schema de saída para retornar dados de centro de treinamento.
    # Herda os campos de CentroTreinamentoIn e adiciona o identificador único (UUID).
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]


class CentroTreinamentoUpdate(BaseSchema):
    # Schema para atualização de centro de treinamento.
    # Permite alterar os campos nome, endereço e proprietário.
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='Ct king', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Rua x.002', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietario do centro de treinamento', example='Marcos', max_length=30)]
