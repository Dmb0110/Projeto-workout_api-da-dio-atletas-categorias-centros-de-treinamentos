from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta

from workout_api.contrib.schemas import BaseSchema, OutMixin

class AtletaIn(BaseSchema):
    # Schema de entrada para criação de um novo atleta.
    # Define os campos obrigatórios e suas validações.
    nome: Annotated[str, Field(description='Nome do atleta', example='Joao', max_length=50)]
    cpf: Annotated[str, Field(description='cpf do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='idade do atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(description='peso do atleta', example=75.5)]
    altura: Annotated[PositiveFloat, Field(description='altura do atleta', example=1.70)]
    sexo: Annotated[str, Field(description='sexo do atleta', example='M', max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]


class AtletaIn(AtletaIn):
    # Classe duplicada para manter consistência de nomenclatura.
    # Pode ser usada como alias ou extensão futura.
    pass

class AtletaOut(AtletaIn, OutMixin):
    # Schema de saída para retornar dados de atleta.
    # Herda os campos de AtletaIn e adiciona mixins de saída (ex: id, created_at).
    pass


class AtletaUpdate(BaseSchema):
    # Schema para atualização parcial de atleta.
    # Todos os campos são opcionais, permitindo PATCH.
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Joao', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(None, description='peso do atleta', example=75.5)]
