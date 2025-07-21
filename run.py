from flask import Flask
from app.interface.routes import main
import os
from dotenv import load_dotenv

load_dotenv()

# Verificar se os diretórios existem
template_dir = os.path.join(os.path.dirname(__file__), 'app', 'interface', 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'app', 'static')

app = Flask(__name__, 
           template_folder=template_dir,
           static_folder=static_dir)

app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
