"""
Módulo de estoque (materiais) do ERP ROMA
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.material import Material, MovimentacaoEstoque
from app.forms import MaterialForm, MovimentacaoEstoqueForm
from datetime import datetime

# Criação do Blueprint
estoque = Blueprint('estoque', __name__, url_prefix='/estoque')

@estoque.route('/')
@login_required
def index():
    """Lista todos os materiais."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    status = request.args.get('status', 'todos', type=str)
    tipo = request.args.get('tipo', '', type=str)
    alerta = request.args.get('alerta', '', type=str)
    
    query = Material.query
    
    if search:
        query = query.filter(
            Material.nome.contains(search) | 
            Material.codigo.contains(search)
        )
    
    if status == 'ativo':
        query = query.filter_by(ativo=True)
    elif status == 'inativo':
        query = query.filter_by(ativo=False)
    
    if tipo:
        query = query.filter_by(tipo=tipo)
    
    if alerta == 'baixo':
        query = query.filter(Material.estoque_atual <= Material.estoque_minimo)
    
    materiais_paginados = query.order_by(Material.nome).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Lista de tipos para o filtro
    tipos = db.session.query(Material.tipo).filter(Material.tipo != None).distinct().all()
    tipos = [t[0] for t in tipos if t[0]]
    
    return render_template('estoque/index.html', 
                         materiais=materiais_paginados,
                         search=search,
                         status=status,
                         tipo=tipo,
                         alerta=alerta,
                         tipos=tipos)

@estoque.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    """Cria um novo material."""
    form = MaterialForm()
    
    if form.validate_on_submit():
        material = Material(
            codigo=form.codigo.data,
            nome=form.nome.data,
            tipo=form.tipo.data,
            unidade_medida=form.unidade_medida.data,
            preco_unitario=form.preco_unitario.data,
            estoque_atual=form.estoque_atual.data,
            estoque_minimo=form.estoque_minimo.data,
            fornecedor_id=form.fornecedor_id.data if form.fornecedor_id.data else None,
            descricao=form.descricao.data,
            ativo=form.ativo.data
        )
        
        db.session.add(material)
        db.session.commit()
        
        # Registra movimentação inicial se houver estoque
        if material.estoque_atual > 0:
            movimentacao = MovimentacaoEstoque(
                material_id=material.id,
                tipo='entrada',
                quantidade=material.estoque_atual,
                motivo='Estoque inicial',
                usuario_id=current_user.id
            )
            db.session.add(movimentacao)
            db.session.commit()
        
        flash(f'Material {material.nome} criado com sucesso!', 'success')
        return redirect(url_for('estoque.view', id=material.id))
    
    return render_template('estoque/form.html', form=form, title='Novo Material')

@estoque.route('/<int:id>')
@login_required
def view(id):
    """Visualiza um material específico."""
    material = Material.query.get_or_404(id)
    
    # Busca últimas movimentações
    movimentacoes = MovimentacaoEstoque.query.filter_by(material_id=id).order_by(
        MovimentacaoEstoque.data.desc()
    ).limit(10).all()
    
    # Busca produtos que usam este material
    from app.models.produto import ComposicaoProduto
    produtos = db.session.query(ComposicaoProduto).filter_by(material_id=id).all()
    
    return render_template('estoque/view.html', 
                         material=material,
                         movimentacoes=movimentacoes,
                         produtos=produtos)

