"""
Módulo de produtos do ERP ROMA
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.produto import Produto, ComposicaoProduto
from app.models.material import Material
from app.forms import ProdutoForm
from sqlalchemy import func

# Criação do Blueprint
produtos = Blueprint('produtos', __name__, url_prefix='/produtos')

@produtos.route('/')
@login_required
def index():
    """Lista todos os produtos."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    status = request.args.get('status', 'todos', type=str)
    categoria = request.args.get('categoria', '', type=str)
    
    query = Produto.query
    
    if search:
        query = query.filter(
            Produto.nome.contains(search) | 
            Produto.codigo.contains(search) |
            Produto.modelo.contains(search)
        )
    
    if status == 'ativo':
        query = query.filter_by(ativo=True)
    elif status == 'inativo':
        query = query.filter_by(ativo=False)
    
    if categoria:
        query = query.filter_by(categoria=categoria)
    
    produtos_paginados = query.order_by(Produto.nome).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Lista de categorias para o filtro
    categorias = db.session.query(Produto.categoria).filter(Produto.categoria != None).distinct().all()
    categorias = [c[0] for c in categorias if c[0]]
    
    return render_template('produtos/index.html', 
                         produtos=produtos_paginados,
                         search=search,
                         status=status,
                         categoria=categoria,
                         categorias=categorias)

@produtos.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    """Cria um novo produto."""
    form = ProdutoForm()
    
    if form.validate_on_submit():
        produto = Produto(
            codigo=form.codigo.data,
            nome=form.nome.data,
            modelo=form.modelo.data,
            descricao=form.descricao.data,
            custo_unitario=form.custo_unitario.data,
            preco_minimo=form.preco_minimo.data,
            preco_sugerido=form.preco_sugerido.data,
            estoque_atual=form.estoque_atual.data,
            estoque_minimo=form.estoque_minimo.data,
            unidade_medida=form.unidade_medida.data,
            categoria=form.categoria.data,
            ativo=form.ativo.data
        )
        
        db.session.add(produto)
        db.session.commit()
        
        flash(f'Produto {produto.nome} criado com sucesso!', 'success')
        return redirect(url_for('produtos.view', id=produto.id))
    
    return render_template('produtos/form.html', form=form, title='Novo Produto')

@produtos.route('/<int:id>')
@login_required
def view(id):
    """Visualiza um produto específico."""
    produto = Produto.query.get_or_404(id)
    
    # Busca composição do produto
    composicao = ComposicaoProduto.query.filter_by(produto_id=id).all()
    
    # Busca estatísticas do produto
    from app.models.producao import ItemProducao
    from app.models.pedido import ItemPedido
    
    stats = {}
    stats['total_producoes'] = db.session.query(func.count(ItemProducao.id)).filter_by(produto_id=id).scalar() or 0
    stats['total_pedidos'] = db.session.query(func.count(ItemPedido.id)).filter_by(produto_id=id).scalar() or 0
    
    # Últimas produções
    ultimas_producoes = db.session.query(ItemProducao).filter_by(produto_id=id).order_by(ItemProducao.id.desc()).limit(5).all()
    
    # Materiais disponíveis para composição
    materiais = Material.query.filter_by(ativo=True).order_by(Material.nome).all()
    
    return render_template('produtos/view.html', 
                         produto=produto,
                         composicao=composicao,
                         stats=stats,
                         ultimas_producoes=ultimas_producoes,
                         materiais=materiais)

