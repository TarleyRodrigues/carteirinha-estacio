# app/__init__.py
from app.routes import bp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # Adicionar import

app = Flask(__name__)
# Adicionar configuração do BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Necessário para sessões e formulários
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil'

db = SQLAlchemy(app)  # Inicializar o BD

app.register_blueprint(bp)
