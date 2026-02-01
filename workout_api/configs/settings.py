from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Classe responsável por carregar configurações da aplicação.
    # Herda de BaseSettings, permitindo integração com variáveis de ambiente.

    DB_URL: str = Field(
        default='postgresql+asyncpg://postgres:davi9090@localhost/workout',
        description='URL de conexão com o banco de dados'
    )
    # Campo que define a URL de conexão com o banco de dados.
    # Pode ser sobrescrito por variável de ambiente.
    # Exemplo: postgresql+asyncpg://usuario:senha@host:porta/nome_banco

    class Config:
        env_file = '.env'
        # Define que as variáveis de ambiente podem ser carregadas de um arquivo .env.
        # Isso facilita a configuração sem precisar alterar o código-fonte.

settings = Settings()
# Instancia única de Settings, usada em toda a aplicação para acessar as configurações.