@estoque.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Edita um material existente."""
    material = Material.query.get_or_404(id)
    form = MaterialForm(material=material, obj=material)
    
    if form.validate_on_submit():
        material.codigo = form.codigo.data
        material.nome = form.nome.data
        material.tipo = form.tipo.data
        material.unidade_medida = form.unidade_medida.data
        material.preco_unitario = form.preco_unitario.data
        material.estoque_minimo = form.estoque_minimo.data
        material.fornecedor_id = form.fornecedor_id.data if form.fornecedor_id.data else None
        material.descricao = form.descricao.data
        material.ativo = form.ativo.data
        
        db.session.commit()
        
        flash(f'Material {material.nome} atualizado com sucesso!', 'success')
        return redirect(url_for('estoque.view', id=material.id))
    
    return render_template('estoque/form.html', form=form, material=material, title='Editar Material')

@estoque.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    """Exclui um material."""
    material = Material.query.get_or_404(id)
    
    # Verifica se o material tem movimentações ou está em composições
    if material.movimentacoes.first():
        flash('Não é possível excluir este material pois ele possui movimentações de estoque.', 'danger')
        return redirect(url_for('estoque.view', id=id))
    
    from app.models.produto import ComposicaoProduto
    if ComposicaoProduto.query.filter_by(material_id=id).first():
        flash('Não é possível excluir este material pois ele está sendo usado em produtos.', 'danger')
        return redirect(url_for('estoque.view', id=id))
    
    nome = material.nome
    db.session.delete(material)
    db.session.commit()
    
    flash(f'Material {nome} excluído com sucesso!', 'success')
    return redirect(url_for('estoque.index'))

@estoque.route('/<int:id>/toggle-status', methods=['POST'])
@login_required
def toggle_status(id):
    """Ativa/desativa um material."""
    material = Material.query.get_or_404(id)
    
    material.ativo = not material.ativo
    db.session.commit()
    
    status = 'ativado' if material.ativo else 'desativado'
    return jsonify({'success': True, 'message': f'Material {status} com sucesso!', 'ativo': material.ativo})

@estoque.route('/movimentacoes')
@login_required
def movimentacoes():
    """Lista todas as movimentações de estoque."""
    page = request.args.get('page', 1, type=int)
    material_id = request.args.get('material_id', '', type=str)
    tipo = request.args.get('tipo', '', type=str)
    
    query = MovimentacaoEstoque.query
    
    if material_id:
        query = query.filter_by(material_id=int(material_id))
    
    if tipo:
        query = query.filter_by(tipo=tipo)
    
    movimentacoes_paginadas = query.order_by(MovimentacaoEstoque.data.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Lista de materiais para o filtro
    materiais = Material.query.filter_by(ativo=True).order_by(Material.nome).all()
    
    return render_template('estoque/movimentacoes.html', 
                         movimentacoes=movimentacoes_paginadas,
                         materiais=materiais,
                         material_id=material_id,
                         tipo=tipo)

@estoque.route('/movimentacao/nova', methods=['GET', 'POST'])
@login_required
def nova_movimentacao():
    """Cria uma nova movimentação de estoque."""
    form = MovimentacaoEstoqueForm()
    
    if form.validate_on_submit():
        material = Material.query.get(form.material_id.data)
        
        # Verifica se há estoque suficiente para saída
        if form.tipo.data == 'saida' and material.estoque_atual < form.quantidade.data:
            flash(f'Estoque insuficiente. Disponível: {material.estoque_atual} {material.unidade_medida}', 'danger')
            return render_template('estoque/movimentacao_form.html', form=form, title='Nova Movimentação')
        
        movimentacao = MovimentacaoEstoque(
            material_id=form.material_id.data,
            tipo=form.tipo.data,
            quantidade=form.quantidade.data,
            motivo=form.motivo.data,
            observacoes=form.observacoes.data,
            usuario_id=current_user.id
        )
        
        db.session.add(movimentacao)
        
        # Atualiza o estoque do material
        material.atualizar_estoque(form.quantidade.data, form.tipo.data, form.motivo.data)
        
        db.session.commit()
        
        flash(f'Movimentação de estoque registrada com sucesso!', 'success')
        return redirect(url_for('estoque.view', id=material.id))
    
    return render_template('estoque/movimentacao_form.html', form=form, title='Nova Movimentação')

@estoque.route('/api/buscar')
@login_required
def api_buscar():
    """API para buscar materiais (usado em selects)."""
    term = request.args.get('term', '')
    
    materiais = Material.query.filter(
        Material.ativo == True,
        Material.nome.contains(term) | Material.codigo.contains(term)
    ).limit(10).all()
    
    results = []
    for material in materiais:
        results.append({
            'id': material.id,
            'text': f'{material.codigo} - {material.nome}',
            'preco': float(material.preco_unitario) if material.preco_unitario else 0,
            'estoque': float(material.estoque_atual),
            'unidade': material.unidade_medida
        })
    
    return jsonify(results)

@estoque.route('/alertas')
@login_required
def alertas():
    """Página de alertas de estoque baixo."""
    materiais_baixo_estoque = Material.query.filter(
        Material.ativo == True,
        Material.estoque_atual <= Material.estoque_minimo
    ).order_by(Material.nome).all()
    
    return render_template('estoque/alertas.html', materiais=materiais_baixo_estoque)

