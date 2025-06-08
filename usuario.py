"""
Modelo de Usuário para o ERP ROMA
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class Usuario(UserMixin, db.Model):
    """Modelo de usuário para autenticação e controle de acesso."""
    
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128))
    tipo = db.Column(db.String(20), default='visualizador')  # administrador, gestor, visualizador
    ativo = db.Column(db.Boolean, default=True)
    ultimo_acesso = db.Column(db.DateTime)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, nome, email, senha, tipo='visualizador'):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo
    
    @property
    def senha(self):
        """Impede acesso direto à senha."""
        raise AttributeError('senha não é um atributo legível')
    
    @senha.setter
    def senha(self, senha):
        """Define a senha com hash."""
        self.senha_hash = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        """Verifica se a senha está correta."""
        return check_password_hash(self.senha_hash, senha)
    
    def is_admin(self):
        """Verifica se o usuário é administrador."""
        return self.tipo == 'administrador'
    
    def is_gestor(self):
        """Verifica se o usuário é gestor."""
        return self.tipo == 'gestor' or self.tipo == 'administrador'
    
    def registrar_acesso(self):
        """Registra o último acesso do usuário."""
        self.ultimo_acesso = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'


@login_manager.user_loader
def load_user(user_id):
    """Carrega o usuário pelo ID para o Flask-Login."""
    return Usuario.query.get(int(user_id))

