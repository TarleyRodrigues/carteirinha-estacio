from flask import Blueprint, render_template, url_for

# 1. Crie uma instância de Blueprint
# O primeiro argumento 'main' é o nome do blueprint.
# O segundo, __name__, ajuda o Flask a localizar a pasta de templates.
bp = Blueprint('main', __name__)

# 2. Troque todos os decoradores @app.route por @bp.route


@bp.route('/')
@bp.route('/login')
def login():
    return render_template('login.html', title='Login')


@bp.route('/menu')
def menu():
    return render_template('menu.html', title='Menu Principal')


@bp.route('/carteirinha')
def carteirinha():
    aluno = {
        'nome': 'Tarley Divino da Silva',
        'cpf': '123.456.789-00',
        'data_nascimento': '01/01/2002',
        'matricula': '202507220001',
        'validade': '31/12/2025',
        'foto_url': url_for('static', filename='img/placeholder-foto.png')
    }
    return render_template('carteirinha.html', title='Carteirinha Estudantil', aluno=aluno)
