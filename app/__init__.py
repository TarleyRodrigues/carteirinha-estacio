from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil'

db = SQLAlchemy(app)

from app.routes import bp
app.register_blueprint(bp)

from app import models