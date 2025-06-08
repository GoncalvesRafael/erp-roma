# Documentação Técnica - ERP ROMA

**Sistema de Gestão Empresarial para Roma Confecções**

---

**Versão:** 1.0  
**Data:** Dezembro 2024  
**Autor:** Manus AI  
**Empresa:** Roma Confecções  

---

## Sumário

1. [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
2. [Tecnologias Utilizadas](#tecnologias-utilizadas)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Banco de Dados](#banco-de-dados)
5. [API e Integrações](#api-e-integrações)
6. [Segurança](#segurança)
7. [Instalação e Configuração](#instalação-e-configuração)
8. [Manutenção](#manutenção)
9. [Monitoramento](#monitoramento)
10. [Troubleshooting](#troubleshooting)

---

## Visão Geral da Arquitetura

O ERP ROMA foi desenvolvido seguindo uma arquitetura modular e escalável, baseada no padrão MVC (Model-View-Controller) e utilizando tecnologias web modernas. A aplicação é construída como uma aplicação web monolítica com componentes bem definidos e separação clara de responsabilidades.

### Arquitetura de Alto Nível

A arquitetura do sistema é composta por três camadas principais:

**Camada de Apresentação (Frontend)**: Responsável pela interface de usuário, implementada com HTML5, CSS3 (TailwindCSS) e JavaScript vanilla. Esta camada se comunica com o backend através de requisições HTTP e formulários web tradicionais.

**Camada de Aplicação (Backend)**: Implementada em Python utilizando o framework Flask, esta camada contém toda a lógica de negócio, controle de acesso, validações e orquestração de operações. É organizada em blueprints para modularidade.

**Camada de Dados**: Utiliza SQLite como sistema de gerenciamento de banco de dados, com SQLAlchemy como ORM (Object-Relational Mapping) para abstração e manipulação de dados.

### Padrões Arquiteturais

O sistema segue diversos padrões arquiteturais estabelecidos:

**MVC (Model-View-Controller)**: Separação clara entre modelos de dados (SQLAlchemy models), visualizações (templates Jinja2) e controladores (Flask routes).

**Repository Pattern**: Implementado através do SQLAlchemy ORM, abstraindo o acesso aos dados e facilitando testes e manutenção.

**Dependency Injection**: Utilizado para configuração de componentes como banco de dados, autenticação e serviços externos.

**Service Layer**: Serviços específicos como integração com Bling e gerenciamento de backup são implementados como classes de serviço independentes.

### Escalabilidade e Performance

Embora seja uma aplicação monolítica, o ERP ROMA foi projetado com considerações de escalabilidade:

**Modularidade**: A organização em blueprints permite fácil separação de funcionalidades em microserviços futuros, se necessário.

**Caching**: Implementação de cache em memória para consultas frequentes e dados relativamente estáticos.

**Otimização de Banco**: Índices apropriados e consultas otimizadas para garantir performance mesmo com crescimento dos dados.

**Compressão**: Recursos estáticos são servidos com compressão gzip para reduzir tempo de carregamento.

---

## Tecnologias Utilizadas

### Backend

**Python 3.11**: Linguagem de programação principal, escolhida por sua produtividade, legibilidade e ecossistema robusto para desenvolvimento web.

**Flask 3.0.3**: Framework web minimalista e flexível, adequado para aplicações de médio porte como o ERP ROMA. Oferece simplicidade sem sacrificar funcionalidades essenciais.

**SQLAlchemy 2.0**: ORM moderno e poderoso que fornece abstração de banco de dados, migrations automáticas e consultas type-safe.

**Flask-Login**: Extensão para gerenciamento de sessões de usuário e autenticação, integrada ao sistema de permissões.

**Flask-WTF**: Extensão para criação e validação de formulários web com proteção CSRF automática.

**Flask-Migrate**: Ferramenta para versionamento e migração de esquemas de banco de dados.

**Werkzeug**: Biblioteca WSGI que fornece utilitários para desenvolvimento web, incluindo debugging e serving de arquivos estáticos.

**Jinja2**: Engine de templates poderoso e flexível, utilizado para renderização de páginas HTML dinâmicas.

### Frontend

**HTML5**: Marcação semântica moderna com suporte a recursos avançados como validação de formulários e APIs web.

**TailwindCSS 3.0**: Framework CSS utility-first que permite desenvolvimento rápido de interfaces responsivas e modernas.

**JavaScript ES6+**: Linguagem de programação client-side para interatividade, validações e comunicação assíncrona.

**Chart.js**: Biblioteca para criação de gráficos interativos e responsivos nos dashboards e relatórios.

### Banco de Dados

**SQLite 3**: Sistema de gerenciamento de banco de dados relacional embarcado, ideal para aplicações de pequeno a médio porte. Oferece ACID compliance, performance adequada e simplicidade de manutenção.

### Integrações

**Requests**: Biblioteca Python para comunicação HTTP com APIs externas, utilizada principalmente para integração com o Bling.

**ReportLab**: Biblioteca para geração de documentos PDF, utilizada na criação de relatórios e documentos exportáveis.

**Pillow**: Biblioteca para manipulação de imagens, utilizada no processamento de logos e gráficos.

### Desenvolvimento e Deploy

**Git**: Sistema de controle de versão distribuído para gerenciamento de código fonte.

**pip**: Gerenciador de pacotes Python para instalação e gerenciamento de dependências.

**virtualenv**: Ferramenta para criação de ambientes Python isolados, garantindo consistência entre desenvolvimento e produção.

### Segurança

**bcrypt**: Algoritmo de hash para senhas, oferecendo proteção robusta contra ataques de força bruta.

**HTTPS/TLS**: Protocolo de comunicação segura para proteção de dados em trânsito.

**CSRF Protection**: Proteção automática contra ataques Cross-Site Request Forgery através do Flask-WTF.

---

## Estrutura do Projeto

A estrutura do projeto ERP ROMA foi organizada seguindo as melhores práticas de desenvolvimento Python e Flask, com separação clara de responsabilidades e modularidade.

```
roma_sistema/
├── app/                          # Aplicação principal
│   ├── __init__.py              # Configuração da aplicação Flask
│   ├── models/                  # Modelos de dados (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── usuario.py           # Modelo de usuário
│   │   ├── cliente.py           # Modelo de cliente
│   │   ├── produto.py           # Modelo de produto
│   │   ├── material.py          # Modelo de material
│   │   ├── fornecedor.py        # Modelo de fornecedor
│   │   ├── producao.py          # Modelo de produção
│   │   └── financeiro.py        # Modelos financeiros
│   ├── routes/                  # Controladores (Blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py              # Autenticação
│   │   ├── main.py              # Rotas principais
│   │   ├── usuarios.py          # CRUD de usuários
│   │   ├── clientes.py          # CRUD de clientes
│   │   ├── produtos.py          # CRUD de produtos
│   │   ├── fornecedores.py      # CRUD de fornecedores
│   │   ├── estoque.py           # Gestão de estoque
│   │   ├── producao.py          # Gestão de produção
│   │   ├── financeiro.py        # Gestão financeira
│   │   ├── dashboard.py         # Dashboard e relatórios
│   │   ├── admin.py             # Administração
│   │   └── bling.py             # Integração Bling
│   ├── services/                # Serviços de negócio
│   │   ├── __init__.py
│   │   └── bling_service.py     # Serviço de integração Bling
│   ├── utils/                   # Utilitários
│   │   ├── __init__.py
│   │   └── security.py          # Backup e segurança
│   ├── static/                  # Arquivos estáticos
│   │   ├── css/
│   │   │   └── style.css        # Estilos customizados
│   │   ├── js/
│   │   │   └── app.js           # JavaScript da aplicação
│   │   └── img/                 # Imagens e logos
│   │       ├── logo_roma.png
│   │       ├── logo_login.png
│   │       └── icon_roma.png
│   └── templates/               # Templates HTML (Jinja2)
│       ├── base.html            # Template base
│       ├── dashboard.html       # Dashboard principal
│       ├── auth/                # Templates de autenticação
│       ├── usuarios/            # Templates de usuários
│       ├── clientes/            # Templates de clientes
│       ├── produtos/            # Templates de produtos
│       ├── fornecedores/        # Templates de fornecedores
│       ├── estoque/             # Templates de estoque
│       ├── producao/            # Templates de produção
│       ├── financeiro/          # Templates financeiros
│       └── dashboard/           # Templates de relatórios
├── instance/                    # Dados da instância
│   └── roma_erp.db             # Banco de dados SQLite
├── migrations/                  # Migrações de banco
├── docs/                        # Documentação
│   ├── manual_usuario.md        # Manual do usuário
│   ├── documentacao_tecnica.md  # Esta documentação
│   └── integracao_bling.md      # Documentação da integração Bling
├── app.py                       # Ponto de entrada da aplicação
├── config.py                    # Configurações da aplicação
├── requirements.txt             # Dependências Python
├── init_db.py                   # Script de inicialização do banco
├── tests.py                     # Testes automatizados
├── optimize.py                  # Script de otimização
├── .env                         # Variáveis de ambiente
└── README.md                    # Documentação básica
```

### Organização dos Módulos

**app/__init__.py**: Contém a factory function que cria e configura a aplicação Flask, registra blueprints, configura extensões e define configurações globais.

**models/**: Contém todos os modelos de dados SQLAlchemy, organizados por domínio. Cada arquivo define as tabelas, relacionamentos e métodos de negócio específicos.

**routes/**: Implementa os controladores da aplicação organizados em blueprints. Cada blueprint é responsável por um conjunto relacionado de funcionalidades.

**services/**: Contém serviços de negócio que encapsulam lógicas complexas ou integrações com sistemas externos.

**utils/**: Utilitários e funções auxiliares utilizadas em diferentes partes da aplicação.

**static/**: Arquivos estáticos servidos diretamente pelo servidor web, incluindo CSS, JavaScript e imagens.

**templates/**: Templates Jinja2 organizados por módulo, seguindo a estrutura dos blueprints.

### Convenções de Nomenclatura

**Arquivos Python**: snake_case (ex: usuario.py, bling_service.py)
**Classes**: PascalCase (ex: Usuario, BlingService)
**Funções e variáveis**: snake_case (ex: criar_usuario, api_key)
**Constantes**: UPPER_SNAKE_CASE (ex: DEFAULT_PAGE_SIZE)
**Templates**: snake_case com extensão .html (ex: lista_usuarios.html)
**Rotas URL**: kebab-case (ex: /usuarios/novo, /relatorios/producao)

---

## Banco de Dados

O ERP ROMA utiliza SQLite como sistema de gerenciamento de banco de dados, com SQLAlchemy como ORM para abstração e manipulação de dados. Esta seção detalha a estrutura do banco, relacionamentos e estratégias de otimização.

### Modelo de Dados

O modelo de dados foi projetado para refletir fielmente os processos de negócio da Roma Confecções, garantindo integridade referencial e performance adequada.

#### Tabela: usuarios

```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    perfil VARCHAR(20) NOT NULL DEFAULT 'visualizador',
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultimo_acesso DATETIME,
    criado_por INTEGER,
    FOREIGN KEY (criado_por) REFERENCES usuarios(id)
);
```

A tabela de usuários armazena informações de autenticação e autorização. O campo `perfil` define as permissões (administrador, gestor, visualizador), enquanto `ativo` permite desabilitar contas sem excluí-las.

#### Tabela: clientes

```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_pessoa VARCHAR(1) NOT NULL CHECK (tipo_pessoa IN ('F', 'J')),
    nome VARCHAR(200) NOT NULL,
    nome_fantasia VARCHAR(200),
    documento VARCHAR(18) UNIQUE NOT NULL,
    rg VARCHAR(20),
    inscricao_estadual VARCHAR(20),
    inscricao_municipal VARCHAR(20),
    email VARCHAR(120) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    telefone_secundario VARCHAR(20),
    cep VARCHAR(10),
    logradouro VARCHAR(200),
    numero VARCHAR(10),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    criado_por INTEGER NOT NULL,
    FOREIGN KEY (criado_por) REFERENCES usuarios(id)
);
```

A tabela de clientes suporta tanto pessoas físicas quanto jurídicas através do campo `tipo_pessoa`. O campo `documento` armazena CPF ou CNPJ conforme o tipo.

#### Tabela: produtos

```sql
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(100),
    preco_venda DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    estoque_atual INTEGER NOT NULL DEFAULT 0,
    estoque_minimo INTEGER NOT NULL DEFAULT 0,
    ncm VARCHAR(10) NOT NULL DEFAULT '62092000',
    origem INTEGER NOT NULL DEFAULT 0,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    criado_por INTEGER NOT NULL,
    FOREIGN KEY (criado_por) REFERENCES usuarios(id)
);
```

A tabela de produtos inclui informações fiscais obrigatórias como NCM e origem, essenciais para emissão de notas fiscais.

#### Tabela: materiais

```sql
CREATE TABLE materiais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(100),
    unidade_medida VARCHAR(10) NOT NULL DEFAULT 'UN',
    preco_unitario DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    estoque_atual DECIMAL(10,3) NOT NULL DEFAULT 0.000,
    estoque_minimo DECIMAL(10,3) NOT NULL DEFAULT 0.000,
    fornecedor_id INTEGER,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    criado_por INTEGER NOT NULL,
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id),
    FOREIGN KEY (criado_por) REFERENCES usuarios(id)
);
```

A tabela de materiais utiliza DECIMAL para estoque para suportar quantidades fracionárias (metros de tecido, quilos de material, etc.).

#### Tabela: produto_composicao

```sql
CREATE TABLE produto_composicao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantidade DECIMAL(10,3) NOT NULL,
    data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES materiais(id),
    UNIQUE(produto_id, material_id)
);
```

Esta tabela de relacionamento define a composição de materiais necessários para cada produto, fundamental para cálculo de custos e controle de estoque.

#### Tabela: producoes

```sql
CREATE TABLE producoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero VARCHAR(20) UNIQUE NOT NULL,
    data_producao DATE NOT NULL,
    cliente_id INTEGER NOT NULL,
    valor_total DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    status VARCHAR(20) NOT NULL DEFAULT 'em_andamento',
    observacoes TEXT,
    data_finalizacao DATETIME,
    finalizada_por INTEGER,
    data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    criado_por INTEGER NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (finalizada_por) REFERENCES usuarios(id),
    FOREIGN KEY (criado_por) REFERENCES usuarios(id)
);
```

A tabela de produções controla o processo produtivo, com status que evolui de "em_andamento" para "finalizada" ou "cancelada".

#### Tabela: producao_itens

```sql
CREATE TABLE producao_itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producao_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL,
    valor_total DECIMAL(12,2) NOT NULL,
    data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producao_id) REFERENCES producoes(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);
```

Esta tabela detalha os itens produzidos em cada produção, permitindo produções com múltiplos produtos.

### Relacionamentos e Integridade

O modelo de dados implementa relacionamentos bem definidos com integridade referencial:

**Um para Muitos**: Cliente → Produções, Produto → Itens de Produção, Usuário → Registros Criados
**Muitos para Muitos**: Produto ↔ Material (através de produto_composicao)
**Referências Opcionais**: Material → Fornecedor (um material pode não ter fornecedor definido)

### Índices e Otimização

O banco de dados inclui índices estratégicos para otimizar consultas frequentes:

```sql
-- Índices para busca e filtros
CREATE INDEX idx_clientes_documento ON clientes(documento);
CREATE INDEX idx_clientes_email ON clientes(email);
CREATE INDEX idx_clientes_ativo ON clientes(ativo);
CREATE INDEX idx_produtos_nome ON produtos(nome);
CREATE INDEX idx_produtos_categoria ON produtos(categoria);
CREATE INDEX idx_producoes_data ON producoes(data_producao);
CREATE INDEX idx_producoes_cliente ON producoes(cliente_id);
CREATE INDEX idx_producoes_status ON producoes(status);

-- Índices compostos para consultas complexas
CREATE INDEX idx_producoes_data_cliente ON producoes(data_producao, cliente_id);
CREATE INDEX idx_estoque_baixo ON produtos(estoque_atual, estoque_minimo) 
    WHERE estoque_atual <= estoque_minimo;
```

### Triggers e Validações

O banco implementa triggers para manter consistência automática:

```sql
-- Trigger para atualizar valor total da produção
CREATE TRIGGER update_producao_total 
AFTER INSERT ON producao_itens
BEGIN
    UPDATE producoes 
    SET valor_total = (
        SELECT COALESCE(SUM(valor_total), 0) 
        FROM producao_itens 
        WHERE producao_id = NEW.producao_id
    )
    WHERE id = NEW.producao_id;
END;

-- Trigger para consumo de materiais na finalização
CREATE TRIGGER consumir_materiais_producao
AFTER UPDATE OF status ON producoes
WHEN NEW.status = 'finalizada' AND OLD.status = 'em_andamento'
BEGIN
    -- Lógica de consumo de materiais implementada na aplicação
    -- por ser mais complexa e requerer validações específicas
END;
```

---

## API e Integrações

O ERP ROMA implementa integrações com sistemas externos através de APIs REST, sendo a principal integração com o sistema Bling para emissão de notas fiscais. Esta seção detalha a arquitetura de integração e as APIs disponíveis.

### Integração com Bling

A integração com o Bling permite emissão automática de notas fiscais diretamente do ERP ROMA, eliminando retrabalho e garantindo conformidade fiscal.

#### Arquitetura da Integração

A integração é implementada através da classe `BlingService` localizada em `app/services/bling_service.py`. Esta classe encapsula toda a comunicação com a API do Bling, incluindo autenticação, formatação de dados e tratamento de erros.

```python
class BlingService:
    def __init__(self, api_key=None):
        self.api_key = api_key or current_app.config.get('BLING_API_KEY')
        self.base_url = 'https://bling.com.br/Api/v2'
        self.session = requests.Session()
        
    def emitir_nota_fiscal(self, nota_fiscal_data):
        """Emite nota fiscal através da API do Bling"""
        xml_data = self._montar_xml_nota_fiscal(nota_fiscal_data)
        response = self._fazer_requisicao('notafiscal', xml_data)
        return self._processar_resposta_emissao(response)
```

#### Mapeamento de Dados

O sistema realiza mapeamento automático entre os dados do ERP ROMA e o formato exigido pela API do Bling:

**Cliente**: Dados cadastrais são mapeados para os campos obrigatórios da nota fiscal, incluindo validação de CNPJ/CPF e formatação de endereço.

**Produtos**: Informações de produtos são convertidas para itens da nota fiscal, incluindo NCM, origem, valores e quantidades.

**Impostos**: Cálculos automáticos de impostos baseados no tipo de cliente e produto, seguindo as regras fiscais brasileiras.

#### Tratamento de Erros

A integração implementa tratamento robusto de erros:

```python
def _fazer_requisicao(self, endpoint, data):
    try:
        response = self.session.post(
            f"{self.base_url}/{endpoint}",
            data=data,
            timeout=30
        )
        response.raise_for_status()
        return response
    except requests.exceptions.Timeout:
        raise BlingTimeoutError("Timeout na comunicação com Bling")
    except requests.exceptions.ConnectionError:
        raise BlingConnectionError("Erro de conexão com Bling")
    except requests.exceptions.HTTPError as e:
        raise BlingAPIError(f"Erro HTTP {e.response.status_code}")
```

#### Configuração da Integração

A configuração da integração é realizada através do painel administrativo:

1. **API Key**: Chave de acesso fornecida pelo Bling
2. **Ambiente**: Produção ou homologação
3. **Certificado**: Certificado digital para assinatura (se aplicável)
4. **Parâmetros Fiscais**: Configurações específicas da empresa

### API Interna do ERP ROMA

O sistema expõe uma API REST interna para comunicação entre módulos e futuras integrações:

#### Endpoints de Consulta

```python
# Busca de clientes para seleção
GET /api/clientes/buscar?q=termo_busca
Response: [{"id": 1, "nome": "Cliente", "documento": "12345678000100"}]

# Busca de produtos para seleção  
GET /api/produtos/buscar?q=termo_busca
Response: [{"id": 1, "nome": "Produto", "preco": 100.00, "estoque": 50}]

# Verificação de estoque
GET /api/estoque/verificar?produto_id=1&quantidade=10
Response: {"disponivel": true, "estoque_atual": 50}
```

#### Endpoints de Ação

```python
# Finalizar produção
POST /api/producao/finalizar
Body: {"producao_id": 1}
Response: {"success": true, "message": "Produção finalizada"}

# Emitir nota fiscal
POST /api/notas-fiscais/emitir
Body: {"cliente_id": 1, "itens": [...]}
Response: {"numero": "123", "chave_acesso": "...", "pdf_url": "..."}
```

#### Autenticação da API

A API interna utiliza autenticação baseada em sessão, aproveitando o sistema de login existente. Para integrações futuras, pode ser implementada autenticação via token JWT.

### Logs de Integração

Todas as comunicações com sistemas externos são registradas em logs detalhados:

```python
def _log_requisicao(self, endpoint, data, response):
    log_entry = {
        'timestamp': datetime.utcnow(),
        'endpoint': endpoint,
        'request_data': self._sanitize_data(data),
        'response_status': response.status_code,
        'response_data': response.text[:1000],  # Primeiros 1000 chars
        'user_id': current_user.id if current_user.is_authenticated else None
    }
    logger.info(f"Bling API: {log_entry}")
```

### Monitoramento de Integrações

O sistema monitora a saúde das integrações através de:

**Health Checks**: Verificações periódicas de conectividade com APIs externas
**Métricas**: Tempo de resposta, taxa de sucesso, volume de requisições
**Alertas**: Notificações automáticas em caso de falhas ou degradação de performance

---

## Segurança

A segurança do ERP ROMA foi implementada seguindo as melhores práticas da indústria, com múltiplas camadas de proteção para garantir a confidencialidade, integridade e disponibilidade dos dados da Roma Confecções.

### Autenticação e Autorização

#### Sistema de Autenticação

O sistema utiliza autenticação baseada em sessão com as seguintes características:

**Hash de Senhas**: Todas as senhas são armazenadas utilizando bcrypt com salt aleatório, tornando impraticável a recuperação da senha original mesmo em caso de comprometimento do banco de dados.

```python
from werkzeug.security import generate_password_hash, check_password_hash

def set_password(self, password):
    self.senha_hash = generate_password_hash(password)
    
def check_password(self, password):
    return check_password_hash(self.senha_hash, password)
```

**Política de Senhas**: Senhas devem atender critérios mínimos de segurança:
- Mínimo de 8 caracteres
- Pelo menos uma letra maiúscula
- Pelo menos uma letra minúscula  
- Pelo menos um número
- Pelo menos um caractere especial

**Bloqueio de Conta**: Após 5 tentativas de login malsucedidas, a conta é temporariamente bloqueada por 15 minutos, protegendo contra ataques de força bruta.

#### Controle de Acesso

O sistema implementa controle de acesso baseado em perfis (RBAC - Role-Based Access Control):

**Administrador**: Acesso completo a todas as funcionalidades, incluindo gerenciamento de usuários e configurações do sistema.

**Gestor**: Acesso às funcionalidades operacionais (clientes, produtos, produção, financeiro) mas sem acesso às configurações administrativas.

**Visualizador**: Acesso apenas para consulta de dados e relatórios, sem permissão para criar, editar ou excluir registros.

```python
from functools import wraps
from flask_login import current_user

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_permission(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/admin/usuarios')
@require_permission('admin')
def admin_usuarios():
    # Funcionalidade restrita a administradores
    pass
```

### Proteção Contra Ataques

#### CSRF Protection

Todas as operações que modificam dados são protegidas contra ataques CSRF (Cross-Site Request Forgery) através do Flask-WTF:

```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# Todos os formulários incluem token CSRF automaticamente
class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    # Token CSRF é adicionado automaticamente
```

#### XSS Protection

Proteção contra XSS (Cross-Site Scripting) através de:

**Escape Automático**: O Jinja2 escapa automaticamente todas as variáveis renderizadas nos templates.

**Content Security Policy**: Headers CSP restringem a execução de scripts não autorizados.

**Validação de Entrada**: Todos os dados de entrada são validados e sanitizados antes do processamento.

#### SQL Injection Protection

O uso do SQLAlchemy ORM elimina virtualmente o risco de injeção SQL, pois todas as consultas são parametrizadas:

```python
# Consulta segura através do ORM
clientes = Cliente.query.filter(
    Cliente.nome.ilike(f'%{termo_busca}%')
).all()

# Em vez de concatenação insegura:
# query = f"SELECT * FROM clientes WHERE nome LIKE '%{termo_busca}%'"
```

### Comunicação Segura

#### HTTPS/TLS

Toda comunicação entre cliente e servidor é criptografada usando HTTPS/TLS:

**Certificado SSL**: Certificado válido configurado no servidor web
**Redirecionamento**: Requisições HTTP são automaticamente redirecionadas para HTTPS
**HSTS**: Header Strict-Transport-Security força uso de HTTPS

```python
from flask_talisman import Talisman

# Configuração de segurança de headers
Talisman(app, force_https=True)
```

#### Proteção de Dados Sensíveis

**Variáveis de Ambiente**: Informações sensíveis como chaves de API são armazenadas em variáveis de ambiente, não no código.

**Logs Sanitizados**: Dados sensíveis são removidos ou mascarados nos logs do sistema.

**Backup Criptografado**: Backups são criptografados antes do armazenamento.

### Auditoria e Monitoramento

#### Logs de Auditoria

Todas as ações significativas são registradas em logs de auditoria:

```python
def log_action(action, resource_type, resource_id, details=None):
    audit_log = AuditLog(
        user_id=current_user.id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        timestamp=datetime.utcnow()
    )
    db.session.add(audit_log)
    db.session.commit()
```

#### Monitoramento de Segurança

**Detecção de Anomalias**: Monitoramento de padrões suspeitos de acesso
**Alertas Automáticos**: Notificações em caso de eventos de segurança
**Relatórios de Segurança**: Relatórios periódicos sobre atividades de segurança

### Backup e Recuperação

#### Estratégia de Backup

**Backup Automático**: Backups diários, semanais e mensais automatizados
**Criptografia**: Todos os backups são criptografados com AES-256
**Redundância**: Armazenamento local e na nuvem (iCloud para usuários Mac)
**Teste de Integridade**: Verificação automática da integridade dos backups

#### Plano de Recuperação

**RTO (Recovery Time Objective)**: Tempo máximo de 4 horas para restauração completa
**RPO (Recovery Point Objective)**: Perda máxima de 24 horas de dados
**Procedimentos Documentados**: Procedimentos detalhados para diferentes cenários de recuperação

### Conformidade e Regulamentações

#### LGPD (Lei Geral de Proteção de Dados)

**Minimização de Dados**: Coleta apenas dados necessários para as operações
**Consentimento**: Usuários são informados sobre o uso de seus dados
**Direito ao Esquecimento**: Funcionalidade para exclusão de dados pessoais
**Portabilidade**: Capacidade de exportar dados em formato estruturado

#### Segurança Fiscal

**Integridade de Notas Fiscais**: Assinatura digital e verificação de integridade
**Logs Fiscais**: Registro detalhado de todas as operações fiscais
**Backup de Documentos**: Armazenamento seguro de documentos fiscais

---

## Instalação e Configuração

Esta seção fornece instruções detalhadas para instalação, configuração e deploy do ERP ROMA em diferentes ambientes.

### Requisitos do Sistema

#### Requisitos Mínimos

**Sistema Operacional**: 
- Linux (Ubuntu 20.04+ recomendado)
- macOS 10.15+
- Windows 10+

**Hardware**:
- CPU: 2 cores, 2.0 GHz
- RAM: 4 GB
- Armazenamento: 10 GB livres
- Rede: Conexão estável com internet

**Software**:
- Python 3.11+
- pip (gerenciador de pacotes Python)
- Git (para controle de versão)

#### Requisitos Recomendados

**Hardware**:
- CPU: 4 cores, 2.5 GHz+
- RAM: 8 GB+
- Armazenamento: SSD com 50 GB livres
- Rede: Banda larga estável

**Software**:
- Nginx ou Apache (para produção)
- Supervisor (para gerenciamento de processos)
- Fail2ban (para segurança adicional)

### Instalação em Desenvolvimento

#### 1. Preparação do Ambiente

```bash
# Clone do repositório
git clone https://github.com/roma-confeccoes/erp-roma.git
cd erp-roma

# Criação do ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Atualização do pip
pip install --upgrade pip
```

#### 2. Instalação de Dependências

```bash
# Instalação das dependências
pip install -r requirements.txt

# Verificação da instalação
python -c "import flask; print(flask.__version__)"
```

#### 3. Configuração do Ambiente

```bash
# Cópia do arquivo de configuração
cp .env.example .env

# Edição das variáveis de ambiente
nano .env
```

Configurações essenciais no arquivo `.env`:

```bash
# Configurações básicas
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua_chave_secreta_muito_segura_aqui

# Banco de dados
DATABASE_URL=sqlite:///instance/roma_erp.db

# Integração Bling (opcional para desenvolvimento)
BLING_API_KEY=sua_api_key_do_bling

# E-mail (opcional para desenvolvimento)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu_email@gmail.com
MAIL_PASSWORD=sua_senha_de_app
```

#### 4. Inicialização do Banco de Dados

```bash
# Criação do banco e dados iniciais
python init_db.py

# Verificação da criação
ls -la instance/
```

#### 5. Execução da Aplicação

```bash
# Execução em modo desenvolvimento
python app.py

# A aplicação estará disponível em http://localhost:5000
```

### Instalação em Produção

#### 1. Preparação do Servidor

```bash
# Atualização do sistema (Ubuntu)
sudo apt update && sudo apt upgrade -y

# Instalação de dependências do sistema
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git

# Criação do usuário da aplicação
sudo useradd -m -s /bin/bash roma-erp
sudo su - roma-erp
```

#### 2. Deploy da Aplicação

```bash
# Clone e configuração
git clone https://github.com/roma-confeccoes/erp-roma.git
cd erp-roma

# Ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalação de dependências
pip install -r requirements.txt
pip install gunicorn  # Servidor WSGI para produção

# Configuração de produção
cp .env.example .env
nano .env
```

Configurações de produção no `.env`:

```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=chave_secreta_super_segura_para_producao

# Banco de dados
DATABASE_URL=sqlite:///instance/roma_erp.db

# Configurações de segurança
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
PERMANENT_SESSION_LIFETIME=1800

# Integração Bling
BLING_API_KEY=api_key_producao_bling

# Configurações de e-mail
MAIL_SERVER=smtp.empresa.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=sistema@romaconfeccoes.com.br
MAIL_PASSWORD=senha_segura
```

#### 3. Configuração do Gunicorn

Criação do arquivo de configuração `gunicorn.conf.py`:

```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

#### 4. Configuração do Supervisor

Criação do arquivo `/etc/supervisor/conf.d/roma-erp.conf`:

```ini
[program:roma-erp]
command=/home/roma-erp/erp-roma/venv/bin/gunicorn -c gunicorn.conf.py app:app
directory=/home/roma-erp/erp-roma
user=roma-erp
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/roma-erp.log
environment=PATH="/home/roma-erp/erp-roma/venv/bin"
```

```bash
# Ativação da configuração
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start roma-erp
```

#### 5. Configuração do Nginx

Criação do arquivo `/etc/nginx/sites-available/roma-erp`:

```nginx
server {
    listen 80;
    server_name erp.romaconfeccoes.com.br;
    
    # Redirecionamento para HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name erp.romaconfeccoes.com.br;
    
    # Certificados SSL
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # Configurações SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # Headers de segurança
    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    
    # Configuração da aplicação
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Arquivos estáticos
    location /static {
        alias /home/roma-erp/erp-roma/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Logs
    access_log /var/log/nginx/roma-erp.access.log;
    error_log /var/log/nginx/roma-erp.error.log;
}
```

```bash
# Ativação do site
sudo ln -s /etc/nginx/sites-available/roma-erp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Configuração de SSL/TLS

#### Usando Let's Encrypt (Recomendado)

```bash
# Instalação do Certbot
sudo apt install certbot python3-certbot-nginx

# Obtenção do certificado
sudo certbot --nginx -d erp.romaconfeccoes.com.br

# Renovação automática
sudo crontab -e
# Adicionar linha:
0 12 * * * /usr/bin/certbot renew --quiet
```

### Configuração de Backup Automático

#### Script de Backup

Criação do script `/home/roma-erp/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/home/roma-erp/backups"
DATE=$(date +%Y%m%d_%H%M%S)
APP_DIR="/home/roma-erp/erp-roma"

# Criação do diretório de backup
mkdir -p $BACKUP_DIR

# Backup do banco de dados
cp $APP_DIR/instance/roma_erp.db $BACKUP_DIR/roma_erp_$DATE.db

# Backup de configurações
tar -czf $BACKUP_DIR/config_$DATE.tar.gz $APP_DIR/.env $APP_DIR/instance/

# Limpeza de backups antigos (manter últimos 30 dias)
find $BACKUP_DIR -name "*.db" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

# Log do backup
echo "$(date): Backup realizado com sucesso" >> /var/log/roma-erp-backup.log
```

#### Agendamento do Backup

```bash
# Tornar o script executável
chmod +x /home/roma-erp/backup.sh

# Configuração do cron
crontab -e
# Adicionar linha para backup diário às 2:00 AM:
0 2 * * * /home/roma-erp/backup.sh
```

### Monitoramento e Logs

#### Configuração de Logs

Criação do arquivo `/etc/logrotate.d/roma-erp`:

```
/var/log/roma-erp.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 roma-erp roma-erp
    postrotate
        supervisorctl restart roma-erp
    endscript
}
```

#### Monitoramento de Saúde

Script de monitoramento `/home/roma-erp/health-check.sh`:

```bash
#!/bin/bash
URL="https://erp.romaconfeccoes.com.br/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $URL)

if [ $RESPONSE -ne 200 ]; then
    echo "$(date): ERP ROMA não está respondendo (HTTP $RESPONSE)" >> /var/log/roma-erp-health.log
    # Enviar alerta por e-mail ou SMS
    supervisorctl restart roma-erp
fi
```

### Troubleshooting de Instalação

#### Problemas Comuns

**Erro de Permissões**:
```bash
# Correção de permissões
sudo chown -R roma-erp:roma-erp /home/roma-erp/erp-roma
chmod +x /home/roma-erp/erp-roma/app.py
```

**Dependências Faltando**:
```bash
# Instalação de dependências do sistema
sudo apt install python3-dev libffi-dev libssl-dev
pip install --upgrade pip setuptools wheel
```

**Problemas de Banco de Dados**:
```bash
# Recriação do banco
rm instance/roma_erp.db
python init_db.py
```

**Problemas de Conectividade**:
```bash
# Verificação de portas
sudo netstat -tlnp | grep :8000
sudo ufw allow 80
sudo ufw allow 443
```

---

