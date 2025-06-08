"""
Módulo de usuários do ERP ROMA
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.usuario import Usuario
from app.forms import UsuarioForm
from functools import wraps

# Criação do Blueprint
usuarios = Blueprint('usuarios', __name__, url_prefix='/usuarios')

def admin_required(f):
    """Decorator para verificar se o usuário é administrador."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo != 'administrador':
            flash('Acesso negado. Apenas administradores podem acessar esta página.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@usuarios.route('/')
@login_required
@admin_required
def index():
    """Lista todos os usuários."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Usuario.query
    
    if search:
        query = query.filter(
            Usuario.nome.contains(search) | 
            Usuario.email.contains(search)
        )
    
    usuarios_paginados = query.order_by(Usuario.nome).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('usuarios/index.html', 
                         usuarios=usuarios_paginados,
                         search=search)

@usuarios.route('/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo():
    """Cria um novo usuário."""
    form = UsuarioForm()
    
    if form.validate_on_submit():
        usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            senha=form.senha.data,
            tipo=form.tipo.data,
            ativo=form.ativo.data
        )
        
        db.session.add(usuario)
        db.session.commit()
        
        flash(f'Usuário {usuario.nome} criado com sucesso!', 'success')
        return redirect(url_for('usuarios.index'))
    
    return render_template('usuarios/form.html', form=form, title='Novo Usuário')

@usuarios.route('/<int:id>')
@login_required
@admin_required
def view(id):
    """Visualiza um usuário específico."""
    usuario = Usuario.query.get_or_404(id)
    return render_template('usuarios/view.html', usuario=usuario)

@usuarios.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    """Edita um usuário existente."""
    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(usuario=usuario, obj=usuario)
    
    if form.validate_on_submit():
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        usuario.tipo = form.tipo.data
        usuario.ativo = form.ativo.data
        
        # Só atualiza a senha se foi fornecida
        if form.senha.data:
            usuario.senha = form.senha.data
        
        db.session.commit()
        
        flash(f'Usuário {usuario.nome} atualizado com sucesso!', 'success')
        return redirect(url_for('usuarios.view', id=usuario.id))
    
    return render_template('usuarios/form.html', form=form, usuario=usuario, title='Editar Usuário')

@usuarios.route('/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir(id):
    """Exclui um usuário."""
    usuario = Usuario.query.get_or_404(id)
    
    # Não permite excluir o próprio usuário
    if usuario.id == current_user.id:
        flash('Você não pode excluir sua própria conta.', 'danger')
        return redirect(url_for('usuarios.index'))
    
    # Não permite excluir se for o último administrador
    if usuario.tipo == 'administrador':
        admin_count = Usuario.query.filter_by(tipo='administrador', ativo=True).count()
        if admin_count <= 1:
            flash('Não é possível excluir o último administrador do sistema.', 'danger')
            return redirect(url_for('usuarios.index'))
    
    nome = usuario.nome
    db.session.delete(usuario)
    db.session.commit()
    
    flash(f'Usuário {nome} excluído com sucesso!', 'success')
    return redirect(url_for('usuarios.index'))

@usuarios.route('/<int:id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_status(id):
    """Ativa/desativa um usuário."""
    usuario = Usuario.query.get_or_404(id)
    
    # Não permite desativar o próprio usuário
    if usuario.id == current_user.id:
        return jsonify({'success': False, 'message': 'Você não pode desativar sua própria conta.'})
    
    # Não permite desativar se for o último administrador ativo
    if usuario.tipo == 'administrador' and usuario.ativo:
        admin_count = Usuario.query.filter_by(tipo='administrador', ativo=True).count()
        if admin_count <= 1:
            return jsonify({'success': False, 'message': 'Não é possível desativar o último administrador ativo.'})
    
    usuario.ativo = not usuario.ativo
    db.session.commit()
    
    status = 'ativado' if usuario.ativo else 'desativado'
    return jsonify({'success': True, 'message': f'Usuário {status} com sucesso!', 'ativo': usuario.ativo})

