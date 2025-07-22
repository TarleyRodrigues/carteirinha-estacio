from app import db  # Importa a instância do BD


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128))  # Nunca guarde a senha em texto!
    is_admin = db.Column(db.Boolean, default=False)
    foto_url = db.Column(db.String(255))
    # Adicione outros campos se necessário

    def __repr__(self):
        return f"Aluno('{self.nome}', '{self.matricula}')"
