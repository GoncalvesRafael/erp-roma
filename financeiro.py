"""
Módulo financeiro do ERP ROMA
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.financeiro import Movimentacao, NotaFiscal
from app.forms import MovimentacaoForm, NotaFiscalForm
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_
from decimal import Decimal

# Criação do Blueprint
financeiro = Blueprint('financeiro', __name__, url_prefix='/financeiro')

@financeiro.route('/')
@login_required
def index():
    """Dashboard financeiro."""
    # Período padrão: mês atual
    hoje = datetime.now().date()
    inicio_mes = hoje.replace(day=1)
    
    # Parâmetros da URL
    data_inicio = request.args.get('data_inicio', inicio_mes.strftime('%Y-%m-%d'))
    data_fim = request.args.get('data_fim', hoje.strftime('%Y-%m-%d'))
    
    try:
        data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
    except ValueError:
        flash('Formato de data inválido.', 'danger')
        data_inicio_obj = inicio_mes
        data_fim_obj = hoje
        data_inicio = inicio_mes.strftime('%Y-%m-%d')
        data_fim = hoje.strftime('%Y-%m-%d')
    
    # Consultas financeiras
    query_base = Movimentacao.query.filter(
        and_(
            Movimentacao.data >= data_inicio_obj,
            Movimentacao.data <= data_fim_obj
        )
    )
    
    # Totais
    receitas = query_base.filter_by(tipo='receita').with_entities(
        func.sum(Movimentacao.valor)
    ).scalar() or Decimal('0')
    
    despesas = query_base.filter_by(tipo='despesa').with_entities(
        func.sum(Movimentacao.valor)
    ).scalar() or Decimal('0')
    
    saldo = receitas - despesas
    
    # Últimas movimentações
    ultimas_movimentacoes = Movimentacao.query.order_by(
        Movimentacao.data.desc()
    ).limit(10).all()
    
    # Movimentações por categoria
    categorias = db.session.query(
        Movimentacao.categoria,
        Movimentacao.tipo,
        func.sum(Movimentacao.valor).label('total')
    ).filter(
        and_(
            Movimentacao.data >= data_inicio_obj,
            Movimentacao.data <= data_fim_obj
        )
    ).group_by(Movimentacao.categoria, Movimentacao.tipo).all()
    
    # Notas fiscais pendentes
    notas_pendentes = NotaFiscal.query.filter_by(status='pendente').count()
    
    return render_template('financeiro/index.html',
                         receitas=receitas,
                         despesas=despesas,
                         saldo=saldo,
                         ultimas_movimentacoes=ultimas_movimentacoes,
                         categorias=categorias,
                         notas_pendentes=notas_pendentes,
                         data_inicio=data_inicio,
                         data_fim=data_fim)

@financeiro.route('/movimentacoes')
@login_required
def movimentacoes():
    """Lista todas as movimentações financeiras."""
    page = request.args.get('page', 1, type=int)
    tipo = request.args.get('tipo', '', type=str)
    categoria = request.args.get('categoria', '', type=str)
    data_inicio = request.args.get('data_inicio', '', type=str)
    data_fim = request.args.get('data_fim', '', type=str)
    
    query = Movimentacao.query
    
    if tipo:
        query = query.filter_by(tipo=tipo)
    
    if categoria:
        query = query.filter_by(categoria=categoria)
    
    if data_inicio:
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            query = query.filter(Movimentacao.data >= data_inicio_obj)
        except ValueError:
            pass
    
    if data_fim:
        try:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
            query = query.filter(Movimentacao.data <= data_fim_obj)
        except ValueError:
            pass
    
    movimentacoes_paginadas = query.order_by(Movimentacao.data.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Lista de categorias para o filtro
    categorias = db.session.query(Movimentacao.categoria).filter(
        Movimentacao.categoria != None
    ).distinct().all()
    categorias = [c[0] for c in categorias if c[0]]
    
    return render_template('financeiro/movimentacoes.html',
                         movimentacoes=movimentacoes_paginadas,
                         tipo=tipo,
                         categoria=categoria,
                         data_inicio=data_inicio,
                         data_fim=data_fim,
                         categorias=categorias)

@financeiro.route('/movimentacao/nova', methods=['GET', 'POST'])
@login_required
def nova_movimentacao():
    """Cria uma nova movimentação financeira."""
    form = MovimentacaoForm()
    
    if form.validate_on_submit():
        movimentacao = Movimentacao(
            tipo=form.tipo.data,
            categoria=form.categoria.data,
            descricao=form.descricao.data,
            valor=form.valor.data,
            data=form.data.data,
            forma_pagamento=form.forma_pagamento.data,
            observacoes=form.observacoes.data,
            usuario_id=current_user.id
        )
        
        db.session.add(movimentacao)
        db.session.commit()
        
        flash(f'Movimentação de {form.tipo.data} registrada com sucesso!', 'success')
        return redirect(url_for('financeiro.movimentacoes'))
    
    return render_template('financeiro/movimentacao_form.html', form=form, title='Nova Movimentação')

@financeiro.route('/movimentacao/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_movimentacao(id):
    """Edita uma movimentação financeira."""
    movimentacao = Movimentacao.query.get_or_404(id)
    form = MovimentacaoForm(obj=movimentacao)
    
    if form.validate_on_submit():
        movimentacao.tipo = form.tipo.data
        movimentacao.categoria = form.categoria.data
        movimentacao.descricao = form.descricao.data
        movimentacao.valor = form.valor.data
        movimentacao.data = form.data.data
        movimentacao.forma_pagamento = form.forma_pagamento.data
        movimentacao.observacoes = form.observacoes.data
        
        db.session.commit()
        
        flash('Movimentação atualizada com sucesso!', 'success')
        return redirect(url_for('financeiro.movimentacoes'))
    
    return render_template('financeiro/movimentacao_form.html', 
                         form=form, movimentacao=movimentacao, title='Editar Movimentação')

@financeiro.route('/movimentacao/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_movimentacao(id):
    """Exclui uma movimentação financeira."""
    movimentacao = Movimentacao.query.get_or_404(id)
    
    db.session.delete(movimentacao)
    db.session.commit()
    
    flash('Movimentação excluída com sucesso!', 'success')
    return redirect(url_for('financeiro.movimentacoes'))

@financeiro.route('/notas-fiscais')
@login_required
def notas_fiscais():
    """Lista todas as notas fiscais."""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '', type=str)
    tipo = request.args.get('tipo', '', type=str)
    cliente_id = request.args.get('cliente_id', '', type=str)
    
    query = NotaFiscal.query
    
    if status:
        query = query.filter_by(status=status)
    
    if tipo:
        query = query.filter_by(tipo=tipo)
    
    if cliente_id:
        query = query.filter_by(cliente_id=int(cliente_id))
    
    notas_paginadas = query.order_by(NotaFiscal.data_emissao.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Lista de clientes para o filtro
    from app.models.cliente import Cliente
    clientes = Cliente.query.filter_by(ativo=True).order_by(Cliente.nome).all()
    
    return render_template('financeiro/notas_fiscais.html',
                         notas=notas_paginadas,
                         status=status,
                         tipo=tipo,
                         cliente_id=cliente_id,
                         clientes=clientes)

@financeiro.route('/nota-fiscal/nova', methods=['GET', 'POST'])
@login_required
def nova_nota_fiscal():
    """Cria uma nova nota fiscal."""
    form = NotaFiscalForm()
    
    if form.validate_on_submit():
        nota = NotaFiscal(
            numero=form.numero.data,
            serie=form.serie.data,
            tipo=form.tipo.data,
            cliente_id=form.cliente_id.data,
            data_emissao=form.data_emissao.data,
            data_vencimento=form.data_vencimento.data,
            valor_total=form.valor_total.data,
            observacoes=form.observacoes.data,
            usuario_id=current_user.id
        )
        
        db.session.add(nota)
        db.session.commit()
        
        flash('Nota fiscal criada com sucesso!', 'success')
        return redirect(url_for('financeiro.view_nota_fiscal', id=nota.id))
    
    return render_template('financeiro/nota_fiscal_form.html', form=form, title='Nova Nota Fiscal')

@financeiro.route('/nota-fiscal/<int:id>')
@login_required
def view_nota_fiscal(id):
    """Visualiza uma nota fiscal específica."""
    nota = NotaFiscal.query.get_or_404(id)
    
    return render_template('financeiro/nota_fiscal_view.html', nota=nota)

@financeiro.route('/nota-fiscal/<int:id>/emitir', methods=['POST'])
@login_required
def emitir_nota_fiscal(id):
    """Emite uma nota fiscal via API do Bling."""
    nota = NotaFiscal.query.get_or_404(id)
    
    if nota.status != 'pendente':
        flash('Esta nota fiscal já foi processada.', 'warning')
        return redirect(url_for('financeiro.view_nota_fiscal', id=id))
    
    try:
        # Aqui seria implementada a integração com a API do Bling
        # Por enquanto, vamos simular a emissão
        nota.emitir_via_bling()
        db.session.commit()
        
        flash('Nota fiscal emitida com sucesso via Bling!', 'success')
    except Exception as e:
        flash(f'Erro ao emitir nota fiscal: {str(e)}', 'danger')
    
    return redirect(url_for('financeiro.view_nota_fiscal', id=id))

@financeiro.route('/relatorio-financeiro')
@login_required
def relatorio_financeiro():
    """Relatório financeiro detalhado."""
    # Período padrão: último trimestre
    hoje = datetime.now().date()
    inicio_trimestre = hoje - timedelta(days=90)
    
    # Parâmetros da URL
    data_inicio = request.args.get('data_inicio', inicio_trimestre.strftime('%Y-%m-%d'))
    data_fim = request.args.get('data_fim', hoje.strftime('%Y-%m-%d'))
    
    try:
        data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
    except ValueError:
        flash('Formato de data inválido.', 'danger')
        return redirect(url_for('financeiro.index'))
    
    # Movimentações por mês
    movimentacoes_mes = db.session.query(
        func.strftime('%Y-%m', Movimentacao.data).label('mes'),
        Movimentacao.tipo,
        func.sum(Movimentacao.valor).label('total')
    ).filter(
        and_(
            Movimentacao.data >= data_inicio_obj,
            Movimentacao.data <= data_fim_obj
        )
    ).group_by(
        func.strftime('%Y-%m', Movimentacao.data),
        Movimentacao.tipo
    ).order_by('mes').all()
    
    # Movimentações por categoria
    movimentacoes_categoria = db.session.query(
        Movimentacao.categoria,
        Movimentacao.tipo,
        func.sum(Movimentacao.valor).label('total')
    ).filter(
        and_(
            Movimentacao.data >= data_inicio_obj,
            Movimentacao.data <= data_fim_obj
        )
    ).group_by(Movimentacao.categoria, Movimentacao.tipo).all()
    
    # Totais gerais
    receitas_total = db.session.query(func.sum(Movimentacao.valor)).filter(
        and_(
            Movimentacao.data >= data_inicio_obj,
            Movimentacao.data <= data_fim_obj,
            Movimentacao.tipo == 'receita'
        )
    ).scalar() or Decimal('0')
    
    despesas_total = db.session.query(func.sum(Movimentacao.valor)).filter(
        and_(
            Movimentacao.data >= data_inicio_obj,
            Movimentacao.data <= data_fim_obj,
            Movimentacao.tipo == 'despesa'
        )
    ).scalar() or Decimal('0')
    
    return render_template('financeiro/relatorio.html',
                         movimentacoes_mes=movimentacoes_mes,
                         movimentacoes_categoria=movimentacoes_categoria,
                         receitas_total=receitas_total,
                         despesas_total=despesas_total,
                         saldo_total=receitas_total - despesas_total,
                         data_inicio=data_inicio,
                         data_fim=data_fim)

