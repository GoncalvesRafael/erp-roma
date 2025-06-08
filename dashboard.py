"""
Módulo de dashboard e relatórios do ERP ROMA
"""

from flask import Blueprint, render_template, request, jsonify, send_file
from flask_login import login_required, current_user
from app import db
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.models.producao import Producao, ItemProducao
from app.models.estoque import Material, MovimentacaoEstoque
from app.models.financeiro import Movimentacao, NotaFiscal
from sqlalchemy import func, and_, or_, desc, extract
from datetime import datetime, timedelta
import calendar
import json
import os
import tempfile
from decimal import Decimal
import matplotlib
matplotlib.use('Agg')  # Usar backend não interativo
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns
from io import BytesIO
import base64

# Configuração para gráficos com caracteres em português
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Criação do Blueprint
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/')
@login_required
def index():
    """Dashboard principal."""
    # Período padrão: últimos 30 dias
    hoje = datetime.now().date()
    data_inicio = hoje - timedelta(days=30)
    data_fim = hoje
    
    # Parâmetros da URL
    periodo = request.args.get('periodo', 'mes')
    
    if periodo == 'semana':
        data_inicio = hoje - timedelta(days=7)
    elif periodo == 'mes':
        data_inicio = hoje.replace(day=1)
    elif periodo == 'trimestre':
        data_inicio = hoje - timedelta(days=90)
    elif periodo == 'ano':
        data_inicio = hoje.replace(month=1, day=1)
    elif periodo == 'personalizado':
        data_inicio_str = request.args.get('data_inicio')
        data_fim_str = request.args.get('data_fim')
        
        if data_inicio_str and data_fim_str:
            try:
                data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
                data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
            except ValueError:
                pass
    
    # Indicadores principais
    total_clientes = Cliente.query.filter_by(ativo=True).count()
    total_produtos = Produto.query.filter_by(ativo=True).count()
    
    # Produção no período
    producao_periodo = db.session.query(
        func.count(Producao.id).label('total'),
        func.sum(Producao.valor_total).label('valor')
    ).filter(
        and_(
            Producao.data >= data_inicio,
            Producao.data <= data_fim,
            Producao.status == 'finalizada'
        )
    ).first()
    
    total_producoes = producao_periodo.total or 0
    valor_producoes = producao_periodo.valor or Decimal('0.00')
    
    # Movimentações financeiras no período
    receitas = db.session.query(
        func.sum(Movimentacao.valor)
    ).filter(
        and_(
            Movimentacao.data >= data_inicio,
            Movimentacao.data <= data_fim,
            Movimentacao.tipo == 'receita'
        )
    ).scalar() or Decimal('0.00')
    
    despesas = db.session.query(
        func.sum(Movimentacao.valor)
    ).filter(
        and_(
            Movimentacao.data >= data_inicio,
            Movimentacao.data <= data_fim,
            Movimentacao.tipo == 'despesa'
        )
    ).scalar() or Decimal('0.00')
    
    saldo = receitas - despesas
    
    # Alertas de estoque
    alertas_estoque = Material.query.filter(
        Material.estoque_atual <= Material.estoque_minimo
    ).count()
    
    # Últimas produções
    ultimas_producoes = Producao.query.filter_by(
        status='finalizada'
    ).order_by(
        Producao.data.desc()
    ).limit(5).all()
    
    # Últimas movimentações financeiras
    ultimas_movimentacoes = Movimentacao.query.order_by(
        Movimentacao.data.desc()
    ).limit(5).all()
    
    # Dados para gráficos
    dados_grafico_producao = obter_dados_grafico_producao(data_inicio, data_fim)
    dados_grafico_financeiro = obter_dados_grafico_financeiro(data_inicio, data_fim)
    dados_grafico_produtos = obter_dados_grafico_produtos(data_inicio, data_fim)
    
    return render_template('dashboard/index.html',
                         periodo=periodo,
                         data_inicio=data_inicio,
                         data_fim=data_fim,
                         total_clientes=total_clientes,
                         total_produtos=total_produtos,
                         total_producoes=total_producoes,
                         valor_producoes=valor_producoes,
                         receitas=receitas,
                         despesas=despesas,
                         saldo=saldo,
                         alertas_estoque=alertas_estoque,
                         ultimas_producoes=ultimas_producoes,
                         ultimas_movimentacoes=ultimas_movimentacoes,
                         dados_grafico_producao=dados_grafico_producao,
                         dados_grafico_financeiro=dados_grafico_financeiro,
                         dados_grafico_produtos=dados_grafico_produtos)

