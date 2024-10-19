import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

class Config:
    # chave secreta usada para proteger sessões e dados sensíveis
    SECRET_KEY = os.getenv('SECRET_KEY')

    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    PASSWORD = quote(DB_PASSWORD)
    
    # Configura a string de conexão com o banco de daados PostgreSQL (via Supabase)
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    
    # Outras configurações
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
    DEBUG = os.getenv('DEBUG', 'False') == 'True'