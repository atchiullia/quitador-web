# Criar arquivo de inicialização da aplicação
from flask import Flask
from app.interface.routes import main
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    
    app = Flask(__name__,
                template_folder='app/interface/templates',
                static_folder='app/static')
    
    app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
    app.register_blueprint(main)
    
    return app 