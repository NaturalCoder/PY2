import os

class Config:
    SECRET_KEY = "minha_chave_secreta"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "app", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limite de 16MB
