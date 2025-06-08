"""
Módulo principal do ERP ROMA
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.models.material import Material
from app.models.producao import Producao
from app.models.financeiro import Movimentacao
from datetime import datetime, timedelta
from sqlalchemy import func, and_

# Criação do Blueprint
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal do sistema."""
    
    # Calcula estatísticas para o dashboard
    stats = {}
    
    # Total de clientes
    stats['total_clientes'] = Cliente.query.filter_by(ativo=True).count()
    
    # Total de produtos
    stats['total_produtos'] = Produto.query.filter_by(ativo=True).count()
    
    # Produções este mês
    inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    stats['producoes_mes'] = Producao.query.filter(
        Producao.data >= inicio_mes.date()
    ).count()
    
    # Faturamento este mês (simulado - será implementado com dados reais)
    entradas_mes = db.session.query(func.sum(Movimentacao.valor)).filter(
        and_(
            Movimentacao.tipo == 'entrada',
            Movimentacao.data >= inicio_mes.date()
        )
    ).scalar() or 0
    stats['faturamento_mes'] = float(entradas_mes)
    
    # Faturamento total (simulado)
    faturamento_total = db.session.query(func.sum(Movimentacao.valor)).filter(
        Movimentacao.tipo == 'entrada'
    ).scalar() or 0
    stats['faturamento_total'] = float(faturamento_total)
    
    # Últimas produções
    ultimas_producoes = Producao.query.order_by(Producao.data.desc()).limit(5).all()
    
    # Alertas de estoque (produtos e materiais com estoque baixo)
    alertas_estoque = []
    
    # Produtos com estoque baixo
    produtos_baixo_estoque = Produto.query.filter(
        and_(
            Produto.ativo == True,
            Produto.estoque_atual <= Produto.estoque_minimo
        )
    ).limit(5).all()
    
    for produto in produtos_baixo_estoque:
        alertas_estoque.append({
            'nome': produto.nome,
            'estoque_atual': produto.estoque_atual,
            'estoque_minimo': produto.estoque_minimo,
            'tipo': 'produto'
        })
    
    # Materiais com estoque baixo
    materiais_baixo_estoque = Material.query.filter(
        and_(
            Material.ativo == True,
            Material.estoque_atual <= Material.estoque_minimo
        )
    ).limit(5).all()
    
    for material in materiais_baixo_estoque:
        alertas_estoque.append({
            'nome': material.nome,
            'estoque_atual': material.estoque_atual,
            'estoque_minimo': material.estoque_minimo,
            'tipo': 'material'
        })
    
    return render_template('dashboard.html', 
                         stats=stats,
                         ultimas_producoes=ultimas_producoes,
                         alertas_estoque=alertas_estoque[:10])  # Limita a 10 alertas

