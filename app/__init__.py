from app.routes import bp
from flask import Flask

# Cria a instância da aplicação principal
app = Flask(__name__)

# Importa o blueprint do nosso arquivo de rotas

# Registra o blueprint na aplicação. Agora a 'app' conhece todas as rotas de 'bp'.
app.register_blueprint(bp)
