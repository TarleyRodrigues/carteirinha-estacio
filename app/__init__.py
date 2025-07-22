import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Lógica para a configuração
# Tenta pegar a DATABASE_URL do ambiente do Render, se não achar, usa o site.db local.
db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///../instance/site.db'

# Tenta pegar a SECRET_KEY do ambiente, se não achar, usa a nossa chave de desenvolvimento.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'uma-chave-secreta-muito-dificil')

db = SQLAlchemy(app)

# Importa e registra o blueprint DEPOIS de inicializar o app e o db
from app.routes import bp
app.register_blueprint(bp)

# Garante que os modelos sejam descobertos pela aplicação
from app import models