def obter_dados_grafico_producao(data_inicio, data_fim):
    """Obtém dados para o gráfico de produção."""
    # Produção por dia
    producao_diaria = db.session.query(
        func.date(Producao.data).label('data'),
        func.count(Producao.id).label('total'),
        func.sum(Producao.valor_total).label('valor')
    ).filter(
        and_(
            Producao.data >= data_inicio,
            Producao.data <= data_fim,
            Producao.status == 'finalizada'
        )
    ).group_by(
        func.date(Producao.data)
    ).order_by(
        func.date(Producao.data)
    ).all()
    
    # Formata os dados para o gráfico
    datas = [p.data.strftime('%d/%m/%Y') for p in producao_diaria]
    totais = [p.total for p in producao_diaria]
    valores = [float(p.valor) if p.valor else 0 for p in producao_diaria]
    
    return {
        'datas': datas,
        'totais': totais,
        'valores': valores
    }

def obter_dados_grafico_financeiro(data_inicio, data_fim):
    """Obtém dados para o gráfico financeiro."""
    # Movimentações por dia
    movimentacoes_diarias = db.session.query(
        func.date(Movimentacao.data).label('data'),
        Movimentacao.tipo,
        func.sum(Movimentacao.valor).label('valor')
    ).filter(
        and_(
            Movimentacao.data >= data_inicio,
            Movimentacao.data <= data_fim
        )
    ).group_by(
        func.date(Movimentacao.data),
        Movimentacao.tipo
    ).order_by(
        func.date(Movimentacao.data)
    ).all()
    
    # Organiza os dados por data e tipo
    datas_unicas = sorted(set(m.data for m in movimentacoes_diarias))
    
    receitas_por_data = {data: 0 for data in datas_unicas}
    despesas_por_data = {data: 0 for data in datas_unicas}
    
    for m in movimentacoes_diarias:
        if m.tipo == 'receita':
            receitas_por_data[m.data] = float(m.valor) if m.valor else 0
        else:
            despesas_por_data[m.data] = float(m.valor) if m.valor else 0
    
    # Formata os dados para o gráfico
    datas = [data.strftime('%d/%m/%Y') for data in datas_unicas]
    receitas = [receitas_por_data[data] for data in datas_unicas]
    despesas = [despesas_por_data[data] for data in datas_unicas]
    
    return {
        'datas': datas,
        'receitas': receitas,
        'despesas': despesas
    }

def obter_dados_grafico_produtos(data_inicio, data_fim):
    """Obtém dados para o gráfico de produtos mais produzidos."""
    # Produtos mais produzidos
    produtos_mais_produzidos = db.session.query(
        Produto.nome,
        func.sum(ItemProducao.quantidade).label('quantidade')
    ).join(
        ItemProducao, ItemProducao.produto_id == Produto.id
    ).join(
        Producao, Producao.id == ItemProducao.producao_id
    ).filter(
        and_(
            Producao.data >= data_inicio,
            Producao.data <= data_fim,
            Producao.status == 'finalizada'
        )
    ).group_by(
        Produto.id
    ).order_by(
        func.sum(ItemProducao.quantidade).desc()
    ).limit(5).all()
    
    # Formata os dados para o gráfico
    produtos = [p.nome for p in produtos_mais_produzidos]
    quantidades = [p.quantidade for p in produtos_mais_produzidos]
    
    return {
        'produtos': produtos,
        'quantidades': quantidades
    }

@dashboard.route('/relatorios')
@login_required
def relatorios():
    """Página de relatórios."""
    return render_template('dashboard/relatorios.html')

