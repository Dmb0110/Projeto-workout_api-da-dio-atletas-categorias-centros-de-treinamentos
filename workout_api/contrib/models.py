from uuid import uuid4
from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class BaseModel(DeclarativeBase):
    # Classe base para todos os modelos ORM da aplicação.
    # Herda de DeclarativeBase, que é a forma moderna de declarar modelos no SQLAlchemy.
    # Centraliza configurações comuns e garante que todos os modelos compartilhem o mesmo metadata.

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),   # Define o tipo da coluna como UUID nativo do PostgreSQL.
        default=uuid4,           # Gera automaticamente um UUID v4 como valor padrão.
        nullable=False           # Campo obrigatório, não pode ser nulo.
    )
    # Campo "id" será a chave primária padrão para todos os modelos que herdarem de BaseModel.
    # Isso padroniza a estrutura das tabelas e evita repetição de código.
