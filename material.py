"""
Modelo de Material para o ERP ROMA
"""

from datetime import datetime
from app import db

class Material(db.Model):
    """Modelo de material para controle de estoque."""
    
    __tablename__ = 'materiais'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(50))  # tecido, aviamento, etc.
    
    # Estoque
    estoque_atual = db.Column(db.Numeric(10, 3), default=0.000)
    estoque_minimo = db.Column(db.Numeric(10, 3), default=0.000)
    unidade_medida = db.Column(db.String(10), default='M')  # M, UN, KG, etc.
    
    # Preços
    custo_unitario = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Fornecedor
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'))
    
    # Informações adicionais
    cor = db.Column(db.String(50))
    largura = db.Column(db.String(20))  # Para tecidos
    composicao = db.Column(db.String(100))  # Para tecidos
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    movimentacoes = db.relationship('MovimentacaoEstoque', backref='material', lazy='dynamic')
    composicoes = db.relationship('ComposicaoProduto', backref='material', lazy='dynamic')
    
    def __init__(self, codigo, nome, categoria, unidade_medida='M', custo_unitario=0.00):
        self.codigo = codigo
        self.nome = nome
        self.categoria = categoria
        self.unidade_medida = unidade_medida
        self.custo_unitario = custo_unitario
    
    def verificar_estoque_minimo(self):
        """Verifica se o estoque está abaixo do mínimo."""
        return self.estoque_atual <= self.estoque_minimo
    
    def atualizar_estoque(self, quantidade, operacao='entrada', observacao=''):
        """Atualiza o estoque do material e registra a movimentação."""
        quantidade_anterior = self.estoque_atual
        
        if operacao == 'entrada':
            self.estoque_atual += quantidade
        elif operacao == 'saida':
            self.estoque_atual -= quantidade
        
        # Não permite estoque negativo
        if self.estoque_atual < 0:
            self.estoque_atual = 0
        
        # Registra a movimentação
        movimentacao = MovimentacaoEstoque(
            material_id=self.id,
            tipo=operacao,
            quantidade=quantidade,
            quantidade_anterior=quantidade_anterior,
            quantidade_atual=self.estoque_atual,
            observacao=observacao
        )
        db.session.add(movimentacao)
    
    def calcular_valor_estoque(self):
        """Calcula o valor total do estoque atual."""
        return float(self.estoque_atual * self.custo_unitario)
    
    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'categoria': self.categoria,
            'estoque_atual': float(self.estoque_atual),
            'estoque_minimo': float(self.estoque_minimo),
            'unidade_medida': self.unidade_medida,
            'custo_unitario': float(self.custo_unitario),
            'valor_estoque': self.calcular_valor_estoque(),
            'alerta_estoque': self.verificar_estoque_minimo(),
            'ativo': self.ativo
        }
    
    def __repr__(self):
        return f'<Material {self.codigo} - {self.nome}>'


class MovimentacaoEstoque(db.Model):
    """Modelo para movimentações de estoque de materiais."""
    
    __tablename__ = 'movimentacoes_estoque'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materiais.id'), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # entrada, saida
    quantidade = db.Column(db.Numeric(10, 3), nullable=False)
    quantidade_anterior = db.Column(db.Numeric(10, 3))
    quantidade_atual = db.Column(db.Numeric(10, 3))
    observacao = db.Column(db.Text)
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    def __repr__(self):
        return f'<MovimentacaoEstoque {self.tipo} - {self.quantidade}>'

