"""
Módulo de clientes do ERP ROMA
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.cliente import Cliente
from app.forms import ClienteForm

# Criação do Blueprint
clientes = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientes.route('/')
@login_required
def index():
    """Lista todos os clientes."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    status = request.args.get('status', 'todos', type=str)
    
    query = Cliente.query
    
    if search:
        query = query.filter(
            Cliente.nome.contains(search) | 
            Cliente.cnpj.contains(search) |
            Cliente.email.contains(search)
        )
    
    if status == 'ativo':
        query = query.filter_by(ativo=True)
    elif status == 'inativo':
        query = query.filter_by(ativo=False)
    
    clientes_paginados = query.order_by(Cliente.nome).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('clientes/index.html', 
                         clientes=clientes_paginados,
                         search=search,
                         status=status)

@clientes.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    """Cria um novo cliente."""
    form = ClienteForm()
    
    if form.validate_on_submit():
        cliente = Cliente(
            nome=form.nome.data,
            cnpj=form.cnpj.data,
            inscricao_estadual=form.inscricao_estadual.data,
            email=form.email.data,
            telefone=form.telefone.data,
            contato=form.contato.data,
            cep=form.cep.data,
            logradouro=form.logradouro.data,
            numero=form.numero.data,
            complemento=form.complemento.data,
            bairro=form.bairro.data,
            cidade=form.cidade.data,
            estado=form.estado.data,
            observacoes=form.observacoes.data,
            ativo=form.ativo.data
        )
        
        db.session.add(cliente)
        db.session.commit()
        
        flash(f'Cliente {cliente.nome} criado com sucesso!', 'success')
        return redirect(url_for('clientes.view', id=cliente.id))
    
    return render_template('clientes/form.html', form=form, title='Novo Cliente')

@clientes.route('/<int:id>')
@login_required
def view(id):
    """Visualiza um cliente específico."""
    cliente = Cliente.query.get_or_404(id)
    
    # Busca estatísticas do cliente
    from app.models.pedido import Pedido
    from app.models.producao import Producao
    from sqlalchemy import func
    
    stats = {}
    stats['total_pedidos'] = Pedido.query.filter_by(cliente_id=id).count()
    stats['total_producoes'] = Producao.query.filter_by(cliente_id=id).count()
    
    # Últimos pedidos
    ultimos_pedidos = Pedido.query.filter_by(cliente_id=id).order_by(Pedido.data_pedido.desc()).limit(5).all()
    
    # Últimas produções
    ultimas_producoes = Producao.query.filter_by(cliente_id=id).order_by(Producao.data.desc()).limit(5).all()
    
    return render_template('clientes/view.html', 
                         cliente=cliente,
                         stats=stats,
                         ultimos_pedidos=ultimos_pedidos,
                         ultimas_producoes=ultimas_producoes)

@clientes.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Edita um cliente existente."""
    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm(cliente=cliente, obj=cliente)
    
    if form.validate_on_submit():
        cliente.nome = form.nome.data
        cliente.cnpj = form.cnpj.data
        cliente.inscricao_estadual = form.inscricao_estadual.data
        cliente.email = form.email.data
        cliente.telefone = form.telefone.data
        cliente.contato = form.contato.data
        cliente.cep = form.cep.data
        cliente.logradouro = form.logradouro.data
        cliente.numero = form.numero.data
        cliente.complemento = form.complemento.data
        cliente.bairro = form.bairro.data
        cliente.cidade = form.cidade.data
        cliente.estado = form.estado.data
        cliente.observacoes = form.observacoes.data
        cliente.ativo = form.ativo.data
        
        db.session.commit()
        
        flash(f'Cliente {cliente.nome} atualizado com sucesso!', 'success')
        return redirect(url_for('clientes.view', id=cliente.id))
    
    return render_template('clientes/form.html', form=form, cliente=cliente, title='Editar Cliente')

@clientes.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    """Exclui um cliente."""
    cliente = Cliente.query.get_or_404(id)
    
    # Verifica se o cliente tem pedidos ou produções associadas
    from app.models.pedido import Pedido
    from app.models.producao import Producao
    
    if Pedido.query.filter_by(cliente_id=id).first() or Producao.query.filter_by(cliente_id=id).first():
        flash('Não é possível excluir este cliente pois ele possui pedidos ou produções associadas.', 'danger')
        return redirect(url_for('clientes.view', id=id))
    
    nome = cliente.nome
    db.session.delete(cliente)
    db.session.commit()
    
    flash(f'Cliente {nome} excluído com sucesso!', 'success')
    return redirect(url_for('clientes.index'))

@clientes.route('/<int:id>/toggle-status', methods=['POST'])
@login_required
def toggle_status(id):
    """Ativa/desativa um cliente."""
    cliente = Cliente.query.get_or_404(id)
    
    cliente.ativo = not cliente.ativo
    db.session.commit()
    
    status = 'ativado' if cliente.ativo else 'desativado'
    return jsonify({'success': True, 'message': f'Cliente {status} com sucesso!', 'ativo': cliente.ativo})

@clientes.route('/api/buscar')
@login_required
def api_buscar():
    """API para buscar clientes (usado em selects)."""
    term = request.args.get('term', '')
    
    clientes = Cliente.query.filter(
        Cliente.ativo == True,
        Cliente.nome.contains(term)
    ).limit(10).all()
    
    results = []
    for cliente in clientes:
        results.append({
            'id': cliente.id,
            'text': cliente.nome,
            'cnpj': cliente.cnpj
        })
    
    return jsonify(results)