@dashboard.route('/relatorio/producao', methods=['GET', 'POST'])
@login_required
def relatorio_producao():
    """Relatório de produção."""
    # Período padrão: mês atual
    hoje = datetime.now().date()
    data_inicio = hoje.replace(day=1)
    data_fim = hoje
    
    # Parâmetros do formulário
    if request.method == 'POST':
        data_inicio_str = request.form.get('data_inicio')
        data_fim_str = request.form.get('data_fim')
        cliente_id = request.form.get('cliente_id')
        produto_id = request.form.get('produto_id')
        
        try:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            pass
        
        # Consulta base
        query = Producao.query.filter(
            and_(
                Producao.data >= data_inicio,
                Producao.data <= data_fim,
                Producao.status == 'finalizada'
            )
        )
        
        # Filtros adicionais
        if cliente_id and cliente_id != '0':
            query = query.filter_by(cliente_id=int(cliente_id))
        
        if produto_id and produto_id != '0':
            query = query.join(
                ItemProducao, ItemProducao.producao_id == Producao.id
            ).filter(
                ItemProducao.produto_id == int(produto_id)
            )
        
        # Executa a consulta
        producoes = query.order_by(Producao.data.desc()).all()
        
        # Gera o relatório
        if request.form.get('formato') == 'pdf':
            return gerar_pdf_producao(producoes, data_inicio, data_fim)
        
        # Renderiza a página com os resultados
        return render_template('dashboard/relatorio_producao.html',
                             producoes=producoes,
                             data_inicio=data_inicio,
                             data_fim=data_fim,
                             cliente_id=cliente_id,
                             produto_id=produto_id)
    
    # Carrega dados para os filtros
    clientes = Cliente.query.filter_by(ativo=True).order_by(Cliente.nome).all()
    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
    
    return render_template('dashboard/relatorio_producao.html',
                         clientes=clientes,
                         produtos=produtos,
                         data_inicio=data_inicio,
                         data_fim=data_fim)

@dashboard.route('/relatorio/financeiro', methods=['GET', 'POST'])
@login_required
def relatorio_financeiro():
    """Relatório financeiro."""
    # Período padrão: mês atual
    hoje = datetime.now().date()
    data_inicio = hoje.replace(day=1)
    data_fim = hoje
    
    # Parâmetros do formulário
    if request.method == 'POST':
        data_inicio_str = request.form.get('data_inicio')
        data_fim_str = request.form.get('data_fim')
        tipo = request.form.get('tipo')
        categoria = request.form.get('categoria')
        
        try:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            pass
        
        # Consulta base
        query = Movimentacao.query.filter(
            and_(
                Movimentacao.data >= data_inicio,
                Movimentacao.data <= data_fim
            )
        )
        
        # Filtros adicionais
        if tipo and tipo != 'todos':
            query = query.filter_by(tipo=tipo)
        
        if categoria and categoria != 'todas':
            query = query.filter_by(categoria=categoria)
        
        # Executa a consulta
        movimentacoes = query.order_by(Movimentacao.data.desc()).all()
        
        # Gera o relatório
        if request.form.get('formato') == 'pdf':
            return gerar_pdf_financeiro(movimentacoes, data_inicio, data_fim, tipo, categoria)
        
        # Renderiza a página com os resultados
        return render_template('dashboard/relatorio_financeiro.html',
                             movimentacoes=movimentacoes,
                             data_inicio=data_inicio,
                             data_fim=data_fim,
                             tipo=tipo,
                             categoria=categoria)
    
    # Carrega dados para os filtros
    categorias = db.session.query(Movimentacao.categoria).distinct().all()
    categorias = [c[0] for c in categorias if c[0]]
    
    return render_template('dashboard/relatorio_financeiro.html',
                         categorias=categorias,
                         data_inicio=data_inicio,
                         data_fim=data_fim)

@dashboard.route('/relatorio/estoque', methods=['GET', 'POST'])
@login_required
def relatorio_estoque():
    """Relatório de estoque."""
    # Parâmetros do formulário
    if request.method == 'POST':
        tipo_relatorio = request.form.get('tipo_relatorio', 'atual')
        categoria = request.form.get('categoria')
        
        if tipo_relatorio == 'atual':
            # Relatório de estoque atual
            query = Material.query
            
            if categoria and categoria != 'todas':
                query = query.filter_by(categoria=categoria)
            
            materiais = query.order_by(Material.nome).all()
            
            # Gera o relatório
            if request.form.get('formato') == 'pdf':
                return gerar_pdf_estoque_atual(materiais)
            
            return render_template('dashboard/relatorio_estoque.html',
                                 materiais=materiais,
                                 tipo_relatorio=tipo_relatorio,
                                 categoria=categoria)
        
        elif tipo_relatorio == 'movimentacoes':
            # Relatório de movimentações de estoque
            data_inicio_str = request.form.get('data_inicio')
            data_fim_str = request.form.get('data_fim')
            material_id = request.form.get('material_id')
            tipo_movimentacao = request.form.get('tipo_movimentacao')
            
            hoje = datetime.now().date()
            data_inicio = hoje.replace(day=1)
            data_fim = hoje
            
            try:
                data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
                data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                pass
            
            # Consulta base
            query = MovimentacaoEstoque.query.filter(
                and_(
                    MovimentacaoEstoque.data >= data_inicio,
                    MovimentacaoEstoque.data <= data_fim
                )
            )
            
            # Filtros adicionais
            if material_id and material_id != '0':
                query = query.filter_by(material_id=int(material_id))
            
            if tipo_movimentacao and tipo_movimentacao != 'todos':
                query = query.filter_by(tipo=tipo_movimentacao)
            
            # Executa a consulta
            movimentacoes = query.order_by(MovimentacaoEstoque.data.desc()).all()
            
            # Gera o relatório
            if request.form.get('formato') == 'pdf':
                return gerar_pdf_movimentacoes_estoque(movimentacoes, data_inicio, data_fim)
            
            return render_template('dashboard/relatorio_estoque.html',
                                 movimentacoes=movimentacoes,
                                 tipo_relatorio=tipo_relatorio,
                                 data_inicio=data_inicio,
                                 data_fim=data_fim,
                                 material_id=material_id,
                                 tipo_movimentacao=tipo_movimentacao)
    
    # Carrega dados para os filtros
    categorias = db.session.query(Material.categoria).distinct().all()
    categorias = [c[0] for c in categorias if c[0]]
    
    materiais = Material.query.order_by(Material.nome).all()
    
    return render_template('dashboard/relatorio_estoque.html',
                         categorias=categorias,
                         materiais=materiais)

