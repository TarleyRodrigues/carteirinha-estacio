print("--- LENDO O ARQUIVO __INIT__.PY CORRETO ---")

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

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

# 6. Cria as tabelas E O ADMIN (para o Render e para a primeira execução local)
#    Isso deve vir DEPOIS de importar os modelos
with app.app_context():
    db.create_all()
    
    # --- LÓGICA DE CRIAÇÃO DO ADMIN ---
    # Isso roda toda vez que o app inicia, mas só cria se o admin não existir.
    try:
        # Pega o modelo 'Aluno' que já foi importado em 'models'
        admin_existente = models.Aluno.query.filter_by(matricula='admin').first()
        
        if not admin_existente:
            print("--- CRIANDO USUÁRIO ADMIN PADRÃO ---")
            senha_hashed = generate_password_hash('Mudar@123', method='pbkdf2:sha256')
            
            usuario_admin = models.Aluno(
                nome='Admin Render', 
                cpf='111.111.111-11', 
                data_nascimento='01/01/1990', 
                matricula='admin', 
                senha_hash=senha_hashed, 
                is_admin=True
            )
            db.session.add(usuario_admin)
            db.session.commit()
            print("--- USUÁRIO ADMIN CRIADO ---")
        else:
            print("--- USUÁRIO ADMIN JÁ EXISTE ---")
            
    except Exception as e:
        # Se o banco ainda não estiver pronto, pode dar um erro.
        # Em um app de produção maior, usaríamos 'flask db upgrade'
        print(f"AVISO: Erro ao tentar criar admin (pode ser normal na primeira migração): {e}")
