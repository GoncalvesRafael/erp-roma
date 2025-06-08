# ERP ROMA - Sistema de Gestão Empresarial

**Sistema completo de gestão empresarial desenvolvido especificamente para a Roma Confecções**

![Logo Roma](app/static/img/logo_roma.png)

---

## 📋 Sobre o Projeto

O ERP ROMA é um sistema de gestão empresarial completo e moderno, desenvolvido especificamente para atender às necessidades da Roma Confecções. O sistema integra todos os processos operacionais da empresa, desde o cadastro de clientes até a emissão de notas fiscais, proporcionando maior eficiência e controle sobre as operações.

### 🎯 Objetivos

- **Centralizar** todas as informações da empresa em um único sistema
- **Automatizar** processos manuais e repetitivos
- **Integrar** com sistemas fiscais (Bling) para emissão de notas fiscais
- **Fornecer** relatórios e dashboards para tomada de decisão
- **Garantir** segurança e backup dos dados empresariais

---

## 🚀 Funcionalidades Principais

### 👥 Gestão de Usuários
- Sistema multiusuário com níveis de permissão
- Perfis: Administrador, Gestor, Visualizador
- Controle de acesso baseado em funções (RBAC)
- Logs de auditoria de ações dos usuários

### 🏢 Gestão de Clientes
- Cadastro completo de pessoas físicas e jurídicas
- Validação automática de CNPJ/CPF
- Controle de endereços e informações de contato
- Histórico de produções por cliente

### 📦 Gestão de Produtos
- Cadastro de produtos com informações fiscais
- Controle de estoque com alertas de estoque mínimo
- Composição de produtos com materiais
- Cálculo automático de custos de produção

### 🏭 Gestão de Produção
- Registro de produções por cliente
- Controle de itens produzidos e quantidades
- Finalização automática com atualização de estoque
- Relatórios de produtividade

### 📊 Gestão Financeira
- Fluxo de caixa com receitas e despesas
- Categorização de movimentações financeiras
- Emissão de notas fiscais integrada ao Bling
- Relatórios financeiros detalhados

### 📈 Dashboard e Relatórios
- Dashboard principal com indicadores em tempo real
- Gráficos interativos de produção e finanças
- Relatórios exportáveis em PDF
- Filtros por período e categoria

### 🔒 Segurança e Backup
- Backup automático diário do banco de dados
- Sincronização com iCloud (para usuários Mac)
- Logs de auditoria e monitoramento
- Proteção contra ataques comuns (CSRF, XSS, SQL Injection)

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11** - Linguagem de programação principal
- **Flask 3.0** - Framework web minimalista e flexível
- **SQLAlchemy 2.0** - ORM para abstração de banco de dados
- **SQLite** - Banco de dados relacional embarcado
- **Flask-Login** - Gerenciamento de autenticação
- **Flask-WTF** - Formulários e proteção CSRF

### Frontend
- **HTML5** - Marcação semântica moderna
- **TailwindCSS** - Framework CSS utility-first
- **JavaScript ES6+** - Interatividade client-side
- **Chart.js** - Gráficos interativos

### Integrações
- **API Bling** - Emissão de notas fiscais
- **ReportLab** - Geração de relatórios PDF
- **Requests** - Comunicação HTTP com APIs

---

## 📁 Estrutura do Projeto

```
roma_sistema/
├── app/                          # Aplicação principal
│   ├── models/                   # Modelos de dados
│   ├── routes/                   # Controladores (Blueprints)
│   ├── services/                 # Serviços de negócio
│   ├── utils/                    # Utilitários
│   ├── static/                   # Arquivos estáticos
│   └── templates/                # Templates HTML
├── docs/                         # Documentação
├── instance/                     # Dados da instância
├── app.py                        # Ponto de entrada
├── config.py                     # Configurações
├── requirements.txt              # Dependências
└── README.md                     # Este arquivo
```

---

## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/roma-confeccoes/erp-roma.git
cd erp-roma

# 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# 5. Inicialize o banco de dados
python init_db.py

# 6. Execute a aplicação
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

### Configuração da Integração Bling

1. Acesse o painel administrativo do sistema
2. Vá em "Configurações" > "Integração Bling"
3. Insira sua API Key do Bling
4. Configure os parâmetros fiscais da empresa
5. Teste a conexão

