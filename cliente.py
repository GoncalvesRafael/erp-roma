"""
Modelo de Cliente para o ERP ROMA
"""

from datetime import datetime
from app import db

class Cliente(db.Model):
    """Modelo de cliente para o ERP ROMA."""
    
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), unique=True)
    inscricao_estadual = db.Column(db.String(20))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    contato = db.Column(db.String(100))
    
    # Endereço
    cep = db.Column(db.String(10))
    logradouro = db.Column(db.String(100))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    
    # Informações adicionais
    observacoes = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    pedidos = db.relationship('Pedido', backref='cliente', lazy='dynamic')
    
    def __init__(self, nome, cnpj=None, email=None, telefone=None):
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.telefone = telefone
    
    def atualizar_endereco(self, cep, logradouro, numero, bairro, cidade, estado, complemento=None):
        """Atualiza o endereço do cliente."""
        self.cep = cep
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
    
    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'cnpj': self.cnpj,
            'email': self.email,
            'telefone': self.telefone,
            'endereco': f"{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}",
            'ativo': self.ativo
        }
    
    def __repr__(self):
        return f'<Cliente {self.nome}>'

