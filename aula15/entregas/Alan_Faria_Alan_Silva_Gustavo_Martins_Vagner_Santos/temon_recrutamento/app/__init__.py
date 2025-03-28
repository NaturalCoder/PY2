from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

# Cria a instância global do SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa o SQLAlchemy com o app
    db.init_app(app)

    # Importa e registra as rotas (Blueprint)
    from app.routes import app as app_blueprint
    app.register_blueprint(app_blueprint)

    return app