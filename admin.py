"""
Módulo de administração do ERP ROMA
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from app.utils.security import backup_manager, security_manager
from app.models.usuario import Usuario
from app import db
import os
from datetime import datetime
from pathlib import Path

# Criação do Blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator para verificar se o usuário é administrador."""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.perfil != 'administrador':
            flash('Acesso negado. Apenas administradores podem acessar esta área.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def index():
    """Página principal de administração."""
    # Estatísticas do sistema
    total_usuarios = Usuario.query.count()
    usuarios_ativos = Usuario.query.filter_by(ativo=True).count()
    
    # Informações de backup
    backups = backup_manager.list_backups()
    ultimo_backup = backups[0] if backups else None
    
    # Informações de segurança
    logs_security = []
    security_log_path = Path('logs/security.log')
    if security_log_path.exists():
        with open(security_log_path, 'r') as f:
            lines = f.readlines()
            logs_security = lines[-10:]  # Últimas 10 linhas
    
    return render_template('admin/index.html',
                         total_usuarios=total_usuarios,
                         usuarios_ativos=usuarios_ativos,
                         backups=backups[:5],  # Últimos 5 backups
                         ultimo_backup=ultimo_backup,
                         logs_security=logs_security)

@admin.route('/backup')
@login_required
@admin_required
def backup():
    """Página de gerenciamento de backup."""
    backups = backup_manager.list_backups()
    
    return render_template('admin/backup.html', backups=backups)

@admin.route('/backup/create', methods=['POST'])
@login_required
@admin_required
def create_backup():
    """Cria um novo backup."""
    backup_type = request.form.get('backup_type', 'incremental')
    
    # Log da ação
    security_manager.log_user_action(
        current_user.id,
        f'CREATE_BACKUP_{backup_type.upper()}',
        ip_address=request.remote_addr
    )
    
    # Cria o backup
    backup_path = backup_manager.create_backup(backup_type)
    
    if backup_path:
        flash(f'Backup {backup_type} criado com sucesso!', 'success')
    else:
        flash('Erro ao criar backup. Verifique os logs.', 'error')
    
    return redirect(url_for('admin.backup'))

@admin.route('/backup/download/<backup_name>')
@login_required
@admin_required
def download_backup(backup_name):
    """Faz download de um backup."""
    backup_path = Path(backup_manager.backup_dir) / backup_name
    
    if not backup_path.exists():
        flash('Backup não encontrado.', 'error')
        return redirect(url_for('admin.backup'))
    
    # Log da ação
    security_manager.log_user_action(
        current_user.id,
        'DOWNLOAD_BACKUP',
        details=backup_name,
        ip_address=request.remote_addr
    )
    
    return send_file(backup_path, as_attachment=True)

@admin.route('/backup/restore', methods=['POST'])
@login_required
@admin_required
def restore_backup():
    """Restaura um backup."""
    backup_name = request.form.get('backup_name')
    restore_database = request.form.get('restore_database') == 'on'
    restore_config = request.form.get('restore_config') == 'on'
    
    if not backup_name:
        flash('Selecione um backup para restaurar.', 'error')
        return redirect(url_for('admin.backup'))
    
    backup_path = Path(backup_manager.backup_dir) / backup_name
    
    if not backup_path.exists():
        flash('Backup não encontrado.', 'error')
        return redirect(url_for('admin.backup'))
    
    # Log da ação
    security_manager.log_user_action(
        current_user.id,
        'RESTORE_BACKUP',
        details=f'{backup_name} (DB: {restore_database}, Config: {restore_config})',
        ip_address=request.remote_addr
    )
    
    # Restaura o backup
    success = backup_manager.restore_backup(backup_path, restore_database, restore_config)
    
    if success:
        flash('Backup restaurado com sucesso! Reinicie o sistema.', 'success')
    else:
        flash('Erro ao restaurar backup. Verifique os logs.', 'error')
    
    return redirect(url_for('admin.backup'))

@admin.route('/backup/delete/<backup_name>', methods=['POST'])
@login_required
@admin_required
def delete_backup(backup_name):
    """Exclui um backup."""
    backup_path = Path(backup_manager.backup_dir) / backup_name
    
    if not backup_path.exists():
        flash('Backup não encontrado.', 'error')
        return redirect(url_for('admin.backup'))
    
    # Log da ação
    security_manager.log_user_action(
        current_user.id,
        'DELETE_BACKUP',
        details=backup_name,
        ip_address=request.remote_addr
    )
    
    try:
        backup_path.unlink()
        flash('Backup excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir backup: {str(e)}', 'error')
    
    return redirect(url_for('admin.backup'))

@admin.route('/security')
@login_required
@admin_required
def security():
    """Página de segurança."""
    # Lê logs de segurança
    security_logs = []
    security_log_path = Path('logs/security.log')
    
    if security_log_path.exists():
        with open(security_log_path, 'r') as f:
            lines = f.readlines()
            # Últimas 50 linhas
            for line in lines[-50:]:
                if line.strip():
                    security_logs.append(line.strip())
    
    # Estatísticas de segurança
    failed_logins = len([log for log in security_logs if 'FAILED' in log])
    successful_logins = len([log for log in security_logs if 'SUCCESS' in log])
    
    return render_template('admin/security.html',
                         security_logs=security_logs,
                         failed_logins=failed_logins,
                         successful_logins=successful_logins)

@admin.route('/security/clear-logs', methods=['POST'])
@login_required
@admin_required
def clear_security_logs():
    """Limpa logs de segurança."""
    # Log da ação antes de limpar
    security_manager.log_user_action(
        current_user.id,
        'CLEAR_SECURITY_LOGS',
        ip_address=request.remote_addr
    )
    
    try:
        security_log_path = Path('logs/security.log')
        if security_log_path.exists():
            # Cria backup do log antes de limpar
            backup_log_path = Path(f'logs/security_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
            security_log_path.rename(backup_log_path)
            
            # Cria novo arquivo de log vazio
            security_log_path.touch()
            
            flash('Logs de segurança limpos com sucesso! Backup criado.', 'success')
        else:
            flash('Arquivo de log não encontrado.', 'warning')
    except Exception as e:
        flash(f'Erro ao limpar logs: {str(e)}', 'error')
    
    return redirect(url_for('admin.security'))

@admin.route('/system')
@login_required
@admin_required
def system():
    """Página de informações do sistema."""
    import psutil
    import platform
    
    # Informações do sistema
    system_info = {
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'cpu_count': psutil.cpu_count(),
        'memory_total': round(psutil.virtual_memory().total / (1024**3), 2),  # GB
        'memory_available': round(psutil.virtual_memory().available / (1024**3), 2),  # GB
        'disk_usage': psutil.disk_usage('/'),
    }
    
    # Informações do banco de dados
    db_info = {
        'type': 'SQLite',
        'path': 'instance/roma.db',
        'size': 0
    }
    
    db_path = Path('instance/roma.db')
    if db_path.exists():
        db_info['size'] = round(db_path.stat().st_size / (1024**2), 2)  # MB
    
    # Informações de configuração
    config_info = {
        'debug': current_app.config.get('DEBUG', False),
        'secret_key_set': bool(current_app.config.get('SECRET_KEY')),
        'backup_enabled': bool(backup_manager),
        'icloud_sync': backup_manager.icloud_sync if backup_manager else False,
    }
    
    return render_template('admin/system.html',
                         system_info=system_info,
                         db_info=db_info,
                         config_info=config_info)

@admin.route('/logs')
@login_required
@admin_required
def logs():
    """Página de visualização de logs."""
    log_type = request.args.get('type', 'app')
    
    logs = []
    log_files = {
        'app': 'logs/app.log',
        'backup': 'logs/backup.log',
        'security': 'logs/security.log',
        'error': 'logs/error.log'
    }
    
    log_file = log_files.get(log_type, 'logs/app.log')
    log_path = Path(log_file)
    
    if log_path.exists():
        with open(log_path, 'r') as f:
            lines = f.readlines()
            # Últimas 100 linhas
            logs = [line.strip() for line in lines[-100:] if line.strip()]
    
    return render_template('admin/logs.html',
                         logs=logs,
                         log_type=log_type,
                         log_files=log_files)

@admin.route('/logs/download/<log_type>')
@login_required
@admin_required
def download_log(log_type):
    """Faz download de um arquivo de log."""
    log_files = {
        'app': 'logs/app.log',
        'backup': 'logs/backup.log',
        'security': 'logs/security.log',
        'error': 'logs/error.log'
    }
    
    log_file = log_files.get(log_type)
    if not log_file:
        flash('Tipo de log inválido.', 'error')
        return redirect(url_for('admin.logs'))
    
    log_path = Path(log_file)
    if not log_path.exists():
        flash('Arquivo de log não encontrado.', 'error')
        return redirect(url_for('admin.logs'))
    
    # Log da ação
    security_manager.log_user_action(
        current_user.id,
        'DOWNLOAD_LOG',
        details=log_type,
        ip_address=request.remote_addr
    )
    
    return send_file(log_path, as_attachment=True)

@admin.route('/config')
@login_required
@admin_required
def config():
    """Página de configurações do sistema."""
    return render_template('admin/config.html')

@admin.route('/config/backup', methods=['POST'])
@login_required
@admin_required
def update_backup_config():
    """Atualiza configurações de backup."""
    max_backups = request.form.get('max_backups', type=int)
    backup_interval = request.form.get('backup_interval', type=int)
    icloud_sync = request.form.get('icloud_sync') == 'on'
    icloud_dir = request.form.get('icloud_dir')
    
    # Atualiza configurações
    if max_backups:
        backup_manager.max_backups = max_backups
    
    if backup_interval:
        backup_manager.backup_interval = backup_interval
    
    backup_manager.icloud_sync = icloud_sync
    
    if icloud_dir:
        backup_manager.icloud_dir = icloud_dir
    
    # Log da ação
    security_manager.log_user_action(
        current_user.id,
        'UPDATE_BACKUP_CONFIG',
        details=f'Max: {max_backups}, Interval: {backup_interval}h, iCloud: {icloud_sync}',
        ip_address=request.remote_addr
    )
    
    flash('Configurações de backup atualizadas com sucesso!', 'success')
    return redirect(url_for('admin.config'))

@admin.route('/config/security', methods=['POST'])
@login_required
@admin_required
def update_security_config():
    """Atualiza configurações de segurança."""
    max_login_attempts = request.form.get('max_login_attempts', type=int)
    lockout_duration = request.form.get('lockout_duration', type=int)
    session_timeout = request.form.get('session_timeout', type=int)
    
    # Atualiza configurações
    if max_login_attempts:
        security_manager.max_login_attempts = max_login_attempts
    
    if lockout_duration:
        security_manager.lockout_duration = lockout_duration
    
    if session_timeout:
        security_manager.session_timeout = session_timeout
    
    # Log da ação
    security_manager.log_user_action(
        current_user.id,
        'UPDATE_SECURITY_CONFIG',
        details=f'Max attempts: {max_login_attempts}, Lockout: {lockout_duration}min, Session: {session_timeout}min',
        ip_address=request.remote_addr
    )
    
    flash('Configurações de segurança atualizadas com sucesso!', 'success')
    return redirect(url_for('admin.config'))

@admin.route('/api/system-status')
@login_required
@admin_required
def api_system_status():
    """API para status do sistema."""
    import psutil
    
    status = {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(status)

@admin.route('/api/backup-status')
@login_required
@admin_required
def api_backup_status():
    """API para status dos backups."""
    backups = backup_manager.list_backups()
    
    status = {
        'total_backups': len(backups),
        'last_backup': backups[0]['timestamp'].isoformat() if backups else None,
        'total_size_mb': sum(backup.get('size_mb', 0) for backup in backups),
        'icloud_enabled': backup_manager.icloud_sync
    }
    
    return jsonify(status)

