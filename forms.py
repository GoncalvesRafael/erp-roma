"""
Formulários para o ERP ROMA
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, DecimalField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from wtforms import ValidationError
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.produto import Produto

class LoginForm(FlaskForm):
    """Formulário de login."""
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class UsuarioForm(FlaskForm):
    """Formulário para cadastro/edição de usuários."""
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(max=100)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', 
                                   validators=[DataRequired(), EqualTo('senha', message='As senhas devem ser iguais')])
    tipo = SelectField('Tipo de Usuário', 
                      choices=[('visualizador', 'Visualizador'), ('gestor', 'Gestor'), ('administrador', 'Administrador')],
                      default='visualizador')
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')
    
    def __init__(self, usuario=None, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.usuario = usuario
        
        # Se estiver editando, não exigir senha
        if usuario:
            self.senha.validators = [Optional(), Length(min=6)]
            self.confirmar_senha.validators = [Optional(), EqualTo('senha', message='As senhas devem ser iguais')]
    
    def validate_email(self, field):
        """Valida se o e-mail já não está em uso."""
        usuario = Usuario.query.filter_by(email=field.data).first()
        if usuario and (not self.usuario or usuario.id != self.usuario.id):
            raise ValidationError('Este e-mail já está em uso.')

class ClienteForm(FlaskForm):
    """Formulário para cadastro/edição de clientes."""
    nome = StringField('Nome/Razão Social', validators=[DataRequired(), Length(min=2, max=100)])
    cnpj = StringField('CNPJ', validators=[Optional(), Length(max=18)])
    inscricao_estadual = StringField('Inscrição Estadual', validators=[Optional(), Length(max=20)])
    email = StringField('E-mail', validators=[Optional(), Email(), Length(max=100)])
    telefone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    contato = StringField('Pessoa de Contato', validators=[Optional(), Length(max=100)])
    
    # Endereço
    cep = StringField('CEP', validators=[Optional(), Length(max=10)])
    logradouro = StringField('Logradouro', validators=[Optional(), Length(max=100)])
    numero = StringField('Número', validators=[Optional(), Length(max=10)])
    complemento = StringField('Complemento', validators=[Optional(), Length(max=100)])
    bairro = StringField('Bairro', validators=[Optional(), Length(max=100)])
    cidade = StringField('Cidade', validators=[Optional(), Length(max=100)])
    estado = SelectField('Estado', choices=[
        ('', 'Selecione...'),
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ], validators=[Optional()])
    
    observacoes = TextAreaField('Observações', validators=[Optional()])
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')
    
    def __init__(self, cliente=None, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.cliente = cliente
    
    def validate_cnpj(self, field):
        """Valida se o CNPJ já não está em uso."""
        if field.data:
            cliente = Cliente.query.filter_by(cnpj=field.data).first()
            if cliente and (not self.cliente or cliente.id != self.cliente.id):
                raise ValidationError('Este CNPJ já está cadastrado.')

class ProdutoForm(FlaskForm):
    """Formulário para cadastro/edição de produtos."""
    codigo = StringField('Código', validators=[DataRequired(), Length(min=1, max=20)])
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    modelo = StringField('Modelo', validators=[Optional(), Length(max=50)])
    descricao = TextAreaField('Descrição', validators=[Optional()])
    
    # Preços e custos
    custo_unitario = DecimalField('Custo Unitário (R$)', validators=[Optional(), NumberRange(min=0)], places=2)
    preco_minimo = DecimalField('Preço Mínimo (R$)', validators=[Optional(), NumberRange(min=0)], places=2)
    preco_sugerido = DecimalField('Preço Sugerido (R$)', validators=[Optional(), NumberRange(min=0)], places=2)
    
    # Estoque
    estoque_atual = IntegerField('Estoque Atual', validators=[Optional(), NumberRange(min=0)], default=0)
    estoque_minimo = IntegerField('Estoque Mínimo', validators=[Optional(), NumberRange(min=0)], default=0)
    
    # Informações adicionais
    unidade_medida = SelectField('Unidade de Medida', 
                                choices=[('UN', 'Unidade'), ('M', 'Metro'), ('KG', 'Quilograma'), ('L', 'Litro')],
                                default='UN')
    categoria = StringField('Categoria', validators=[Optional(), Length(max=50)])
    
    # Informações fiscais
    ncm = StringField('NCM', validators=[Optional(), Length(max=10)], 
                     render_kw={'placeholder': 'Ex: 62092000'})
    origem = SelectField('Origem', 
                        choices=[
                            ('0', '0 - Nacional'),
                            ('1', '1 - Estrangeira - Importação direta'),
                            ('2', '2 - Estrangeira - Adquirida no mercado interno')
                        ],
                        default='0')
    
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')
    
    def __init__(self, produto=None, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.produto = produto
    
    def validate_codigo(self, field):
        """Valida se o código já não está em uso."""
        produto = Produto.query.filter_by(codigo=field.data).first()
        if produto and (not self.produto or produto.id != self.produto.id):
            raise ValidationError('Este código já está em uso.')

class AlterarSenhaForm(FlaskForm):
    """Formulário para alterar senha do usuário."""
    senha_atual = PasswordField('Senha Atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Nova Senha', 
                                   validators=[DataRequired(), EqualTo('nova_senha', message='As senhas devem ser iguais')])
    submit = SubmitField('Alterar Senha')



class FornecedorForm(FlaskForm):
    """Formulário para cadastro/edição de fornecedores."""
    nome = StringField('Nome/Razão Social', validators=[DataRequired(), Length(min=2, max=100)])
    cnpj = StringField('CNPJ', validators=[Optional(), Length(max=18)])
    inscricao_estadual = StringField('Inscrição Estadual', validators=[Optional(), Length(max=20)])
    email = StringField('E-mail', validators=[Optional(), Email(), Length(max=100)])
    telefone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    contato = StringField('Pessoa de Contato', validators=[Optional(), Length(max=100)])
    
    # Endereço
    cep = StringField('CEP', validators=[Optional(), Length(max=10)])
    logradouro = StringField('Logradouro', validators=[Optional(), Length(max=100)])
    numero = StringField('Número', validators=[Optional(), Length(max=10)])
    complemento = StringField('Complemento', validators=[Optional(), Length(max=100)])
    bairro = StringField('Bairro', validators=[Optional(), Length(max=100)])
    cidade = StringField('Cidade', validators=[Optional(), Length(max=100)])
    estado = SelectField('Estado', choices=[
        ('', 'Selecione...'),
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ], validators=[Optional()])
    
    # Informações comerciais
    prazo_entrega = IntegerField('Prazo de Entrega (dias)', validators=[Optional(), NumberRange(min=0)])
    forma_pagamento = StringField('Forma de Pagamento', validators=[Optional(), Length(max=50)])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')
    
    def __init__(self, fornecedor=None, *args, **kwargs):
        super(FornecedorForm, self).__init__(*args, **kwargs)
        self.fornecedor = fornecedor
    
    def validate_cnpj(self, field):
        """Valida se o CNPJ já não está em uso."""
        if field.data:
            from app.models.fornecedor import Fornecedor
            fornecedor = Fornecedor.query.filter_by(cnpj=field.data).first()
            if fornecedor and (not self.fornecedor or fornecedor.id != self.fornecedor.id):
                raise ValidationError('Este CNPJ já está cadastrado.')

class MaterialForm(FlaskForm):
    """Formulário para cadastro/edição de materiais."""
    codigo = StringField('Código', validators=[DataRequired(), Length(min=1, max=20)])
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    tipo = SelectField('Tipo', 
                      choices=[('tecido', 'Tecido'), ('aviamento', 'Aviamento'), ('acessorio', 'Acessório'), ('outro', 'Outro')],
                      default='tecido')
    unidade_medida = SelectField('Unidade de Medida', 
                                choices=[('M', 'Metro'), ('UN', 'Unidade'), ('KG', 'Quilograma'), ('L', 'Litro')],
                                default='M')
    
    # Preços e estoque
    preco_unitario = DecimalField('Preço Unitário (R$)', validators=[Optional(), NumberRange(min=0)], places=2)
    estoque_atual = DecimalField('Estoque Atual', validators=[Optional(), NumberRange(min=0)], places=2, default=0)
    estoque_minimo = DecimalField('Estoque Mínimo', validators=[Optional(), NumberRange(min=0)], places=2, default=0)
    
    # Fornecedor
    fornecedor_id = SelectField('Fornecedor', coerce=int, validators=[Optional()])
    
    # Informações adicionais
    descricao = TextAreaField('Descrição', validators=[Optional()])
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')
    
    def __init__(self, material=None, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.material = material
        
        # Carrega fornecedores para o select
        from app.models.fornecedor import Fornecedor
        fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome).all()
        self.fornecedor_id.choices = [('', 'Selecione...')] + [(f.id, f.nome) for f in fornecedores]
    
    def validate_codigo(self, field):
        """Valida se o código já não está em uso."""
        from app.models.material import Material
        material = Material.query.filter_by(codigo=field.data).first()
        if material and (not self.material or material.id != self.material.id):
            raise ValidationError('Este código já está em uso.')

class ProducaoForm(FlaskForm):
    """Formulário para cadastro/edição de produção."""
    data = DateField('Data', validators=[DataRequired()], default=datetime.now().date)
    cliente_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    pedido_id = SelectField('Pedido', coerce=int, validators=[Optional()])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    submit = SubmitField('Salvar')
    
    def __init__(self, producao=None, *args, **kwargs):
        super(ProducaoForm, self).__init__(*args, **kwargs)
        self.producao = producao
        
        # Carrega clientes para o select
        from app.models.cliente import Cliente
        clientes = Cliente.query.filter_by(ativo=True).order_by(Cliente.nome).all()
        self.cliente_id.choices = [('', 'Selecione...')] + [(c.id, c.nome) for c in clientes]
        
        # Carrega pedidos para o select (será filtrado via JavaScript)
        from app.models.fornecedor import Pedido
        pedidos = Pedido.query.order_by(Pedido.numero).all()
        self.pedido_id.choices = [('', 'Selecione...')] + [(p.id, f'{p.numero} - {p.cliente.nome}') for p in pedidos]

class MovimentacaoEstoqueForm(FlaskForm):
    """Formulário para movimentação de estoque."""
    material_id = SelectField('Material', coerce=int, validators=[DataRequired()])
    tipo = SelectField('Tipo', 
                      choices=[('entrada', 'Entrada'), ('saida', 'Saída'), ('ajuste', 'Ajuste')],
                      validators=[DataRequired()])
    quantidade = DecimalField('Quantidade', validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    motivo = StringField('Motivo', validators=[DataRequired(), Length(min=2, max=200)])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    submit = SubmitField('Salvar')
    
    def __init__(self, *args, **kwargs):
        super(MovimentacaoEstoqueForm, self).__init__(*args, **kwargs)
        
        # Carrega materiais para o select
        from app.models.material import Material
        materiais = Material.query.filter_by(ativo=True).order_by(Material.nome).all()
        self.material_id.choices = [('', 'Selecione...')] + [(m.id, f'{m.codigo} - {m.nome}') for m in materiais]


class MovimentacaoForm(FlaskForm):
    """Formulário para movimentações financeiras."""
    tipo = SelectField('Tipo', 
                      choices=[('receita', 'Receita'), ('despesa', 'Despesa')],
                      validators=[DataRequired()])
    categoria = SelectField('Categoria', 
                           choices=[
                               ('vendas', 'Vendas'),
                               ('servicos', 'Serviços'),
                               ('materiais', 'Materiais'),
                               ('salarios', 'Salários'),
                               ('impostos', 'Impostos'),
                               ('aluguel', 'Aluguel'),
                               ('energia', 'Energia'),
                               ('telefone', 'Telefone'),
                               ('manutencao', 'Manutenção'),
                               ('marketing', 'Marketing'),
                               ('outros', 'Outros')
                           ],
                           validators=[DataRequired()])
    descricao = StringField('Descrição', validators=[DataRequired(), Length(min=2, max=200)])
    valor = DecimalField('Valor (R$)', validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    data = DateField('Data', validators=[DataRequired()], default=datetime.now().date)
    forma_pagamento = SelectField('Forma de Pagamento',
                                 choices=[
                                     ('dinheiro', 'Dinheiro'),
                                     ('pix', 'PIX'),
                                     ('cartao_debito', 'Cartão de Débito'),
                                     ('cartao_credito', 'Cartão de Crédito'),
                                     ('transferencia', 'Transferência'),
                                     ('boleto', 'Boleto'),
                                     ('cheque', 'Cheque')
                                 ],
                                 validators=[DataRequired()])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    submit = SubmitField('Salvar')

class NotaFiscalForm(FlaskForm):
    """Formulário para notas fiscais."""
    numero = StringField('Número', validators=[DataRequired(), Length(min=1, max=20)])
    serie = StringField('Série', validators=[DataRequired(), Length(min=1, max=10)])
    tipo = SelectField('Tipo', 
                      choices=[('saida', 'Saída'), ('entrada', 'Entrada')],
                      validators=[DataRequired()])
    cliente_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    data_emissao = DateField('Data de Emissão', validators=[DataRequired()], default=datetime.now().date)
    data_vencimento = DateField('Data de Vencimento', validators=[Optional()])
    valor_total = DecimalField('Valor Total (R$)', validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    observacoes = TextAreaField('Observações', validators=[Optional()])
    submit = SubmitField('Salvar')
    
    def __init__(self, *args, **kwargs):
        super(NotaFiscalForm, self).__init__(*args, **kwargs)
        
        # Carrega clientes para o select
        from app.models.cliente import Cliente
        clientes = Cliente.query.filter_by(ativo=True).order_by(Cliente.nome).all()
        self.cliente_id.choices = [('', 'Selecione...')] + [(c.id, c.nome) for c in clientes]

class BlingConfigForm(FlaskForm):
    """Formulário para configuração da API do Bling."""
    api_key = StringField('API Key do Bling', validators=[DataRequired(), Length(min=10, max=100)])
    situacao_padrao = SelectField('Situação Padrão das Notas',
                                 choices=[
                                     ('0', 'Em digitação'),
                                     ('1', 'Pendente'),
                                     ('2', 'Verificado'),
                                     ('3', 'Autorizado'),
                                     ('6', 'Cancelado')
                                 ],
                                 default='1')
    serie_padrao = StringField('Série Padrão', validators=[DataRequired()], default='1')
    observacoes_padrao = TextAreaField('Observações Padrão', validators=[Optional()])
    submit = SubmitField('Salvar Configuração')