@dashboard.route('/relatorio/clientes', methods=['GET', 'POST'])
@login_required
def relatorio_clientes():
    """Relatório de clientes."""
    # Parâmetros do formulário
    if request.method == 'POST':
        ativo = request.form.get('ativo')
        
        # Consulta base
        query = Cliente.query
        
        # Filtros adicionais
        if ativo == 'sim':
            query = query.filter_by(ativo=True)
        elif ativo == 'nao':
            query = query.filter_by(ativo=False)
        
        # Executa a consulta
        clientes = query.order_by(Cliente.nome).all()
        
        # Gera o relatório
        if request.form.get('formato') == 'pdf':
            return gerar_pdf_clientes(clientes)
        
        # Renderiza a página com os resultados
        return render_template('dashboard/relatorio_clientes.html',
                             clientes=clientes,
                             ativo=ativo)
    
    return render_template('dashboard/relatorio_clientes.html')

@dashboard.route('/relatorio/produtos', methods=['GET', 'POST'])
@login_required
def relatorio_produtos():
    """Relatório de produtos."""
    # Parâmetros do formulário
    if request.method == 'POST':
        categoria = request.form.get('categoria')
        ativo = request.form.get('ativo')
        
        # Consulta base
        query = Produto.query
        
        # Filtros adicionais
        if categoria and categoria != 'todas':
            query = query.filter_by(categoria=categoria)
        
        if ativo == 'sim':
            query = query.filter_by(ativo=True)
        elif ativo == 'nao':
            query = query.filter_by(ativo=False)
        
        # Executa a consulta
        produtos = query.order_by(Produto.nome).all()
        
        # Gera o relatório
        if request.form.get('formato') == 'pdf':
            return gerar_pdf_produtos(produtos)
        
        # Renderiza a página com os resultados
        return render_template('dashboard/relatorio_produtos.html',
                             produtos=produtos,
                             categoria=categoria,
                             ativo=ativo)
    
    # Carrega dados para os filtros
    categorias = db.session.query(Produto.categoria).distinct().all()
    categorias = [c[0] for c in categorias if c[0]]
    
    return render_template('dashboard/relatorio_produtos.html',
                         categorias=categorias)

