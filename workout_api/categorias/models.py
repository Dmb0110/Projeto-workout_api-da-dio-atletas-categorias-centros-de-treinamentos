from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from workout_api.contrib.models import BaseModel
from workout_api.atleta.models import AtletaModel

class CategoriaModel(BaseModel):
    __tablename__ = 'categorias'  
    # Define o nome da tabela no banco de dados como "categorias".

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Chave primária da tabela, do tipo inteiro.

    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    # Nome da categoria, obrigatório, único e limitado a 50 caracteres.

    atleta: Mapped[list[AtletaModel]] = relationship(back_populates='categoria', lazy='selectin')
    # Relacionamento com a tabela de atletas.
    # Uma categoria pode estar associada a vários atletas.
    # O parâmetro back_populates conecta com o campo "categoria" definido em AtletaModel.
    # O lazy='selectin' otimiza o carregamento das relações.
