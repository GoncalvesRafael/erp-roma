"""
Módulo de fornecedores do ERP ROMA
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.fornecedor import Fornecedor
from app.forms import FornecedorForm

# Criação do Blueprint
fornecedores = Blueprint('fornecedores', __name__, url_prefix='/fornecedores')

@fornecedores.route('/')
@login_required
def index():
    """Lista todos os fornecedores."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    status = request.args.get('status', 'todos', type=str)
    
    query = Fornecedor.query
    
    if search:
        query = query.filter(
            Fornecedor.nome.contains(search) | 
            Fornecedor.cnpj.contains(search) |
            Fornecedor.email.contains(search)
        )
    
    if status == 'ativo':
        query = query.filter_by(ativo=True)
    elif status == 'inativo':
        query = query.filter_by(ativo=False)
    
    fornecedores_paginados = query.order_by(Fornecedor.nome).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('fornecedores/index.html', 
                         fornecedores=fornecedores_paginados,
                         search=search,
                         status=status)

@fornecedores.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    """Cria um novo fornecedor."""
    form = FornecedorForm()
    
    if form.validate_on_submit():
        fornecedor = Fornecedor(
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
            prazo_entrega=form.prazo_entrega.data,
            forma_pagamento=form.forma_pagamento.data,
            observacoes=form.observacoes.data,
            ativo=form.ativo.data
        )
        
        db.session.add(fornecedor)
        db.session.commit()
        
        flash(f'Fornecedor {fornecedor.nome} criado com sucesso!', 'success')
        return redirect(url_for('fornecedores.view', id=fornecedor.id))
    
    return render_template('fornecedores/form.html', form=form, title='Novo Fornecedor')

@fornecedores.route('/<int:id>')
@login_required
def view(id):
    """Visualiza um fornecedor específico."""
    fornecedor = Fornecedor.query.get_or_404(id)
    
    # Busca materiais fornecidos
    materiais = fornecedor.materiais.filter_by(ativo=True).all()
    
    return render_template('fornecedores/view.html', 
                         fornecedor=fornecedor,
                         materiais=materiais)

@fornecedores.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Edita um fornecedor existente."""
    fornecedor = Fornecedor.query.get_or_404(id)
    form = FornecedorForm(fornecedor=fornecedor, obj=fornecedor)
    
    if form.validate_on_submit():
        fornecedor.nome = form.nome.data
        fornecedor.cnpj = form.cnpj.data
        fornecedor.inscricao_estadual = form.inscricao_estadual.data
        fornecedor.email = form.email.data
        fornecedor.telefone = form.telefone.data
        fornecedor.contato = form.contato.data
        fornecedor.cep = form.cep.data
        fornecedor.logradouro = form.logradouro.data
        fornecedor.numero = form.numero.data
        fornecedor.complemento = form.complemento.data
        fornecedor.bairro = form.bairro.data
        fornecedor.cidade = form.cidade.data
        fornecedor.estado = form.estado.data
        fornecedor.prazo_entrega = form.prazo_entrega.data
        fornecedor.forma_pagamento = form.forma_pagamento.data
        fornecedor.observacoes = form.observacoes.data
        fornecedor.ativo = form.ativo.data
        
        db.session.commit()
        
        flash(f'Fornecedor {fornecedor.nome} atualizado com sucesso!', 'success')
        return redirect(url_for('fornecedores.view', id=fornecedor.id))
    
    return render_template('fornecedores/form.html', form=form, fornecedor=fornecedor, title='Editar Fornecedor')

@fornecedores.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    """Exclui um fornecedor."""
    fornecedor = Fornecedor.query.get_or_404(id)
    
    # Verifica se o fornecedor tem materiais associados
    if fornecedor.materiais.first():
        flash('Não é possível excluir este fornecedor pois ele possui materiais associados.', 'danger')
        return redirect(url_for('fornecedores.view', id=id))
    
    nome = fornecedor.nome
    db.session.delete(fornecedor)
    db.session.commit()
    
    flash(f'Fornecedor {nome} excluído com sucesso!', 'success')
    return redirect(url_for('fornecedores.index'))

@fornecedores.route('/<int:id>/toggle-status', methods=['POST'])
@login_required
def toggle_status(id):
    """Ativa/desativa um fornecedor."""
    fornecedor = Fornecedor.query.get_or_404(id)
    
    fornecedor.ativo = not fornecedor.ativo
    db.session.commit()
    
    status = 'ativado' if fornecedor.ativo else 'desativado'
    return jsonify({'success': True, 'message': f'Fornecedor {status} com sucesso!', 'ativo': fornecedor.ativo})

@fornecedores.route('/api/buscar')
@login_required
def api_buscar():
    """API para buscar fornecedores (usado em selects)."""
    term = request.args.get('term', '')
    
    fornecedores = Fornecedor.query.filter(
        Fornecedor.ativo == True,
        Fornecedor.nome.contains(term)
    ).limit(10).all()
    
    results = []
    for fornecedor in fornecedores:
        results.append({
            'id': fornecedor.id,
            'text': fornecedor.nome,
            'cnpj': fornecedor.cnpj
        })
    
    return jsonify(results)