@produtos.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Edita um produto existente."""
    produto = Produto.query.get_or_404(id)
    form = ProdutoForm(produto=produto, obj=produto)
    
    if form.validate_on_submit():
        produto.codigo = form.codigo.data
        produto.nome = form.nome.data
        produto.modelo = form.modelo.data
        produto.descricao = form.descricao.data
        produto.custo_unitario = form.custo_unitario.data
        produto.preco_minimo = form.preco_minimo.data
        produto.preco_sugerido = form.preco_sugerido.data
        produto.estoque_atual = form.estoque_atual.data
        produto.estoque_minimo = form.estoque_minimo.data
        produto.unidade_medida = form.unidade_medida.data
        produto.categoria = form.categoria.data
        produto.ativo = form.ativo.data
        
        db.session.commit()
        
        flash(f'Produto {produto.nome} atualizado com sucesso!', 'success')
        return redirect(url_for('produtos.view', id=produto.id))
    
    return render_template('produtos/form.html', form=form, produto=produto, title='Editar Produto')

@produtos.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    """Exclui um produto."""
    produto = Produto.query.get_or_404(id)
    
    # Verifica se o produto tem itens de produção ou pedidos associados
    from app.models.producao import ItemProducao
    from app.models.pedido import ItemPedido
    
    if ItemProducao.query.filter_by(produto_id=id).first() or ItemPedido.query.filter_by(produto_id=id).first():
        flash('Não é possível excluir este produto pois ele possui produções ou pedidos associados.', 'danger')
        return redirect(url_for('produtos.view', id=id))
    
    nome = produto.nome
    
    # Remove a composição do produto
    ComposicaoProduto.query.filter_by(produto_id=id).delete()
    
    db.session.delete(produto)
    db.session.commit()
    
    flash(f'Produto {nome} excluído com sucesso!', 'success')
    return redirect(url_for('produtos.index'))

@produtos.route('/<int:id>/toggle-status', methods=['POST'])
@login_required
def toggle_status(id):
    """Ativa/desativa um produto."""
    produto = Produto.query.get_or_404(id)
    
    produto.ativo = not produto.ativo
    db.session.commit()
    
    status = 'ativado' if produto.ativo else 'desativado'
    return jsonify({'success': True, 'message': f'Produto {status} com sucesso!', 'ativo': produto.ativo})

@produtos.route('/<int:id>/composicao/adicionar', methods=['POST'])
@login_required
def adicionar_composicao(id):
    """Adiciona um material à composição do produto."""
    produto = Produto.query.get_or_404(id)
    
    material_id = request.form.get('material_id', type=int)
    quantidade = request.form.get('quantidade', type=float)
    
    if not material_id or not quantidade or quantidade <= 0:
        flash('Material e quantidade são obrigatórios.', 'danger')
        return redirect(url_for('produtos.view', id=id))
    
    material = Material.query.get_or_404(material_id)
    
    # Verifica se o material já está na composição
    composicao_existente = ComposicaoProduto.query.filter_by(
        produto_id=id, material_id=material_id
    ).first()
    
    if composicao_existente:
        composicao_existente.quantidade = quantidade
        flash(f'Quantidade de {material.nome} atualizada com sucesso!', 'success')
    else:
        composicao = ComposicaoProduto(
            produto_id=id,
            material_id=material_id,
            quantidade=quantidade
        )
        db.session.add(composicao)
        flash(f'Material {material.nome} adicionado à composição com sucesso!', 'success')
    
    db.session.commit()
    
    # Recalcula o custo do produto
    produto.calcular_custo()
    db.session.commit()
    
    return redirect(url_for('produtos.view', id=id))

@produtos.route('/<int:id>/composicao/<int:composicao_id>/remover', methods=['POST'])
@login_required
def remover_composicao(id, composicao_id):
    """Remove um material da composição do produto."""
    produto = Produto.query.get_or_404(id)
    composicao = ComposicaoProduto.query.get_or_404(composicao_id)
    
    if composicao.produto_id != id:
        flash('Material não pertence a este produto.', 'danger')
        return redirect(url_for('produtos.view', id=id))
    
    material_nome = composicao.material.nome
    
    db.session.delete(composicao)
    db.session.commit()
    
    # Recalcula o custo do produto
    produto.calcular_custo()
    db.session.commit()
    
    flash(f'Material {material_nome} removido da composição com sucesso!', 'success')
    return redirect(url_for('produtos.view', id=id))

@produtos.route('/api/buscar')
@login_required
def api_buscar():
    """API para buscar produtos (usado em selects)."""
    term = request.args.get('term', '')
    
    produtos = Produto.query.filter(
        Produto.ativo == True,
        Produto.nome.contains(term) | Produto.codigo.contains(term)
    ).limit(10).all()
    
    results = []
    for produto in produtos:
        results.append({
            'id': produto.id,
            'text': f'{produto.codigo} - {produto.nome}',
            'preco': float(produto.preco_minimo),
            'estoque': produto.estoque_atual
        })
    
    return jsonify(results)

