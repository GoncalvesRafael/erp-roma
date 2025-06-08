"""
Modelo de Produção para o ERP ROMA
"""

from datetime import datetime
from app import db

class Producao(db.Model):
    """Modelo para registro de produção."""
    
    __tablename__ = 'producoes'
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'))
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='em_producao')  # em_producao, finalizada, cancelada
    data_finalizacao = db.Column(db.DateTime)
    
    # Informações adicionais
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    itens = db.relationship('ItemProducao', backref='producao', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, data, cliente_id, pedido_id=None, observacoes=None):
        self.data = data
        self.cliente_id = cliente_id
        self.pedido_id = pedido_id
        self.observacoes = observacoes
    
    def calcular_total(self):
        """Calcula o valor total da produção."""
        return sum(item.calcular_subtotal() for item in self.itens)
    
    def finalizar(self):
        """Finaliza a produção e atualiza o estoque."""
        if self.status != 'finalizada':
            self.status = 'finalizada'
            self.data_finalizacao = datetime.utcnow()
            
            # Atualiza o estoque dos produtos
            for item in self.itens:
                produto = item.produto
                produto.atualizar_estoque(item.quantidade, 'adicionar')
                
                # Deduz os materiais utilizados
                for composicao in produto.composicoes:
                    material = composicao.material
                    quantidade_usada = composicao.quantidade * item.quantidade
                    material.atualizar_estoque(quantidade_usada, 'saida', f'Produção #{self.id}')
    
    def cancelar(self):
        """Cancela a produção."""
        if self.status != 'cancelada':
            self.status = 'cancelada'
    
    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'data': self.data.strftime('%d/%m/%Y'),
            'cliente_id': self.cliente_id,
            'cliente': self.cliente.nome if self.cliente else None,
            'pedido_id': self.pedido_id,
            'status': self.status,
            'total': self.calcular_total(),
            'itens': [item.to_dict() for item in self.itens]
        }
    
    def __repr__(self):
        return f'<Producao #{self.id} - {self.data}>'


class ItemProducao(db.Model):
    """Modelo para itens de produção."""
    
    __tablename__ = 'itens_producao'
    
    id = db.Column(db.Integer, primary_key=True)
    producao_id = db.Column(db.Integer, db.ForeignKey('producoes.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    valor_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __init__(self, produto_id, quantidade, valor_unitario=None):
        self.produto_id = produto_id
        self.quantidade = quantidade
        
        # Se o valor unitário não for fornecido, usa o preço mínimo do produto
        if valor_unitario is None:
            from app.models.produto import Produto
            produto = Produto.query.get(produto_id)
            if produto:
                self.valor_unitario = produto.preco_minimo
            else:
                self.valor_unitario = 0.00
        else:
            self.valor_unitario = valor_unitario
    
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
            'subtotal': self.calcular_subtotal()
        }
    
    def __repr__(self):
        return f'<ItemProducao {self.produto_id} - {self.quantidade}>'

