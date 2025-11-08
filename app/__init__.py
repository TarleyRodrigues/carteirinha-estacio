print("--- LENDO O ARQUIVO __INIT__.PY CORRETO ---")

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 1. Cria a instância do app PRIMEIRO
app = Flask(__name__) 

# 2. Configura o app (lendo variáveis de ambiente)
db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///../instance/site.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'uma-chave-secreta-muito-dificil')

# 3. Cria a instância do DB (ligada ao app)
db = SQLAlchemy(app) 

# --- SÓ AGORA QUE PODE IMPORTAR ---
# 4. Importa os modelos e rotas (DEPOIS que 'db' e 'app' existem)
#    Isso permite que 'models.py' e 'routes.py' façam "from app import db"
from app import models
from app.routes import bp 

# 5. Registra as rotas no app
app.register_blueprint(bp)

# 6. Cria as tabelas (para o Render e para a primeira execução local)
#    Isso deve vir DEPOIS de importar os modelos
with app.app_context():
    db.create_all()
