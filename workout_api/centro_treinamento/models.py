from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from workout_api.contrib.models import BaseModel
from workout_api.atleta.models import AtletaModel

class CentroTreinamentoModel(BaseModel):
    __tablename__ = 'centro_treinamento'
    # Define o nome da tabela no banco de dados como "centro_treinamento".

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Chave primária da tabela, do tipo inteiro.

    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    # Nome do centro de treinamento, obrigatório, único e limitado a 50 caracteres.

    endereco: Mapped[str] = mapped_column(String(60), nullable=False)
    # Endereço do centro de treinamento, obrigatório, limitado a 60 caracteres.

    proprietario: Mapped[str] = mapped_column(String(30), nullable=False)
    # Nome do proprietário do centro de treinamento, obrigatório, limitado a 30 caracteres.

    atleta: Mapped[list[AtletaModel]] = relationship(back_populates='centro_treinamento')
    # Relacionamento com a tabela de atletas.
    # Um centro de treinamento pode estar associado a vários atletas.
    # O parâmetro back_populates conecta com o campo "centro_treinamento" definido em AtletaModel.
