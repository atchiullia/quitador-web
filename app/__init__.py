from flask import Flask
from flask_session import Session
from redis import Redis
import os

def create_app():
    app = Flask(__name__)
    
    # Carrega variáveis de ambiente com prefixo FLASK_
    app.config.from_prefixed_env()
    
    # Configuração da sessão usando Redis
    app.config['SESSION_TYPE'] = "redis"
    app.config['SESSION_REDIS'] = Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379))
    )
    
    # Inicializa o suporte a sessão
    Session(app)

    # Registra as rotas
    from .routes import main
    app.register_blueprint(main)

    return app
