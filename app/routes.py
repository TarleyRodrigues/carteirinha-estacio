# Importações de bibliotecas padrão e de terceiros
import os
from flask import Blueprint, render_template, url_for, request, flash, redirect, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# Importações locais da nossa aplicação
from app import db
from app.models import Aluno
from app.forms import (
    CadastroForm, 
    EditarPerfilForm, 
    AlterarSenhaForm, 
    FotoPerfilForm,
    LogoUploadForm
)



bp = Blueprint('main', __name__)

# Rota de Login
@bp.route('/')
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        senha = request.form.get('senha')
        aluno = Aluno.query.filter_by(matricula=matricula).first()

        if aluno and check_password_hash(aluno.senha_hash, senha):
            session['aluno_id'] = aluno.id
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.menu'))
        else:
            flash('Matrícula ou senha inválida. Tente novamente.', 'danger')
    return render_template('login.html', title='Login')

# Rota do Menu Principal
@bp.route('/menu')
def menu():
    if 'aluno_id' not in session:
        flash('Você precisa fazer login para acessar esta página.', 'warning')
        return redirect(url_for('main.login'))
    
    aluno_logado = Aluno.query.get(session['aluno_id'])
    if not aluno_logado:
        session.pop('aluno_id', None)
        return redirect(url_for('main.login'))

    return render_template('menu.html', title='Menu Principal', aluno=aluno_logado)

# Rota da Carteirinha Estudantil
@bp.route('/carteirinha')
def carteirinha():
    if 'aluno_id' not in session:
        return redirect(url_for('main.login'))
    
    aluno_logado = Aluno.query.get(session['aluno_id'])
    return render_template('carteirinha.html', title='Carteirinha Estudantil', aluno=aluno_logado)

# Rota para ver o Perfil
@bp.route('/perfil')
def perfil():
    if 'aluno_id' not in session:
        flash('Você precisa fazer login para acessar esta página.', 'warning')
        return redirect(url_for('main.login'))

    aluno_logado = Aluno.query.get(session['aluno_id'])
    return render_template('perfil.html', title='Meu Perfil', aluno=aluno_logado)

# Rota para Editar o Perfil
@bp.route('/perfil/editar', methods=['GET', 'POST'])
def editar_perfil():
    if 'aluno_id' not in session:
        return redirect(url_for('main.login'))

    aluno = Aluno.query.get_or_404(session['aluno_id'])
    form = EditarPerfilForm()

    if form.validate_on_submit():
        aluno.nome = form.nome.data
        aluno.cpf = form.cpf.data
        aluno.data_nascimento = form.data_nascimento.data
        db.session.commit()
        flash('Seu perfil foi atualizado com sucesso!', 'success')
        return redirect(url_for('main.perfil'))

    elif request.method == 'GET':
        form.nome.data = aluno.nome
        form.cpf.data = aluno.cpf
        form.data_nascimento.data = aluno.data_nascimento

    return render_template('editar_perfil.html', title='Editar Perfil', form=form)

# Rota para Alterar a Senha
@bp.route('/perfil/alterar-senha', methods=['GET', 'POST'])
def alterar_senha():
    if 'aluno_id' not in session:
        return redirect(url_for('main.login'))

    aluno = Aluno.query.get_or_404(session['aluno_id'])
    form = AlterarSenhaForm()

    if form.validate_on_submit():
        if check_password_hash(aluno.senha_hash, form.senha_atual.data):
            nova_senha_hashed = generate_password_hash(form.nova_senha.data, method='pbkdf2:sha256')
            aluno.senha_hash = nova_senha_hashed
            db.session.commit()
            flash('Sua senha foi alterada com sucesso!', 'success')
            return redirect(url_for('main.perfil'))
        else:
            flash('A senha atual está incorreta. Tente novamente.', 'danger')
    
    return render_template('alterar_senha.html', title='Alterar Senha', form=form)

# Rota para Upload da Foto de Perfil
@bp.route('/perfil/upload-foto', methods=['GET', 'POST'])
def upload_foto_perfil():
    if 'aluno_id' not in session:
        return redirect(url_for('main.login'))

    aluno = Aluno.query.get_or_404(session['aluno_id'])
    form = FotoPerfilForm()

    if form.validate_on_submit():
        foto = form.foto.data
        nome_seguro = secure_filename(f"{aluno.id}_{foto.filename}")
        caminho_base = os.path.join(current_app.root_path, 'static', 'uploads')
        
        os.makedirs(caminho_base, exist_ok=True) # Garante que a pasta exista
        
        caminho_foto = os.path.join(caminho_base, nome_seguro)
        foto.save(caminho_foto)
        
        aluno.foto_url = f"/static/uploads/{nome_seguro}" # Salva o caminho relativo no banco
        db.session.commit()
        
        flash('Sua foto de perfil foi atualizada!', 'success')
        return redirect(url_for('main.perfil'))

    return render_template('upload_foto_perfil.html', title='Enviar Foto de Perfil', form=form)

# Rota de Cadastro de Estudante (Admin)
@bp.route('/admin/cadastro', methods=['GET', 'POST'])
def cadastro_estudante():
    if 'aluno_id' not in session:
        return redirect(url_for('main.login'))

    user_logado = Aluno.query.get(session['aluno_id'])
    if not user_logado or not user_logado.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('main.menu'))

    form = CadastroForm()
    if form.validate_on_submit():
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

    return render_template('admin/cadastro_estudante.html', title='Cadastro de Estudante', form=form)

# em app/routes.py

@bp.route('/admin/upload-logo', methods=['GET', 'POST'])
def upload_logo():
    # Proteção: Garante que apenas o admin acesse
    if 'aluno_id' not in session:
        return redirect(url_for('main.login'))
    user_logado = Aluno.query.get(session['aluno_id'])
    if not user_logado or not user_logado.is_admin:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('main.menu'))

    form = LogoUploadForm()
    if form.validate_on_submit():
        logo_file = form.logo.data
        # Usamos um nome de arquivo FIXO
        filename = 'logo_faculdade.png'
        save_path = os.path.join(current_app.root_path, 'static', 'img', filename)

        # Salva o novo logo, substituindo o antigo se existir
        logo_file.save(save_path)

        flash('Logo da faculdade atualizado com sucesso!', 'success')
        return redirect(url_for('main.menu'))

    return render_template('admin/upload_logo.html', title='Alterar Logo da Faculdade', form=form)

# Rota de Logout
@bp.route('/logout')
def logout():
    session.pop('aluno_id', None)
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('main.login'))

# Rota para configurar o banco de dados (apenas para uso inicial)

@bp.route('/setup-database/a-very-long-and-random-secret-key-12345')
def setup_database():
    try:
        # Comando 1: Criar todas as tabelas
        db.create_all()

        # Comando 2: Criar o usuário admin, mas só se ele não existir
        admin_existente = Aluno.query.filter_by(matricula='admin').first()
        if not admin_existente:
            senha_hashed = generate_password_hash('senha_super_segura', method='pbkdf2:sha256')
            usuario_admin = Aluno(
                nome='Admin Render', 
                cpf='111.111.111-11', 
                data_nascimento='01/01/1990', 
                matricula='admin', 
                senha_hash=senha_hashed, 
                is_admin=True
            )
            db.session.add(usuario_admin)
            db.session.commit()
            return "Banco de dados e usuário admin criados com sucesso!"

        return "Banco de dados verificado. Admin já existe."

    except Exception as e:
        return f"Ocorreu um erro: {str(e)}"

# ... (sua rota de logout aqui)