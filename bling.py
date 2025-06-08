"""
Módulo de configuração do Bling para o ERP ROMA
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.forms import BlingConfigForm
from app.services.bling_service import BlingService
import os
from dotenv import load_dotenv, set_key

# Criação do Blueprint
bling = Blueprint('bling', __name__, url_prefix='/bling')

@bling.route('/')
@login_required
def index():
    """Página principal de configuração do Bling."""
    # Verifica se o usuário é administrador
    if current_user.tipo != 'administrador':
        flash('Acesso restrito a administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Carrega a API Key atual
    api_key = os.getenv('BLING_API_KEY', '')
    
    # Testa a conexão com o Bling
    bling_service = BlingService()
    status_conexao, mensagem = bling_service.testar_conexao()
    
    return render_template('financeiro/bling/index.html',
                         api_key=api_key,
                         status_conexao=status_conexao,
                         mensagem=mensagem)

@bling.route('/configurar', methods=['GET', 'POST'])
@login_required
def configurar():
    """Configura a API do Bling."""
    # Verifica se o usuário é administrador
    if current_user.tipo != 'administrador':
        flash('Acesso restrito a administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = BlingConfigForm()
    
    # Preenche o formulário com os valores atuais
    if request.method == 'GET':
        form.api_key.data = os.getenv('BLING_API_KEY', '')
        form.situacao_padrao.data = os.getenv('BLING_SITUACAO_PADRAO', '1')
        form.serie_padrao.data = os.getenv('BLING_SERIE_PADRAO', '1')
        form.observacoes_padrao.data = os.getenv('BLING_OBSERVACOES_PADRAO', '')
    
    if form.validate_on_submit():
        # Salva as configurações no arquivo .env
        env_path = os.path.join(os.getcwd(), '.env')
        
        # Atualiza as variáveis de ambiente
        os.environ['BLING_API_KEY'] = form.api_key.data
        os.environ['BLING_SITUACAO_PADRAO'] = form.situacao_padrao.data
        os.environ['BLING_SERIE_PADRAO'] = form.serie_padrao.data
        os.environ['BLING_OBSERVACOES_PADRAO'] = form.observacoes_padrao.data
        
        # Salva no arquivo .env
        set_key(env_path, 'BLING_API_KEY', form.api_key.data)
        set_key(env_path, 'BLING_SITUACAO_PADRAO', form.situacao_padrao.data)
        set_key(env_path, 'BLING_SERIE_PADRAO', form.serie_padrao.data)
        set_key(env_path, 'BLING_OBSERVACOES_PADRAO', form.observacoes_padrao.data)
        
        flash('Configurações do Bling salvas com sucesso!', 'success')
        return redirect(url_for('bling.index'))
    
    return render_template('financeiro/bling/configurar.html', form=form)

@bling.route('/testar-conexao')
@login_required
def testar_conexao():
    """Testa a conexão com a API do Bling."""
    # Verifica se o usuário é administrador
    if current_user.tipo != 'administrador':
        flash('Acesso restrito a administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    bling_service = BlingService()
    status, mensagem = bling_service.testar_conexao()
    
    return jsonify({
        'status': status,
        'mensagem': mensagem
    })

@bling.route('/sincronizar-clientes')
@login_required
def sincronizar_clientes():
    """Sincroniza clientes com o Bling."""
    # Verifica se o usuário é administrador
    if current_user.tipo != 'administrador':
        flash('Acesso restrito a administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    try:
        bling_service = BlingService()
        total_clientes = bling_service.sincronizar_clientes()
        
        flash(f'{total_clientes} clientes sincronizados com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao sincronizar clientes: {str(e)}', 'danger')
    
    return redirect(url_for('bling.index'))