---

## 👤 Usuário Padrão

Após a inicialização do banco de dados, um usuário administrador é criado automaticamente:

- **E-mail:** admin@romaconfeccoes.com
- **Senha:** admin123

⚠️ **Importante:** Altere a senha padrão imediatamente após o primeiro acesso!

---

## 📖 Documentação

- **[Manual do Usuário](docs/manual_usuario.md)** - Guia completo para usuários finais
- **[Documentação Técnica](docs/documentacao_tecnica.md)** - Informações técnicas detalhadas
- **[Integração Bling](docs/integracao_bling.md)** - Documentação da integração fiscal

---

## 🧪 Testes

Execute os testes automatizados:

```bash
# Testes de integridade do sistema
python tests.py

# Otimização e limpeza
python optimize.py
```

---

## 🔄 Backup e Manutenção

### Backup Automático

O sistema realiza backup automático:
- **Diário:** Às 2:00 AM
- **Semanal:** Domingos às 3:00 AM
- **Mensal:** Primeiro domingo do mês

### Backup Manual

```bash
# Backup do banco de dados
cp instance/roma_erp.db backups/roma_erp_$(date +%Y%m%d).db

# Backup completo
python -c "from app.utils.security import backup_manager; backup_manager.criar_backup_completo()"
```

---

## 📊 Monitoramento

### Logs do Sistema

- **Aplicação:** `/var/log/roma-erp.log`
- **Backup:** `/var/log/roma-erp-backup.log`
- **Segurança:** `/var/log/roma-erp-security.log`

### Health Check

Verifique a saúde do sistema:

```bash
curl http://localhost:5000/health
```

---

## 🔒 Segurança

### Recursos de Segurança

- **Autenticação:** Sistema robusto com hash bcrypt
- **Autorização:** Controle de acesso baseado em perfis
- **Proteção CSRF:** Proteção automática contra ataques CSRF
- **Logs de Auditoria:** Registro de todas as ações importantes
- **Backup Criptografado:** Backups protegidos com criptografia

### Boas Práticas

- Use senhas fortes (mínimo 8 caracteres, maiúsculas, minúsculas, números e símbolos)
- Mantenha o sistema sempre atualizado
- Monitore os logs regularmente
- Realize backups periódicos
- Use HTTPS em produção

---

## 🚀 Deploy em Produção

### Usando Gunicorn + Nginx

```bash
# 1. Instale o Gunicorn
pip install gunicorn

# 2. Execute com Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# 3. Configure o Nginx como proxy reverso
# (Ver documentação técnica para configuração completa)
```

### Usando Docker (Opcional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

---

## 🤝 Suporte

### Contato

- **Empresa:** Roma Confecções
- **Sistema:** ERP ROMA v1.0
- **Desenvolvido por:** Manus AI

### Solução de Problemas

1. **Verifique os logs** em `/var/log/roma-erp.log`
2. **Consulte a documentação** técnica
3. **Execute os testes** com `python tests.py`
4. **Verifique as configurações** no arquivo `.env`

### Problemas Comuns

**Erro de conexão com banco:**
```bash
# Recrie o banco de dados
rm instance/roma_erp.db
python init_db.py
```

**Erro de permissões:**
```bash
# Ajuste as permissões
chmod +x app.py
chown -R usuario:grupo roma_sistema/
```

**Erro na integração Bling:**
- Verifique a API Key no painel administrativo
- Teste a conectividade com a internet
- Consulte os logs de integração

---

## 📝 Changelog

### v1.0.0 (Dezembro 2024)
- ✅ Sistema completo de gestão empresarial
- ✅ Integração com API do Bling
- ✅ Dashboard com gráficos interativos
- ✅ Sistema de backup automático
- ✅ Controle de acesso multiusuário
- ✅ Relatórios exportáveis em PDF

---

## 📄 Licença

Este sistema foi desenvolvido exclusivamente para a Roma Confecções. Todos os direitos reservados.

---

## 🎉 Agradecimentos

Agradecemos à equipe da Roma Confecções pela confiança e colaboração no desenvolvimento deste sistema. O ERP ROMA foi criado com dedicação para atender às necessidades específicas da empresa e contribuir para seu crescimento e sucesso.

---

**ERP ROMA - Gestão Empresarial Inteligente** 🚀

