# em app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class CadastroForm(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=14, max=14)])
    data_nascimento = StringField('Data de Nascimento (DD/MM/AAAA)', validators=[DataRequired()])
    matricula = StringField('Matrícula', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Cadastrar Aluno')