@dashboard.route('/grafico/producao-mensal')
@login_required
def grafico_producao_mensal():
    """Gera gráfico de produção mensal."""
    # Obtém o ano atual ou o ano especificado
    ano = request.args.get('ano', datetime.now().year)
    try:
        ano = int(ano)
    except ValueError:
        ano = datetime.now().year
    
    # Consulta a produção mensal
    producao_mensal = db.session.query(
        extract('month', Producao.data).label('mes'),
        func.count(Producao.id).label('total'),
        func.sum(Producao.valor_total).label('valor')
    ).filter(
        and_(
            extract('year', Producao.data) == ano,
            Producao.status == 'finalizada'
        )
    ).group_by(
        extract('month', Producao.data)
    ).order_by(
        extract('month', Producao.data)
    ).all()
    
    # Prepara os dados para todos os meses
    meses = range(1, 13)
    totais = {mes: 0 for mes in meses}
    valores = {mes: 0 for mes in meses}
    
    for p in producao_mensal:
        totais[p.mes] = p.total
        valores[p.mes] = float(p.valor) if p.valor else 0
    
    # Cria o gráfico
    plt.figure(figsize=(10, 6))
    
    # Gráfico de barras para quantidade
    ax1 = plt.subplot(111)
    ax1.bar(meses, [totais[mes] for mes in meses], color='#6366F1', alpha=0.7, label='Quantidade')
    ax1.set_xlabel('Mês')
    ax1.set_ylabel('Quantidade de Produções')
    ax1.set_xticks(meses)
    ax1.set_xticklabels(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
    
    # Gráfico de linha para valor
    ax2 = ax1.twinx()
    ax2.plot(meses, [valores[mes] for mes in meses], color='#F59E0B', marker='o', linewidth=2, label='Valor (R$)')
    ax2.set_ylabel('Valor Total (R$)')
    
    # Título e legenda
    plt.title(f'Produção Mensal - {ano}')
    
    # Combina as legendas
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    # Salva o gráfico em um buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    
    # Converte para base64
    image_png = buffer.getvalue()
    buffer.close()
    
    # Retorna a imagem
    response = send_file(
        BytesIO(image_png),
        mimetype='image/png',
        as_attachment=False
    )
    
    return response

@dashboard.route('/grafico/financeiro-mensal')
@login_required
def grafico_financeiro_mensal():
    """Gera gráfico financeiro mensal."""
    # Obtém o ano atual ou o ano especificado
    ano = request.args.get('ano', datetime.now().year)
    try:
        ano = int(ano)
    except ValueError:
        ano = datetime.now().year
    
    # Consulta as movimentações mensais
    movimentacoes_mensais = db.session.query(
        extract('month', Movimentacao.data).label('mes'),
        Movimentacao.tipo,
        func.sum(Movimentacao.valor).label('valor')
    ).filter(
        extract('year', Movimentacao.data) == ano
    ).group_by(
        extract('month', Movimentacao.data),
        Movimentacao.tipo
    ).order_by(
        extract('month', Movimentacao.data)
    ).all()
    
    # Prepara os dados para todos os meses
    meses = range(1, 13)
    receitas = {mes: 0 for mes in meses}
    despesas = {mes: 0 for mes in meses}
    
    for m in movimentacoes_mensais:
        if m.tipo == 'receita':
            receitas[m.mes] = float(m.valor) if m.valor else 0
        else:
            despesas[m.mes] = float(m.valor) if m.valor else 0
    
    # Cria o gráfico
    plt.figure(figsize=(10, 6))
    
    # Gráfico de barras agrupadas
    x = np.arange(len(meses))
    width = 0.35
    
    plt.bar(x - width/2, [receitas[mes] for mes in meses], width, color='#10B981', label='Receitas')
    plt.bar(x + width/2, [despesas[mes] for mes in meses], width, color='#EF4444', label='Despesas')
    
    plt.xlabel('Mês')
    plt.ylabel('Valor (R$)')
    plt.title(f'Movimentações Financeiras - {ano}')
    plt.xticks(x, ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
    plt.legend()
    
    # Adiciona os valores de saldo
    saldos = [receitas[mes] - despesas[mes] for mes in meses]
    plt.plot(x, saldos, color='#6366F1', marker='o', linewidth=2, label='Saldo')
    
    # Salva o gráfico em um buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    
    # Converte para base64
    image_png = buffer.getvalue()
    buffer.close()
    
    # Retorna a imagem
    response = send_file(
        BytesIO(image_png),
        mimetype='image/png',
        as_attachment=False
    )
    
    return response

@dashboard.route('/grafico/produtos-mais-produzidos')
@login_required
def grafico_produtos_mais_produzidos():
    """Gera gráfico de produtos mais produzidos."""
    # Obtém o período
    periodo = request.args.get('periodo', 'ano')
    
    hoje = datetime.now().date()
    
    if periodo == 'mes':
        data_inicio = hoje.replace(day=1)
    elif periodo == 'trimestre':
        data_inicio = hoje - timedelta(days=90)
    elif periodo == 'semestre':
        data_inicio = hoje - timedelta(days=180)
    else:  # ano
        data_inicio = hoje.replace(month=1, day=1)
    
    data_fim = hoje
    
    # Consulta os produtos mais produzidos
    produtos_mais_produzidos = db.session.query(
        Produto.nome,
        func.sum(ItemProducao.quantidade).label('quantidade')
    ).join(
        ItemProducao, ItemProducao.produto_id == Produto.id
    ).join(
        Producao, Producao.id == ItemProducao.producao_id
    ).filter(
        and_(
            Producao.data >= data_inicio,
            Producao.data <= data_fim,
            Producao.status == 'finalizada'
        )
    ).group_by(
        Produto.id
    ).order_by(
        func.sum(ItemProducao.quantidade).desc()
    ).limit(10).all()
    
    # Prepara os dados
    produtos = [p.nome for p in produtos_mais_produzidos]
    quantidades = [p.quantidade for p in produtos_mais_produzidos]
    
    # Cria o gráfico
    plt.figure(figsize=(10, 6))
    
    # Gráfico de barras horizontais
    plt.barh(produtos, quantidades, color='#6366F1')
    
    plt.xlabel('Quantidade')
    plt.ylabel('Produto')
    plt.title(f'Produtos Mais Produzidos - {periodo.capitalize()}')
    
    # Adiciona os valores nas barras
    for i, v in enumerate(quantidades):
        plt.text(v + 0.1, i, str(v), va='center')
    
    # Salva o gráfico em um buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    
    # Converte para base64
    image_png = buffer.getvalue()
    buffer.close()
    
    # Retorna a imagem
    response = send_file(
        BytesIO(image_png),
        mimetype='image/png',
        as_attachment=False
    )
    
    return response

@dashboard.route('/grafico/clientes-mais-atendidos')
@login_required
def grafico_clientes_mais_atendidos():
    """Gera gráfico de clientes mais atendidos."""
    # Obtém o período
    periodo = request.args.get('periodo', 'ano')
    
    hoje = datetime.now().date()
    
    if periodo == 'mes':
        data_inicio = hoje.replace(day=1)
    elif periodo == 'trimestre':
        data_inicio = hoje - timedelta(days=90)
    elif periodo == 'semestre':
        data_inicio = hoje - timedelta(days=180)
    else:  # ano
        data_inicio = hoje.replace(month=1, day=1)
    
    data_fim = hoje
    
    # Consulta os clientes mais atendidos
    clientes_mais_atendidos = db.session.query(
        Cliente.nome,
        func.count(Producao.id).label('total'),
        func.sum(Producao.valor_total).label('valor')
    ).join(
        Producao, Producao.cliente_id == Cliente.id
    ).filter(
        and_(
            Producao.data >= data_inicio,
            Producao.data <= data_fim,
            Producao.status == 'finalizada'
        )
    ).group_by(
        Cliente.id
    ).order_by(
        func.sum(Producao.valor_total).desc()
    ).limit(10).all()
    
    # Prepara os dados
    clientes = [c.nome for c in clientes_mais_atendidos]
    valores = [float(c.valor) if c.valor else 0 for c in clientes_mais_atendidos]
    
    # Cria o gráfico
    plt.figure(figsize=(10, 6))
    
    # Gráfico de pizza
    plt.pie(valores, labels=clientes, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    
    plt.title(f'Clientes Mais Atendidos (por valor) - {periodo.capitalize()}')
    
    # Salva o gráfico em um buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    
    # Converte para base64
    image_png = buffer.getvalue()
    buffer.close()
    
    # Retorna a imagem
    response = send_file(
        BytesIO(image_png),
        mimetype='image/png',
        as_attachment=False
    )
    
    return response

# Funções auxiliares para geração de PDFs
def gerar_pdf_producao(producoes, data_inicio, data_fim):
    """Gera um relatório PDF de produção."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    
    # Cria um arquivo temporário
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        # Configura o documento
        doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        subtitle_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Título
        elements.append(Paragraph('Relatório de Produção', title_style))
        elements.append(Spacer(1, 12))
        
        # Período
        elements.append(Paragraph(f'Período: {data_inicio.strftime("%d/%m/%Y")} a {data_fim.strftime("%d/%m/%Y")}', subtitle_style))
        elements.append(Spacer(1, 12))
        
        # Tabela de produções
        data = [['Data', 'Cliente', 'Valor Total', 'Status']]
        
        for p in producoes:
            data.append([
                p.data.strftime('%d/%m/%Y'),
                p.cliente.nome if p.cliente else '',
                f'R$ {p.valor_total:.2f}',
                p.status.capitalize()
            ])
        
        # Adiciona totais
        valor_total = sum(p.valor_total for p in producoes)
        data.append(['', 'Total', f'R$ {valor_total:.2f}', ''])
        
        # Cria a tabela
        table = Table(data)
        
        # Estilo da tabela
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
        ]))
        
        elements.append(table)
        
        # Constrói o PDF
        doc.build(elements)
        
        # Retorna o arquivo
        return send_file(
            temp_file.name,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'relatorio_producao_{data_inicio.strftime("%Y%m%d")}_{data_fim.strftime("%Y%m%d")}.pdf'
        )

def gerar_pdf_financeiro(movimentacoes, data_inicio, data_fim, tipo, categoria):
    """Gera um relatório PDF financeiro."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    
    # Cria um arquivo temporário
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        # Configura o documento
        doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        subtitle_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Título
        elements.append(Paragraph('Relatório Financeiro', title_style))
        elements.append(Spacer(1, 12))
        
        # Período
        elements.append(Paragraph(f'Período: {data_inicio.strftime("%d/%m/%Y")} a {data_fim.strftime("%d/%m/%Y")}', subtitle_style))
        elements.append(Spacer(1, 12))
        
        # Filtros
        filtros = []
        if tipo and tipo != 'todos':
            filtros.append(f'Tipo: {tipo.capitalize()}')
        if categoria and categoria != 'todas':
            filtros.append(f'Categoria: {categoria}')
        
        if filtros:
            elements.append(Paragraph('Filtros: ' + ', '.join(filtros), normal_style))
            elements.append(Spacer(1, 12))
        
        # Tabela de movimentações
        data = [['Data', 'Tipo', 'Categoria', 'Descrição', 'Valor']]
        
        for m in movimentacoes:
            data.append([
                m.data.strftime('%d/%m/%Y'),
                m.tipo.capitalize(),
                m.categoria,
                m.descricao,
                f'R$ {m.valor:.2f}'
            ])
        
        # Adiciona totais
        receitas = sum(m.valor for m in movimentacoes if m.tipo == 'receita')
        despesas = sum(m.valor for m in movimentacoes if m.tipo == 'despesa')
        saldo = receitas - despesas
        
        data.append(['', '', '', 'Total Receitas', f'R$ {receitas:.2f}'])
        data.append(['', '', '', 'Total Despesas', f'R$ {despesas:.2f}'])
        data.append(['', '', '', 'Saldo', f'R$ {saldo:.2f}'])
        
        # Cria a tabela
        table = Table(data)
        
        # Estilo da tabela
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -3), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
        ]))
        
        elements.append(table)
        
        # Constrói o PDF
        doc.build(elements)
        
        # Retorna o arquivo
        return send_file(
            temp_file.name,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'relatorio_financeiro_{data_inicio.strftime("%Y%m%d")}_{data_fim.strftime("%Y%m%d")}.pdf'
        )

