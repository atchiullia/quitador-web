from flask import Flask
from flask_session import Session
from redis import Redis, ConnectionError
import os

def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.pardir, "static")
    )
    
    # Carrega variáveis do ambiente
    app.config.from_prefixed_env()

    # Sessão Redis com tratamento de erro
    try:
        redis_host = os.getenv("REDIS_HOST", "redis")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_conn = Redis(host=redis_host, port=redis_port)
        redis_conn.ping()  # Teste de conexão

        app.config['SESSION_TYPE'] = "redis"
        app.config['SESSION_REDIS'] = redis_conn

    except ConnectionError as e:
        print(f"[ERRO] Falha ao conectar ao Redis ({redis_host}:{redis_port}): {e}")
        app.config['SESSION_TYPE'] = "filesystem"

    # Inicializa a sessão
    Session(app)

    # Registra blueprint
    from .routes import main
    app.register_blueprint(main)

    return app
