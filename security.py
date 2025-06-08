"""
Sistema de backup e segurança do ERP ROMA
"""

import os
import shutil
import sqlite3
import zipfile
import schedule
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread
import hashlib
import json
from flask import current_app
from app import db
from app.models.usuario import Usuario

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/backup.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class BackupManager:
    """Gerenciador de backup do sistema."""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializa o gerenciador de backup com a aplicação Flask."""
        self.app = app
        
        # Configurações de backup
        self.backup_dir = app.config.get('BACKUP_DIR', 'backups')
        self.max_backups = app.config.get('MAX_BACKUPS', 30)
        self.backup_interval = app.config.get('BACKUP_INTERVAL', 24)  # horas
        self.icloud_sync = app.config.get('ICLOUD_SYNC', False)
        self.icloud_dir = app.config.get('ICLOUD_DIR', '~/Library/Mobile Documents/com~apple~CloudDocs/ERP_ROMA_Backups')
        
        # Cria diretórios necessários
        self._create_directories()
        
        # Agenda backups automáticos
        self._schedule_backups()
    
    def _create_directories(self):
        """Cria os diretórios necessários para backup."""
        # Diretório de backup local
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)
        
        # Diretório de logs
        Path('logs').mkdir(parents=True, exist_ok=True)
        
        # Diretório do iCloud (se habilitado)
        if self.icloud_sync:
            icloud_path = Path(self.icloud_dir).expanduser()
            icloud_path.mkdir(parents=True, exist_ok=True)
    
    def _schedule_backups(self):
        """Agenda backups automáticos."""
        # Backup diário às 2:00 AM
        schedule.every().day.at("02:00").do(self.create_backup)
        
        # Backup semanal aos domingos às 3:00 AM
        schedule.every().sunday.at("03:00").do(self.create_full_backup)
        
        # Inicia thread para executar os agendamentos
        backup_thread = Thread(target=self._run_scheduler, daemon=True)
        backup_thread.start()
        
        logger.info("Sistema de backup automático iniciado")
    
    def _run_scheduler(self):
        """Executa o agendador de backups."""
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verifica a cada minuto
    
    def create_backup(self, backup_type='incremental'):
        """Cria um backup do sistema."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"backup_{backup_type}_{timestamp}"
            backup_path = Path(self.backup_dir) / f"{backup_name}.zip"
            
            logger.info(f"Iniciando backup {backup_type}: {backup_name}")
            
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Backup do banco de dados
                self._backup_database(zipf, backup_name)
                
                # Backup dos arquivos de configuração
                self._backup_config_files(zipf)
                
                # Backup dos logs (últimos 30 dias)
                self._backup_logs(zipf)
                
                # Backup dos uploads/anexos
                self._backup_uploads(zipf)
                
                # Metadados do backup
                self._create_backup_metadata(zipf, backup_name, backup_type)
            
            # Verifica integridade do backup
            if self._verify_backup_integrity(backup_path):
                logger.info(f"Backup criado com sucesso: {backup_path}")
                
                # Sincroniza com iCloud se habilitado
                if self.icloud_sync:
                    self._sync_to_icloud(backup_path)
                
                # Remove backups antigos
                self._cleanup_old_backups()
                
                return backup_path
            else:
                logger.error(f"Falha na verificação de integridade do backup: {backup_path}")
                backup_path.unlink()  # Remove backup corrompido
                return None
                
        except Exception as e:
            logger.error(f"Erro ao criar backup: {str(e)}")
            return None
    
    def create_full_backup(self):
        """Cria um backup completo do sistema."""
        return self.create_backup('full')
    
    def _backup_database(self, zipf, backup_name):
        """Faz backup do banco de dados."""
        db_path = self.app.config.get('DATABASE_URL', 'sqlite:///instance/roma.db')
        
        if db_path.startswith('sqlite:///'):
            # Backup do SQLite
            db_file = db_path.replace('sqlite:///', '')
            
            if os.path.exists(db_file):
                # Cria uma cópia do banco para backup
                backup_db_path = f"temp_{backup_name}.db"
                
                # Conecta ao banco original
                source_conn = sqlite3.connect(db_file)
                
                # Cria backup usando o método backup do SQLite
                backup_conn = sqlite3.connect(backup_db_path)
                source_conn.backup(backup_conn)
                
                # Fecha conexões
                source_conn.close()
                backup_conn.close()
                
                # Adiciona ao arquivo ZIP
                zipf.write(backup_db_path, 'database/roma.db')
                
                # Remove arquivo temporário
                os.remove(backup_db_path)
                
                logger.info("Backup do banco de dados SQLite concluído")
        else:
            # Para outros bancos (MySQL, PostgreSQL), usar dump
            logger.warning("Backup de bancos não-SQLite não implementado")
    
    def _backup_config_files(self, zipf):
        """Faz backup dos arquivos de configuração."""
        config_files = [
            'config.py',
            '.env',
            'requirements.txt'
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                zipf.write(config_file, f'config/{config_file}')
        
        logger.info("Backup dos arquivos de configuração concluído")
    
    def _backup_logs(self, zipf):
        """Faz backup dos logs recentes."""
        logs_dir = Path('logs')
        
        if logs_dir.exists():
            # Backup dos logs dos últimos 30 dias
            cutoff_date = datetime.now() - timedelta(days=30)
            
            for log_file in logs_dir.glob('*.log'):
                if log_file.stat().st_mtime > cutoff_date.timestamp():
                    zipf.write(log_file, f'logs/{log_file.name}')
        
        logger.info("Backup dos logs concluído")
    
    def _backup_uploads(self, zipf):
        """Faz backup dos arquivos de upload."""
        uploads_dir = Path('app/static/uploads')
        
        if uploads_dir.exists():
            for upload_file in uploads_dir.rglob('*'):
                if upload_file.is_file():
                    relative_path = upload_file.relative_to('app/static')
                    zipf.write(upload_file, f'uploads/{relative_path}')
        
        logger.info("Backup dos uploads concluído")
    
    def _create_backup_metadata(self, zipf, backup_name, backup_type):
        """Cria metadados do backup."""
        metadata = {
            'backup_name': backup_name,
            'backup_type': backup_type,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0',
            'system': 'ERP ROMA',
            'database_type': 'SQLite',
            'files_count': len(zipf.namelist()) if hasattr(zipf, 'namelist') else 0
        }
        
        # Adiciona metadados ao ZIP
        zipf.writestr('metadata.json', json.dumps(metadata, indent=2))
        
        logger.info("Metadados do backup criados")
    
    def _verify_backup_integrity(self, backup_path):
        """Verifica a integridade do backup."""
        try:
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                # Testa se o arquivo ZIP está válido
                bad_file = zipf.testzip()
                if bad_file:
                    logger.error(f"Arquivo corrompido no backup: {bad_file}")
                    return False
                
                # Verifica se os arquivos essenciais estão presentes
                required_files = ['database/roma.db', 'metadata.json']
                namelist = zipf.namelist()
                
                for required_file in required_files:
                    if required_file not in namelist:
                        logger.error(f"Arquivo essencial ausente no backup: {required_file}")
                        return False
                
                return True
                
        except Exception as e:
            logger.error(f"Erro na verificação de integridade: {str(e)}")
            return False
    
    def _sync_to_icloud(self, backup_path):
        """Sincroniza backup com iCloud."""
        try:
            icloud_path = Path(self.icloud_dir).expanduser()
            
            if icloud_path.exists():
                destination = icloud_path / backup_path.name
                shutil.copy2(backup_path, destination)
                logger.info(f"Backup sincronizado com iCloud: {destination}")
            else:
                logger.warning("Diretório do iCloud não encontrado")
                
        except Exception as e:
            logger.error(f"Erro na sincronização com iCloud: {str(e)}")
    
    def _cleanup_old_backups(self):
        """Remove backups antigos."""
        try:
            backup_dir = Path(self.backup_dir)
            backup_files = sorted(backup_dir.glob('backup_*.zip'), key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remove backups excedentes
            if len(backup_files) > self.max_backups:
                for old_backup in backup_files[self.max_backups:]:
                    old_backup.unlink()
                    logger.info(f"Backup antigo removido: {old_backup}")
            
            # Remove backups do iCloud também
            if self.icloud_sync:
                icloud_path = Path(self.icloud_dir).expanduser()
                if icloud_path.exists():
                    icloud_backups = sorted(icloud_path.glob('backup_*.zip'), key=lambda x: x.stat().st_mtime, reverse=True)
                    
                    if len(icloud_backups) > self.max_backups:
                        for old_backup in icloud_backups[self.max_backups:]:
                            old_backup.unlink()
                            logger.info(f"Backup antigo removido do iCloud: {old_backup}")
                            
        except Exception as e:
            logger.error(f"Erro na limpeza de backups antigos: {str(e)}")
    
    def restore_backup(self, backup_path, restore_database=True, restore_config=False):
        """Restaura um backup do sistema."""
        try:
            backup_path = Path(backup_path)
            
            if not backup_path.exists():
                logger.error(f"Arquivo de backup não encontrado: {backup_path}")
                return False
            
            logger.info(f"Iniciando restauração do backup: {backup_path}")
            
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                # Verifica integridade antes da restauração
                if not self._verify_backup_integrity(backup_path):
                    logger.error("Backup corrompido, restauração cancelada")
                    return False
                
                # Restaura banco de dados
                if restore_database:
                    self._restore_database(zipf)
                
                # Restaura configurações
                if restore_config:
                    self._restore_config_files(zipf)
                
                # Restaura uploads
                self._restore_uploads(zipf)
            
            logger.info("Restauração concluída com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro na restauração do backup: {str(e)}")
            return False
    
    def _restore_database(self, zipf):
        """Restaura o banco de dados."""
        db_path = self.app.config.get('DATABASE_URL', 'sqlite:///instance/roma.db')
        
        if db_path.startswith('sqlite:///'):
            db_file = db_path.replace('sqlite:///', '')
            
            # Cria backup do banco atual antes da restauração
            if os.path.exists(db_file):
                backup_current = f"{db_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(db_file, backup_current)
                logger.info(f"Backup do banco atual criado: {backup_current}")
            
            # Extrai e restaura o banco
            zipf.extract('database/roma.db', 'temp_restore')
            shutil.move('temp_restore/database/roma.db', db_file)
            
            # Remove diretório temporário
            shutil.rmtree('temp_restore')
            
            logger.info("Banco de dados restaurado")
    
    def _restore_config_files(self, zipf):
        """Restaura arquivos de configuração."""
        config_files = ['config/config.py', 'config/.env', 'config/requirements.txt']
        
        for config_file in config_files:
            try:
                zipf.extract(config_file, 'temp_restore')
                source = f"temp_restore/{config_file}"
                destination = config_file.replace('config/', '')
                
                if os.path.exists(source):
                    shutil.move(source, destination)
                    logger.info(f"Arquivo de configuração restaurado: {destination}")
                    
            except KeyError:
                # Arquivo não existe no backup
                pass
        
        # Remove diretório temporário
        if os.path.exists('temp_restore'):
            shutil.rmtree('temp_restore')
    
    def _restore_uploads(self, zipf):
        """Restaura arquivos de upload."""
        uploads_dir = Path('app/static/uploads')
        
        # Cria diretório se não existir
        uploads_dir.mkdir(parents=True, exist_ok=True)
        
        # Extrai arquivos de upload
        for file_info in zipf.infolist():
            if file_info.filename.startswith('uploads/'):
                zipf.extract(file_info, 'temp_restore')
                
                source = f"temp_restore/{file_info.filename}"
                destination = f"app/static/{file_info.filename}"
                
                # Cria diretórios necessários
                Path(destination).parent.mkdir(parents=True, exist_ok=True)
                
                if os.path.exists(source):
                    shutil.move(source, destination)
        
        # Remove diretório temporário
        if os.path.exists('temp_restore'):
            shutil.rmtree('temp_restore')
        
        logger.info("Arquivos de upload restaurados")
    
    def list_backups(self):
        """Lista todos os backups disponíveis."""
        backups = []
        
        # Backups locais
        backup_dir = Path(self.backup_dir)
        if backup_dir.exists():
            for backup_file in backup_dir.glob('backup_*.zip'):
                backup_info = self._get_backup_info(backup_file)
                backup_info['location'] = 'local'
                backups.append(backup_info)
        
        # Backups do iCloud
        if self.icloud_sync:
            icloud_path = Path(self.icloud_dir).expanduser()
            if icloud_path.exists():
                for backup_file in icloud_path.glob('backup_*.zip'):
                    backup_info = self._get_backup_info(backup_file)
                    backup_info['location'] = 'icloud'
                    backups.append(backup_info)
        
        # Ordena por data (mais recente primeiro)
        backups.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return backups
    
    def _get_backup_info(self, backup_path):
        """Obtém informações de um backup."""
        try:
            stat = backup_path.stat()
            
            backup_info = {
                'name': backup_path.name,
                'path': str(backup_path),
                'size': stat.st_size,
                'timestamp': datetime.fromtimestamp(stat.st_mtime),
                'size_mb': round(stat.st_size / (1024 * 1024), 2)
            }
            
            # Tenta ler metadados do backup
            try:
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    metadata_content = zipf.read('metadata.json')
                    metadata = json.loads(metadata_content)
                    backup_info.update(metadata)
            except:
                # Metadados não disponíveis
                pass
            
            return backup_info
            
        except Exception as e:
            logger.error(f"Erro ao obter informações do backup {backup_path}: {str(e)}")
            return {
                'name': backup_path.name,
                'path': str(backup_path),
                'error': str(e)
            }


class SecurityManager:
    """Gerenciador de segurança do sistema."""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializa o gerenciador de segurança com a aplicação Flask."""
        self.app = app
        
        # Configurações de segurança
        self.max_login_attempts = app.config.get('MAX_LOGIN_ATTEMPTS', 5)
        self.lockout_duration = app.config.get('LOCKOUT_DURATION', 30)  # minutos
        self.session_timeout = app.config.get('SESSION_TIMEOUT', 120)  # minutos
        
        # Dicionário para rastrear tentativas de login
        self.login_attempts = {}
        
        # Configura logging de segurança
        self._setup_security_logging()
    
    def _setup_security_logging(self):
        """Configura logging específico para segurança."""
        security_logger = logging.getLogger('security')
        security_handler = logging.FileHandler('logs/security.log')
        security_formatter = logging.Formatter(
            '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
        )
        security_handler.setFormatter(security_formatter)
        security_logger.addHandler(security_handler)
        security_logger.setLevel(logging.INFO)
        
        self.security_logger = security_logger
    
    def log_login_attempt(self, username, ip_address, success=True, user_agent=None):
        """Registra tentativa de login."""
        status = "SUCCESS" if success else "FAILED"
        message = f"Login {status} - User: {username}, IP: {ip_address}"
        
        if user_agent:
            message += f", User-Agent: {user_agent}"
        
        if success:
            self.security_logger.info(message)
            # Remove tentativas anteriores em caso de sucesso
            if ip_address in self.login_attempts:
                del self.login_attempts[ip_address]
        else:
            self.security_logger.warning(message)
            # Registra tentativa falhada
            self._record_failed_attempt(ip_address)
    
    def _record_failed_attempt(self, ip_address):
        """Registra tentativa de login falhada."""
        now = datetime.now()
        
        if ip_address not in self.login_attempts:
            self.login_attempts[ip_address] = []
        
        # Remove tentativas antigas (fora do período de lockout)
        cutoff_time = now - timedelta(minutes=self.lockout_duration)
        self.login_attempts[ip_address] = [
            attempt for attempt in self.login_attempts[ip_address]
            if attempt > cutoff_time
        ]
        
        # Adiciona nova tentativa
        self.login_attempts[ip_address].append(now)
    
    def is_ip_locked(self, ip_address):
        """Verifica se um IP está bloqueado."""
        if ip_address not in self.login_attempts:
            return False
        
        now = datetime.now()
        cutoff_time = now - timedelta(minutes=self.lockout_duration)
        
        # Remove tentativas antigas
        self.login_attempts[ip_address] = [
            attempt for attempt in self.login_attempts[ip_address]
            if attempt > cutoff_time
        ]
        
        # Verifica se excedeu o limite
        return len(self.login_attempts[ip_address]) >= self.max_login_attempts
    
    def get_remaining_lockout_time(self, ip_address):
        """Retorna o tempo restante de bloqueio em minutos."""
        if not self.is_ip_locked(ip_address):
            return 0
        
        if ip_address not in self.login_attempts:
            return 0
        
        # Encontra a tentativa mais antiga dentro do período
        now = datetime.now()
        cutoff_time = now - timedelta(minutes=self.lockout_duration)
        
        valid_attempts = [
            attempt for attempt in self.login_attempts[ip_address]
            if attempt > cutoff_time
        ]
        
        if not valid_attempts:
            return 0
        
        oldest_attempt = min(valid_attempts)
        unlock_time = oldest_attempt + timedelta(minutes=self.lockout_duration)
        
        if unlock_time > now:
            return int((unlock_time - now).total_seconds() / 60)
        
        return 0
    
    def log_user_action(self, user_id, action, details=None, ip_address=None):
        """Registra ação do usuário para auditoria."""
        message = f"User Action - User ID: {user_id}, Action: {action}"
        
        if details:
            message += f", Details: {details}"
        
        if ip_address:
            message += f", IP: {ip_address}"
        
        self.security_logger.info(message)
    
    def validate_password_strength(self, password):
        """Valida a força da senha."""
        errors = []
        
        if len(password) < 8:
            errors.append("A senha deve ter pelo menos 8 caracteres")
        
        if not any(c.isupper() for c in password):
            errors.append("A senha deve conter pelo menos uma letra maiúscula")
        
        if not any(c.islower() for c in password):
            errors.append("A senha deve conter pelo menos uma letra minúscula")
        
        if not any(c.isdigit() for c in password):
            errors.append("A senha deve conter pelo menos um número")
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            errors.append("A senha deve conter pelo menos um caractere especial")
        
        return len(errors) == 0, errors
    
    def generate_csrf_token(self):
        """Gera token CSRF."""
        import secrets
        return secrets.token_urlsafe(32)
    
    def validate_csrf_token(self, token, session_token):
        """Valida token CSRF."""
        return token == session_token
    
    def hash_password(self, password):
        """Gera hash da senha."""
        import bcrypt
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password, hashed):
        """Verifica senha contra hash."""
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


# Instâncias globais
backup_manager = BackupManager()
security_manager = SecurityManager()

