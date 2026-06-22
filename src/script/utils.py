import os
from pathlib import Path
from sqlalchemy import create_engine
from dotenv import load_dotenv

def get_database_engine():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    ENV_PATH = BASE_DIR / '.env'
    
    load_dotenv(dotenv_path=ENV_PATH)
    
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASS')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    
    if not db_user or not db_password:
        raise ValueError(f"Erro: Credenciais nao encontradas em: {ENV_PATH}")
    
    # Validação profissional com fail-fast detalhado
    missing_vars = []
    if not db_user: missing_vars.append('DB_USER')
    if not db_password: missing_vars.append('DB_PASS')
    if not db_name: missing_vars.append('DB_NAME')
    
    if missing_vars:
        raise ValueError(
            f"Erro: As seguintes variaveis nao foram encontradas no .env: {missing_vars}. "
            f"Arquivo lido em: {ENV_PATH}"
        )
        
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(connection_string)