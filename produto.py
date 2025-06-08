"""
Modelo de Produto para o ERP ROMA
"""

from datetime import datetime
from app import db

class Produto(db.Model):
    """Modelo de produto para o ERP ROMA."""
    
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(50))
    descricao = db.Column(db.Text)
    
    # Preços e custos
    custo_unitario = db.Column(db.Numeric(10, 2), default=0.00)
    preco_minimo = db.Column(db.Numeric(10, 2), default=0.00)
    preco_sugerido = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Estoque
    estoque_atual = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=0)
    
    # Informações fiscais
    ncm = db.Column(db.String(10), nullable=True)  # Nomenclatura Comum do Mercosul
    origem = db.Column(db.Integer, default=0)  # Origem do produto (0-Nacional)
    
    # Informações adicionais
    unidade_medida = db.Column(db.String(10), default='UN')
    categoria = db.Column(db.String(50))
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    composicoes = db.relationship('ComposicaoProduto', backref='produto', lazy='dynamic', cascade='all, delete-orphan')
    itens_producao = db.relationship('ItemProducao', backref='produto', lazy='dynamic')
    
    def __init__(self, codigo, nome, modelo=None, custo_unitario=0.00, preco_minimo=0.00):
        self.codigo = codigo
        self.nome = nome
        self.modelo = modelo
        self.custo_unitario = custo_unitario
        self.preco_minimo = preco_minimo
    
    def calcular_margem(self, preco_venda):
        """Calcula a margem de lucro baseada no preço de venda."""
        if self.custo_unitario > 0:
            return ((preco_venda - self.custo_unitario) / preco_venda) * 100
        return 0
    
    def verificar_estoque_minimo(self):
        """Verifica se o estoque está abaixo do mínimo."""
        return self.estoque_atual <= self.estoque_minimo
    
    def atualizar_estoque(self, quantidade, operacao='adicionar'):
        """Atualiza o estoque do produto."""
        if operacao == 'adicionar':
            self.estoque_atual += quantidade
        elif operacao == 'subtrair':
            self.estoque_atual -= quantidade
        
        # Não permite estoque negativo
        if self.estoque_atual < 0:
            self.estoque_atual = 0
    
    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'modelo': self.modelo,
            'custo_unitario': float(self.custo_unitario),
            'preco_minimo': float(self.preco_minimo),
            'estoque_atual': self.estoque_atual,
            'estoque_minimo': self.estoque_minimo,
            'alerta_estoque': self.verificar_estoque_minimo(),
            'ativo': self.ativo
        }
    
    def __repr__(self):
        return f'<Produto {self.codigo} - {self.nome}>'


class ComposicaoProduto(db.Model):
    """Modelo para composição de materiais do produto."""
    
    __tablename__ = 'composicao_produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materiais.id'), nullable=False)
    quantidade = db.Column(db.Numeric(10, 3), nullable=False)
    unidade = db.Column(db.String(10), default='UN')
    
    def __repr__(self):
        return f'<ComposicaoProduto {self.produto_id} - {self.material_id}>'

