import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Caminho base do projeto

UPLOAD_FOLDER_PATH = os.path.join(BASE_DIR, "uploads")

# Cria a pasta uploads se não existir
if not os.path.exists(UPLOAD_FOLDER_PATH):
    os.makedirs(UPLOAD_FOLDER_PATH)

class Config:
    SECRET_KEY = "minha_chave_secreta"
    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/example.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER_PATH
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
