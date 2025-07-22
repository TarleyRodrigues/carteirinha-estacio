from flask import Blueprint, render_template, url_for, request, flash, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from app import db  
from app.models import Aluno
from app.forms import CadastroForm

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se o método for POST, significa que o usuário enviou o formulário
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        senha = request.form.get('senha')

        # Busca o aluno no banco de dados pela matrícula
        aluno = Aluno.query.filter_by(matricula=matricula).first()

        # Verifica se o aluno existe e se a senha está correta
        if aluno and check_password_hash(aluno.senha_hash, senha):
            # Se tudo estiver certo, armazena o id do aluno na sessão
            session['aluno_id'] = aluno.id
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.menu')) # Redireciona para o menu
        else:
            # Se algo estiver errado, exibe uma mensagem de erro
            flash('Matrícula ou senha inválida. Tente novamente.', 'danger')

    # Se o método for GET (primeiro acesso à página), apenas renderiza o template
    return render_template('login.html', title='Login')


@bp.route('/menu')
def menu():
    # Verifica se o usuário está logado antes de mostrar o menu
    if 'aluno_id' not in session:
        flash('Você precisa fazer login para acessar esta página.', 'warning')
        return redirect(url_for('main.login'))
    
    # Busca o aluno logado no banco de dados
    aluno_logado = Aluno.query.get(session['aluno_id'])
    if not aluno_logado:
        # Se o usuário foi deletado por algum motivo, limpa a sessão
        session.pop('aluno_id', None)
        return redirect(url_for('main.login'))

    # Envia o objeto 'aluno' para o template do menu
    return render_template('menu.html', title='Menu Principal', aluno=aluno_logado)

@bp.route('/carteirinha')
def carteirinha():
    if 'aluno_id' not in session:
        return redirect(url_for('main.login'))
    
    # Busca o aluno logado no banco de dados usando o id da sessão
    aluno_logado = Aluno.query.get(session['aluno_id'])
    
    return render_template('carteirinha.html', title='Carteirinha Estudantil', aluno=aluno_logado)

# em app/routes.py

@bp.route('/admin/cadastro', methods=['GET', 'POST'])
def cadastro_estudante():
    # 1. Proteger a rota: verificar se o usuário está logado E se é admin
    if 'aluno_id' not in session:
        flash('Acesso negado. Faça login para continuar.', 'warning')
        return redirect(url_for('main.login'))

    user_logado = Aluno.query.get(session['aluno_id'])
    if not user_logado.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('main.menu'))

    # 2. Lógica do formulário
    form = CadastroForm()
    if form.validate_on_submit():
        # Se o formulário for válido, cria e salva o novo aluno
        senha_hashed = generate_password_hash(form.senha.data, method='pbkdf2:sha256')
        novo_aluno = Aluno(
            nome=form.nome.data,
            cpf=form.cpf.data,
            data_nascimento=form.data_nascimento.data,
            matricula=form.matricula.data,
            senha_hash=senha_hashed
        )
        db.session.add(novo_aluno)
        db.session.commit()
        flash(f'Aluno {form.nome.data} cadastrado com sucesso!', 'success')
        return redirect(url_for('main.menu'))

    # 3. Se for um acesso GET, apenas exibe a página com o formulário
    return render_template('admin/cadastro_estudante.html', title='Cadastro de Estudante', form=form)

@bp.route('/perfil')
def perfil():
    # 1. Proteção: Garante que apenas usuários logados acessem
    if 'aluno_id' not in session:
        flash('Você precisa fazer login para acessar esta página.', 'warning')
        return redirect(url_for('main.login'))

    # 2. Busca os dados do aluno logado no banco de dados
    aluno_logado = Aluno.query.get(session['aluno_id'])

    # 3. Renderiza o novo template 'perfil.html', enviando os dados do aluno
    return render_template('perfil.html', title='Meu Perfil', aluno=aluno_logado)


@bp.route('/logout')
def logout():
    # Remove o id do aluno da sessão para fazer logout
    session.pop('aluno_id', None)
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('main.login'))