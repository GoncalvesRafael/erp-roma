"""
ERP ROMA - Sistema de Gestão para Roma Confecções
Aplicação principal Flask
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

# Inicialização das extensões
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name=None):
    """Factory function para criar a aplicação Flask."""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG') or 'default'
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Inicialização das extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Configurações do Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    # Registro dos Blueprints (rotas)
    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.routes.usuarios import usuarios as usuarios_blueprint
    app.register_blueprint(usuarios_blueprint, url_prefix='/usuarios')
    
    from app.routes.clientes import clientes as clientes_blueprint
    app.register_blueprint(clientes_blueprint, url_prefix='/clientes')
    
    from app.routes.produtos import produtos as produtos_blueprint
    app.register_blueprint(produtos_blueprint, url_prefix='/produtos')
    
    from app.routes.producao import producao as producao_blueprint
    app.register_blueprint(producao_blueprint, url_prefix='/producao')
    
    from app.routes.estoque import estoque as estoque_blueprint
    app.register_blueprint(estoque_blueprint, url_prefix='/estoque')
    
    from app.routes.financeiro import financeiro as financeiro_blueprint
    app.register_blueprint(financeiro_blueprint, url_prefix='/financeiro')
    
    from app.routes.relatorios import relatorios as relatorios_blueprint
    app.register_blueprint(relatorios_blueprint, url_prefix='/relatorios')
    
    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

