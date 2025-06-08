#!/usr/bin/env python3
"""
Script de otimização e ajustes finais para o ERP ROMA.
Este script realiza otimizações de performance e ajustes finais no sistema.
"""

import os
import sys
import sqlite3
import logging
from pathlib import Path
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/optimization.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('optimization')

# Adiciona o diretório atual ao path para importar a aplicação
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.models.material import Material
from app.models.fornecedor import Fornecedor
from app.models.producao import Producao
from app.models.financeiro import Movimentacao, NotaFiscal

class SystemOptimizer:
    """Classe para otimização do sistema."""
    
    def __init__(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
    def __del__(self):
        if hasattr(self, 'app_context'):
            self.app_context.pop()
    
    def optimize_database(self):
        """Otimiza o banco de dados."""
        logger.info("Iniciando otimização do banco de dados...")
        
        # Obtém o caminho do banco de dados
        db_path = self.app.config.get('DATABASE_URL', 'sqlite:///instance/roma.db')
        if db_path.startswith('sqlite:///'):
            db_file = db_path.replace('sqlite:///', '')
            
            if os.path.exists(db_file):
                # Conecta ao banco de dados
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Executa VACUUM para otimizar o banco
                logger.info("Executando VACUUM no banco de dados...")
                cursor.execute('VACUUM')
                
                # Executa ANALYZE para atualizar estatísticas
                logger.info("Executando ANALYZE no banco de dados...")
                cursor.execute('ANALYZE')
                
                # Cria índices para melhorar performance
                self._create_indexes(cursor)
                
                # Confirma as alterações
                conn.commit()
                conn.close()
                
                logger.info("Otimização do banco de dados concluída")
            else:
                logger.warning("Arquivo do banco de dados não encontrado")
        else:
            logger.warning("Otimização disponível apenas para SQLite")
    
    def _create_indexes(self, cursor):
        """Cria índices para melhorar performance."""
        logger.info("Criando índices para otimização...")
        
        indexes = [
            # Índices para usuários
            "CREATE INDEX IF NOT EXISTS idx_usuario_email ON usuario(email)",
            "CREATE INDEX IF NOT EXISTS idx_usuario_ativo ON usuario(ativo)",
            
            # Índices para clientes
            "CREATE INDEX IF NOT EXISTS idx_cliente_cnpj ON cliente(cnpj)",
            "CREATE INDEX IF NOT EXISTS idx_cliente_ativo ON cliente(ativo)",
            "CREATE INDEX IF NOT EXISTS idx_cliente_nome ON cliente(nome)",
            
            # Índices para produtos
            "CREATE INDEX IF NOT EXISTS idx_produto_nome ON produto(nome)",
            "CREATE INDEX IF NOT EXISTS idx_produto_ativo ON produto(ativo)",
            "CREATE INDEX IF NOT EXISTS idx_produto_estoque ON produto(estoque_atual)",
            
            # Índices para materiais
            "CREATE INDEX IF NOT EXISTS idx_material_nome ON material(nome)",
            "CREATE INDEX IF NOT EXISTS idx_material_ativo ON material(ativo)",
            "CREATE INDEX IF NOT EXISTS idx_material_estoque ON material(estoque_atual)",
            "CREATE INDEX IF NOT EXISTS idx_material_fornecedor ON material(fornecedor_id)",
            
            # Índices para fornecedores
            "CREATE INDEX IF NOT EXISTS idx_fornecedor_cnpj ON fornecedor(cnpj)",
            "CREATE INDEX IF NOT EXISTS idx_fornecedor_ativo ON fornecedor(ativo)",
            
            # Índices para produção
            "CREATE INDEX IF NOT EXISTS idx_producao_data ON producao(data)",
            "CREATE INDEX IF NOT EXISTS idx_producao_cliente ON producao(cliente_id)",
            "CREATE INDEX IF NOT EXISTS idx_producao_status ON producao(status)",
            
            # Índices para movimentações financeiras
            "CREATE INDEX IF NOT EXISTS idx_movimentacao_data ON movimentacao(data)",
            "CREATE INDEX IF NOT EXISTS idx_movimentacao_tipo ON movimentacao(tipo)",
            "CREATE INDEX IF NOT EXISTS idx_movimentacao_status ON movimentacao(status)",
            
            # Índices para notas fiscais
            "CREATE INDEX IF NOT EXISTS idx_nota_fiscal_data ON nota_fiscal(data_emissao)",
            "CREATE INDEX IF NOT EXISTS idx_nota_fiscal_cliente ON nota_fiscal(cliente_id)",
            "CREATE INDEX IF NOT EXISTS idx_nota_fiscal_status ON nota_fiscal(status)",
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
                logger.debug(f"Índice criado: {index_sql}")
            except sqlite3.Error as e:
                logger.warning(f"Erro ao criar índice: {e}")
    
    def clean_old_data(self):
        """Limpa dados antigos desnecessários."""
        logger.info("Iniciando limpeza de dados antigos...")
        
        # Remove logs antigos (mais de 90 dias)
        logs_dir = Path('logs')
        if logs_dir.exists():
            cutoff_date = datetime.now().timestamp() - (90 * 24 * 60 * 60)  # 90 dias
            
            for log_file in logs_dir.glob('*.log'):
                if log_file.stat().st_mtime < cutoff_date:
                    log_file.unlink()
                    logger.info(f"Log antigo removido: {log_file}")
        
        # Remove backups antigos (mais de 60 dias)
        backups_dir = Path('backups')
        if backups_dir.exists():
            cutoff_date = datetime.now().timestamp() - (60 * 24 * 60 * 60)  # 60 dias
            
            for backup_file in backups_dir.glob('backup_*.zip'):
                if backup_file.stat().st_mtime < cutoff_date:
                    backup_file.unlink()
                    logger.info(f"Backup antigo removido: {backup_file}")
        
        logger.info("Limpeza de dados antigos concluída")
    
    def validate_data_integrity(self):
        """Valida a integridade dos dados."""
        logger.info("Iniciando validação de integridade dos dados...")
        
        issues = []
        
        # Verifica usuários sem email
        usuarios_sem_email = Usuario.query.filter(Usuario.email.is_(None)).count()
        if usuarios_sem_email > 0:
            issues.append(f"{usuarios_sem_email} usuários sem email")
        
        # Verifica clientes sem CNPJ/CPF
        clientes_sem_documento = Cliente.query.filter(
            Cliente.cnpj.is_(None) & Cliente.cpf.is_(None)
        ).count()
        if clientes_sem_documento > 0:
            issues.append(f"{clientes_sem_documento} clientes sem documento")
        
        # Verifica produtos com estoque negativo
        produtos_estoque_negativo = Produto.query.filter(Produto.estoque_atual < 0).count()
        if produtos_estoque_negativo > 0:
            issues.append(f"{produtos_estoque_negativo} produtos com estoque negativo")
        
        # Verifica materiais com estoque negativo
        materiais_estoque_negativo = Material.query.filter(Material.estoque_atual < 0).count()
        if materiais_estoque_negativo > 0:
            issues.append(f"{materiais_estoque_negativo} materiais com estoque negativo")
        
        # Verifica produções sem itens
        producoes_sem_itens = Producao.query.filter(~Producao.itens.any()).count()
        if producoes_sem_itens > 0:
            issues.append(f"{producoes_sem_itens} produções sem itens")
        
        # Verifica movimentações com valor zero
        movimentacoes_valor_zero = Movimentacao.query.filter(Movimentacao.valor == 0).count()
        if movimentacoes_valor_zero > 0:
            issues.append(f"{movimentacoes_valor_zero} movimentações com valor zero")
        
        if issues:
            logger.warning("Problemas de integridade encontrados:")
            for issue in issues:
                logger.warning(f"  - {issue}")
        else:
            logger.info("Nenhum problema de integridade encontrado")
        
        return len(issues) == 0
    
    def update_statistics(self):
        """Atualiza estatísticas do sistema."""
        logger.info("Atualizando estatísticas do sistema...")
        
        # Calcula estatísticas
        stats = {
            'total_usuarios': Usuario.query.count(),
            'usuarios_ativos': Usuario.query.filter_by(ativo=True).count(),
            'total_clientes': Cliente.query.count(),
            'clientes_ativos': Cliente.query.filter_by(ativo=True).count(),
            'total_produtos': Produto.query.count(),
            'produtos_ativos': Produto.query.filter_by(ativo=True).count(),
            'total_materiais': Material.query.count(),
            'materiais_ativos': Material.query.filter_by(ativo=True).count(),
            'total_fornecedores': Fornecedor.query.count(),
            'fornecedores_ativos': Fornecedor.query.filter_by(ativo=True).count(),
            'total_producoes': Producao.query.count(),
            'producoes_finalizadas': Producao.query.filter_by(status='finalizada').count(),
            'total_movimentacoes': Movimentacao.query.count(),
            'total_notas_fiscais': NotaFiscal.query.count(),
        }
        
        # Salva estatísticas em arquivo
        stats_file = Path('instance/statistics.json')
        stats_file.parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2, default=str)
        
        logger.info("Estatísticas atualizadas:")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")
    
    def check_system_health(self):
        """Verifica a saúde geral do sistema."""
        logger.info("Verificando saúde do sistema...")
        
        health_issues = []
        
        # Verifica espaço em disco
        import shutil
        total, used, free = shutil.disk_usage('/')
        free_percent = (free / total) * 100
        
        if free_percent < 10:
            health_issues.append(f"Pouco espaço em disco: {free_percent:.1f}% livre")
        
        # Verifica tamanho do banco de dados
        db_path = self.app.config.get('DATABASE_URL', 'sqlite:///instance/roma.db')
        if db_path.startswith('sqlite:///'):
            db_file = db_path.replace('sqlite:///', '')
            if os.path.exists(db_file):
                db_size = os.path.getsize(db_file) / (1024 * 1024)  # MB
                if db_size > 100:  # Mais de 100MB
                    health_issues.append(f"Banco de dados grande: {db_size:.1f}MB")
        
        # Verifica logs grandes
        logs_dir = Path('logs')
        if logs_dir.exists():
            for log_file in logs_dir.glob('*.log'):
                log_size = log_file.stat().st_size / (1024 * 1024)  # MB
                if log_size > 10:  # Mais de 10MB
                    health_issues.append(f"Log grande: {log_file.name} ({log_size:.1f}MB)")
        
        # Verifica muitos backups
        backups_dir = Path('backups')
        if backups_dir.exists():
            backup_count = len(list(backups_dir.glob('backup_*.zip')))
            if backup_count > 50:
                health_issues.append(f"Muitos backups: {backup_count} arquivos")
        
        if health_issues:
            logger.warning("Problemas de saúde do sistema encontrados:")
            for issue in health_issues:
                logger.warning(f"  - {issue}")
        else:
            logger.info("Sistema em boa saúde")
        
        return len(health_issues) == 0
    
    def optimize_all(self):
        """Executa todas as otimizações."""
        logger.info("Iniciando otimização completa do sistema...")
        
        try:
            # Otimiza banco de dados
            self.optimize_database()
            
            # Limpa dados antigos
            self.clean_old_data()
            
            # Valida integridade
            integrity_ok = self.validate_data_integrity()
            
            # Atualiza estatísticas
            self.update_statistics()
            
            # Verifica saúde do sistema
            health_ok = self.check_system_health()
            
            if integrity_ok and health_ok:
                logger.info("Otimização completa concluída com sucesso!")
                return True
            else:
                logger.warning("Otimização concluída com avisos")
                return False
                
        except Exception as e:
            logger.error(f"Erro durante otimização: {str(e)}")
            return False


def main():
    """Função principal."""
    # Cria diretório de logs se não existir
    Path('logs').mkdir(parents=True, exist_ok=True)
    
    # Executa otimização
    optimizer = SystemOptimizer()
    success = optimizer.optimize_all()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())

