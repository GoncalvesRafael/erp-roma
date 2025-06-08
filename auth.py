"""
Módulo de autenticação do ERP ROMA
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.usuario import Usuario
from app.forms import LoginForm, AlterarSenhaForm
from werkzeug.security import check_password_hash

# Criação do Blueprint
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Rota para login de usuários."""
    # Se o usuário já estiver autenticado, redireciona para o dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Busca o usuário pelo e-mail
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        
        # Verifica se o usuário existe e se a senha está correta
        if usuario and usuario.verificar_senha(form.senha.data):
            # Verifica se o usuário está ativo
            if not usuario.ativo:
                flash('Sua conta está desativada. Entre em contato com o administrador.', 'danger')
                return render_template('auth/login.html', form=form)
            
            # Realiza o login
            login_user(usuario, remember=form.lembrar_me.data)
            
            # Redireciona para a página solicitada ou para o dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            flash('E-mail ou senha inválidos.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """Rota para logout de usuários."""
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/alterar-senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    """Rota para alterar a senha do usuário."""
    form = AlterarSenhaForm()
    if form.validate_on_submit():
        # Verifica se a senha atual está correta
        if current_user.verificar_senha(form.senha_atual.data):
            # Atualiza a senha
            current_user.senha = form.nova_senha.data
            db.session.commit()
            flash('Sua senha foi alterada com sucesso.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Senha atual incorreta.', 'danger')
    
    return render_template('auth/alterar_senha.html', form=form)