def gerar_pdf_estoque_atual(materiais):
    """Gera um relatório PDF de estoque atual."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    
    # Cria um arquivo temporário
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        # Configura o documento
        doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        subtitle_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Título
        elements.append(Paragraph('Relatório de Estoque Atual', title_style))
        elements.append(Spacer(1, 12))
        
        # Data
        elements.append(Paragraph(f'Data: {datetime.now().strftime("%d/%m/%Y")}', subtitle_style))
        elements.append(Spacer(1, 12))
        
        # Tabela de materiais
        data = [['Código', 'Material', 'Categoria', 'Estoque Atual', 'Estoque Mínimo', 'Status']]
        
        for m in materiais:
            # Define o status
            if m.estoque_atual <= m.estoque_minimo:
                status = 'Baixo'
            else:
                status = 'Normal'
            
            data.append([
                m.codigo,
                m.nome,
                m.categoria,
                m.estoque_atual,
                m.estoque_minimo,
                status
            ])
        
        # Cria a tabela
        table = Table(data)
        
        # Estilo da tabela
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (3, 1), (4, -1), 'CENTER'),
        ]))
        
        # Adiciona cores para status
        for i in range(1, len(data)):
            if data[i][-1] == 'Baixo':
                table.setStyle(TableStyle([
                    ('TEXTCOLOR', (-1, i), (-1, i), colors.red),
                    ('FONTNAME', (-1, i), (-1, i), 'Helvetica-Bold'),
                ]))
        
        elements.append(table)
        
        # Constrói o PDF
        doc.build(elements)
        
        # Retorna o arquivo
        return send_file(
            temp_file.name,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'relatorio_estoque_atual_{datetime.now().strftime("%Y%m%d")}.pdf'
        )

def gerar_pdf_movimentacoes_estoque(movimentacoes, data_inicio, data_fim):
    """Gera um relatório PDF de movimentações de estoque."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    
    # Cria um arquivo temporário
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        # Configura o documento
        doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        subtitle_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Título
        elements.append(Paragraph('Relatório de Movimentações de Estoque', title_style))
        elements.append(Spacer(1, 12))
        
        # Período
        elements.append(Paragraph(f'Período: {data_inicio.strftime("%d/%m/%Y")} a {data_fim.strftime("%d/%m/%Y")}', subtitle_style))
        elements.append(Spacer(1, 12))
        
        # Tabela de movimentações
        data = [['Data', 'Material', 'Tipo', 'Quantidade', 'Observação']]
        
        for m in movimentacoes:
            data.append([
                m.data.strftime('%d/%m/%Y'),
                m.material.nome if m.material else '',
                m.tipo.capitalize(),
                m.quantidade,
                m.observacao or ''
            ])
        
        # Cria a tabela
        table = Table(data)
        
        # Estilo da tabela
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),
        ]))
        
        # Adiciona cores para tipo
        for i in range(1, len(data)):
            if data[i][2] == 'Entrada':
                table.setStyle(TableStyle([
                    ('TEXTCOLOR', (2, i), (2, i), colors.green),
                ]))
            elif data[i][2] == 'Saída':
                table.setStyle(TableStyle([
                    ('TEXTCOLOR', (2, i), (2, i), colors.red),
                ]))
        
        elements.append(table)
        
        # Constrói o PDF
        doc.build(elements)
        
        # Retorna o arquivo
        return send_file(
            temp_file.name,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'relatorio_movimentacoes_estoque_{data_inicio.strftime("%Y%m%d")}_{data_fim.strftime("%Y%m%d")}.pdf'
        )

