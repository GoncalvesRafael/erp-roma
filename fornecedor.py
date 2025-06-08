"""
Modelo de Fornecedor para o ERP ROMA
"""

from datetime import datetime
from app import db

class Fornecedor(db.Model):
    """Modelo de fornecedor para o ERP ROMA."""
    
    __tablename__ = 'fornecedores'
    
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
    
    # Informações comerciais
    prazo_entrega = db.Column(db.Integer)  # dias
    forma_pagamento = db.Column(db.String(50))
    observacoes = db.Column(db.Text)
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    materiais = db.relationship('Material', backref='fornecedor', lazy='dynamic')
    
    def __init__(self, nome, cnpj=None, email=None, telefone=None):
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.telefone = telefone
    
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
        return f'<Fornecedor {self.nome}>'


class Pedido(db.Model):
    """Modelo de pedido para o ERP ROMA."""
    
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data_pedido = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    data_entrega = db.Column(db.Date)
    
    # Valores
    valor_total = db.Column(db.Numeric(10, 2), default=0.00)
    desconto = db.Column(db.Numeric(10, 2), default=0.00)
    valor_final = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Status
    status = db.Column(db.String(20), default='pendente')  # pendente, em_producao, finalizado, cancelado
    observacoes = db.Column(db.Text)
    
    # Informações adicionais
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    itens = db.relationship('ItemPedido', backref='pedido', lazy='dynamic', cascade='all, delete-orphan')
    producoes = db.relationship('Producao', backref='pedido', lazy='dynamic')
    
    def __init__(self, numero, cliente_id, data_entrega=None):
        self.numero = numero
        self.cliente_id = cliente_id
        self.data_entrega = data_entrega
    
    def calcular_total(self):
        """Calcula o valor total do pedido."""
        self.valor_total = sum(item.calcular_subtotal() for item in self.itens)
        self.valor_final = self.valor_total - self.desconto
        return self.valor_final
    
    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'numero': self.numero,
            'cliente_id': self.cliente_id,
            'cliente': self.cliente.nome if self.cliente else None,
            'data_pedido': self.data_pedido.strftime('%d/%m/%Y'),
            'data_entrega': self.data_entrega.strftime('%d/%m/%Y') if self.data_entrega else None,
            'valor_total': float(self.valor_total),
            'valor_final': float(self.valor_final),
            'status': self.status
        }
    
    def __repr__(self):
        return f'<Pedido {self.numero}>'


class ItemPedido(db.Model):
    """Modelo para itens de pedido."""
    
    __tablename__ = 'itens_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    valor_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    descricao_personalizada = db.Column(db.Text)
    
    def calcular_subtotal(self):
        """Calcula o subtotal do item."""
        return float(self.valor_unitario) * self.quantidade
    
    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'produto': self.produto.nome if self.produto else None,
            'quantidade': self.quantidade,
            'valor_unitario': float(self.valor_unitario),
            'subtotal': self.calcular_subtotal(),
            'descricao_personalizada': self.descricao_personalizada
        }
    
    def __repr__(self):
        return f'<ItemPedido {self.produto_id} - {self.quantidade}>'