def gerar_pdf_clientes(clientes):
    """Gera um relatório PDF de clientes."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    
    # Cria um arquivo temporário
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        # Configura o documento
        doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        subtitle_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Título
        elements.append(Paragraph('Relatório de Clientes', title_style))
        elements.append(Spacer(1, 12))
        
        # Data
        elements.append(Paragraph(f'Data: {datetime.now().strftime("%d/%m/%Y")}', subtitle_style))
        elements.append(Spacer(1, 12))
        
        # Tabela de clientes
        data = [['Nome', 'CNPJ', 'Telefone', 'Email', 'Cidade/UF', 'Status']]
        
        for c in clientes:
            data.append([
                c.nome,
                c.cnpj,
                c.telefone,
                c.email,
                f'{c.cidade}/{c.estado}',
                'Ativo' if c.ativo else 'Inativo'
            ])
        
        # Cria a tabela
        table = Table(data)
        
        # Estilo da tabela
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        # Adiciona cores para status
        for i in range(1, len(data)):
            if data[i][-1] == 'Ativo':
                table.setStyle(TableStyle([
                    ('TEXTCOLOR', (-1, i), (-1, i), colors.green),
                ]))
            else:
                table.setStyle(TableStyle([
                    ('TEXTCOLOR', (-1, i), (-1, i), colors.red),
                ]))
        
        elements.append(table)
        
        # Constrói o PDF
        doc.build(elements)
        
        # Retorna o arquivo
        return send_file(
            temp_file.name,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'relatorio_clientes_{datetime.now().strftime("%Y%m%d")}.pdf'
        )

def gerar_pdf_produtos(produtos):
    """Gera um relatório PDF de produtos."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    
    # Cria um arquivo temporário
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        # Configura o documento
        doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        subtitle_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Título
        elements.append(Paragraph('Relatório de Produtos', title_style))
        elements.append(Spacer(1, 12))
        
        # Data
        elements.append(Paragraph(f'Data: {datetime.now().strftime("%d/%m/%Y")}', subtitle_style))
        elements.append(Spacer(1, 12))
        
        # Tabela de produtos
        data = [['Código', 'Nome', 'Categoria', 'Preço Venda', 'Estoque', 'Status']]
        
        for p in produtos:
            data.append([
                p.codigo,
                p.nome,
                p.categoria,
                f'R$ {p.preco_venda:.2f}',
                p.estoque_atual,
                'Ativo' if p.ativo else 'Inativo'
            ])
        
        # Cria a tabela
        table = Table(data)
        
        # Estilo da tabela
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
            ('ALIGN', (4, 1), (4, -1), 'CENTER'),
        ]))
        
        # Adiciona cores para status
        for i in range(1, len(data)):
            if data[i][-1] == 'Ativo':
                table.setStyle(TableStyle([
                    ('TEXTCOLOR', (-1, i), (-1, i), colors.green),
                ]))
            else:
                table.setStyle(TableStyle([
                    ('TEXTCOLOR', (-1, i), (-1, i), colors.red),
                ]))
        
        elements.append(table)
        
        # Constrói o PDF
        doc.build(elements)
        
        # Retorna o arquivo
        return send_file(
            temp_file.name,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'relatorio_produtos_{datetime.now().strftime("%Y%m%d")}.pdf'
        )

