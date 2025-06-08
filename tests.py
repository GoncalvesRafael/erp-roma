#!/usr/bin/env python3
"""
Script de testes integrados para o ERP ROMA.
Este script realiza testes em todos os módulos do sistema para garantir seu funcionamento correto.
"""

import os
import sys
import unittest
import time
import random
import string
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/tests.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('tests')

# Adiciona o diretório atual ao path para importar a aplicação
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Importa a aplicação Flask
from app import create_app, db
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.models.material import Material
from app.models.fornecedor import Fornecedor
from app.models.producao import Producao, ItemProducao
from app.models.financeiro import Movimentacao, NotaFiscal
from app.utils.security import backup_manager, security_manager

class TestConfig:
    """Configuração para testes."""
    TESTING = True
    DEBUG = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-key'
    DATABASE_URL = 'sqlite:///:memory:'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BACKUP_DIR = 'test_backups'
    MAX_BACKUPS = 5
    BACKUP_INTERVAL = 24
    ICLOUD_SYNC = False

class ERPRomaTestCase(unittest.TestCase):
    """Classe base para testes do ERP ROMA."""
    
    def setUp(self):
        """Configuração inicial para cada teste."""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        # Cria as tabelas no banco de dados em memória
        db.create_all()
        
        # Cria usuário de teste
        self.create_test_user()
        
        # Login para testes
        self.login('admin@romaconfeccoes.com', 'admin123')
        
        logger.info("Configuração de teste inicializada")
    
    def tearDown(self):
        """Limpeza após cada teste."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        logger.info("Limpeza de teste concluída")
    
    def create_test_user(self):
        """Cria um usuário de teste."""
        user = Usuario(
            nome='Admin Teste',
            email='admin@romaconfeccoes.com',
            perfil='administrador',
            ativo=True
        )
        user.set_password('admin123')
        db.session.add(user)
        db.session.commit()
        logger.info("Usuário de teste criado")
    
    def login(self, email, password):
        """Faz login no sistema."""
        return self.client.post('/auth/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)
    
    def logout(self):
        """Faz logout do sistema."""
        return self.client.get('/auth/logout', follow_redirects=True)
    
    def random_string(self, length=10):
        """Gera uma string aleatória."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def create_test_data(self):
        """Cria dados de teste para todos os módulos."""
        # Cria clientes
        for i in range(5):
            cliente = Cliente(
                nome=f'Cliente Teste {i+1}',
                tipo='juridica',
                cnpj=f'12345678901{i:03}',
                email=f'cliente{i+1}@teste.com',
                telefone=f'1198765432{i}',
                endereco=f'Rua Teste, {i+1}',
                cidade='São Paulo',
                estado='SP',
                cep=f'0123456{i}',
                ativo=True
            )
            db.session.add(cliente)
        
        # Cria fornecedores
        for i in range(3):
            fornecedor = Fornecedor(
                nome=f'Fornecedor Teste {i+1}',
                tipo='juridica',
                cnpj=f'98765432101{i:03}',
                email=f'fornecedor{i+1}@teste.com',
                telefone=f'1187654321{i}',
                endereco=f'Av. Teste, {i+1}',
                cidade='São Paulo',
                estado='SP',
                cep=f'0654321{i}',
                ativo=True
            )
            db.session.add(fornecedor)
        
        # Cria materiais
        materiais = []
        for i in range(10):
            material = Material(
                nome=f'Material Teste {i+1}',
                descricao=f'Descrição do material {i+1}',
                unidade='un',
                preco_unitario=10.0 + i,
                estoque_atual=100,
                estoque_minimo=20,
                fornecedor_id=random.randint(1, 3),
                ativo=True
            )
            db.session.add(material)
            materiais.append(material)
        
        # Cria produtos
        produtos = []
        for i in range(5):
            produto = Produto(
                nome=f'Produto Teste {i+1}',
                descricao=f'Descrição do produto {i+1}',
                preco_venda=50.0 + (i * 10),
                estoque_atual=50,
                estoque_minimo=10,
                ncm='62092000',
                origem=0,
                ativo=True
            )
            db.session.add(produto)
            produtos.append(produto)
            
            # Adiciona materiais ao produto
            for j in range(3):
                material_id = random.randint(1, 10)
                quantidade = random.randint(1, 5)
                produto.adicionar_material(material_id, quantidade)
        
        # Cria produções
        for i in range(3):
            producao = Producao(
                data=datetime.now() - timedelta(days=i),
                cliente_id=random.randint(1, 5),
                observacao=f'Produção teste {i+1}',
                status='finalizada'
            )
            db.session.add(producao)
            
            # Adiciona itens à produção
            for j in range(2):
                produto_id = random.randint(1, 5)
                quantidade = random.randint(10, 50)
                producao.adicionar_item(produto_id, quantidade)
        
        # Cria movimentações financeiras
        for i in range(10):
            tipo = 'receita' if i % 2 == 0 else 'despesa'
            movimentacao = Movimentacao(
                data=datetime.now() - timedelta(days=i),
                tipo=tipo,
                categoria='Venda' if tipo == 'receita' else 'Compra',
                descricao=f'Movimentação teste {i+1}',
                valor=random.randint(100, 1000) + random.random(),
                forma_pagamento='pix',
                status='confirmado'
            )
            db.session.add(movimentacao)
        
        # Cria notas fiscais
        for i in range(2):
            nota = NotaFiscal(
                numero=f'NF-{i+1}',
                serie='1',
                data_emissao=datetime.now() - timedelta(days=i),
                cliente_id=random.randint(1, 5),
                valor_total=random.randint(500, 2000) + random.random(),
                status='emitida'
            )
            db.session.add(nota)
        
        db.session.commit()
        logger.info("Dados de teste criados com sucesso")


class TestUsuarios(ERPRomaTestCase):
    """Testes para o módulo de usuários."""
    
    def test_login_logout(self):
        """Testa login e logout."""
        # Logout primeiro
        self.logout()
        
        # Tenta login com credenciais inválidas
        response = self.login('invalid@example.com', 'wrongpassword')
        self.assertIn(b'E-mail ou senha inv', response.data)
        
        # Login com credenciais válidas
        response = self.login('admin@romaconfeccoes.com', 'admin123')
        self.assertIn(b'Login realizado com sucesso', response.data)
        
        # Logout
        response = self.logout()
        self.assertIn(b'Logout realizado com sucesso', response.data)
        
        logger.info("Teste de login/logout concluído com sucesso")
    
    def test_criar_usuario(self):
        """Testa criação de usuário."""
        # Cria um novo usuário
        response = self.client.post('/usuarios/novo', data={
            'nome': 'Usuário Teste',
            'email': 'usuario@teste.com',
            'perfil': 'gestor',
            'password': 'Teste@123',
            'password_confirm': 'Teste@123'
        }, follow_redirects=True)
        
        self.assertIn(b'Usu', response.data)  # "Usuário criado com sucesso"
        
        # Verifica se o usuário foi criado
        usuario = Usuario.query.filter_by(email='usuario@teste.com').first()
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nome, 'Usuário Teste')
        self.assertEqual(usuario.perfil, 'gestor')
        
        logger.info("Teste de criação de usuário concluído com sucesso")
    
    def test_editar_usuario(self):
        """Testa edição de usuário."""
        # Cria um usuário para editar
        usuario = Usuario(
            nome='Editar Teste',
            email='editar@teste.com',
            perfil='visualizador',
            ativo=True
        )
        usuario.set_password('Teste@123')
        db.session.add(usuario)
        db.session.commit()
        
        # Edita o usuário
        response = self.client.post(f'/usuarios/editar/{usuario.id}', data={
            'nome': 'Editado Teste',
            'email': 'editado@teste.com',
            'perfil': 'gestor'
        }, follow_redirects=True)
        
        self.assertIn(b'Usu', response.data)  # "Usuário atualizado com sucesso"
        
        # Verifica se o usuário foi atualizado
        usuario_atualizado = Usuario.query.get(usuario.id)
        self.assertEqual(usuario_atualizado.nome, 'Editado Teste')
        self.assertEqual(usuario_atualizado.email, 'editado@teste.com')
        self.assertEqual(usuario_atualizado.perfil, 'gestor')
        
        logger.info("Teste de edição de usuário concluído com sucesso")


class TestClientes(ERPRomaTestCase):
    """Testes para o módulo de clientes."""
    
    def test_criar_cliente(self):
        """Testa criação de cliente."""
        # Cria um novo cliente
        response = self.client.post('/clientes/novo', data={
            'nome': 'Cliente Teste',
            'tipo': 'juridica',
            'cnpj': '12345678901234',
            'email': 'cliente@teste.com',
            'telefone': '11987654321',
            'endereco': 'Rua Teste, 123',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '01234567'
        }, follow_redirects=True)
        
        self.assertIn(b'Cliente criado com sucesso', response.data)
        
        # Verifica se o cliente foi criado
        cliente = Cliente.query.filter_by(email='cliente@teste.com').first()
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente.nome, 'Cliente Teste')
        
        logger.info("Teste de criação de cliente concluído com sucesso")
    
    def test_editar_cliente(self):
        """Testa edição de cliente."""
        # Cria um cliente para editar
        cliente = Cliente(
            nome='Editar Cliente',
            tipo='juridica',
            cnpj='98765432109876',
            email='editar@cliente.com',
            telefone='11987654321',
            endereco='Rua Editar, 123',
            cidade='São Paulo',
            estado='SP',
            cep='01234567',
            ativo=True
        )
        db.session.add(cliente)
        db.session.commit()
        
        # Edita o cliente
        response = self.client.post(f'/clientes/editar/{cliente.id}', data={
            'nome': 'Cliente Editado',
            'tipo': 'juridica',
            'cnpj': '98765432109876',
            'email': 'editado@cliente.com',
            'telefone': '11987654321',
            'endereco': 'Rua Editada, 456',
            'cidade': 'Rio de Janeiro',
            'estado': 'RJ',
            'cep': '01234567'
        }, follow_redirects=True)
        
        self.assertIn(b'Cliente atualizado com sucesso', response.data)
        
        # Verifica se o cliente foi atualizado
        cliente_atualizado = Cliente.query.get(cliente.id)
        self.assertEqual(cliente_atualizado.nome, 'Cliente Editado')
        self.assertEqual(cliente_atualizado.email, 'editado@cliente.com')
        self.assertEqual(cliente_atualizado.cidade, 'Rio de Janeiro')
        
        logger.info("Teste de edição de cliente concluído com sucesso")


class TestProdutos(ERPRomaTestCase):
    """Testes para o módulo de produtos."""
    
    def test_criar_produto(self):
        """Testa criação de produto."""
        # Cria um novo produto
        response = self.client.post('/produtos/novo', data={
            'nome': 'Produto Teste',
            'descricao': 'Descrição do produto teste',
            'preco_venda': '99.90',
            'estoque_atual': '50',
            'estoque_minimo': '10',
            'ncm': '62092000',
            'origem': '0'
        }, follow_redirects=True)
        
        self.assertIn(b'Produto criado com sucesso', response.data)
        
        # Verifica se o produto foi criado
        produto = Produto.query.filter_by(nome='Produto Teste').first()
        self.assertIsNotNone(produto)
        self.assertEqual(produto.preco_venda, 99.90)
        
        logger.info("Teste de criação de produto concluído com sucesso")
    
    def test_adicionar_material(self):
        """Testa adição de material ao produto."""
        # Cria um produto
        produto = Produto(
            nome='Produto com Material',
            descricao='Produto para teste de materiais',
            preco_venda=149.90,
            estoque_atual=30,
            estoque_minimo=5,
            ncm='62092000',
            origem=0,
            ativo=True
        )
        db.session.add(produto)
        
        # Cria um material
        material = Material(
            nome='Material para Produto',
            descricao='Material para teste',
            unidade='un',
            preco_unitario=10.0,
            estoque_atual=100,
            estoque_minimo=20,
            ativo=True
        )
        db.session.add(material)
        db.session.commit()
        
        # Adiciona o material ao produto
        produto.adicionar_material(material.id, 2)
        db.session.commit()
        
        # Verifica se o material foi adicionado
        self.assertEqual(len(produto.materiais), 1)
        self.assertEqual(produto.materiais[0].material_id, material.id)
        self.assertEqual(produto.materiais[0].quantidade, 2)
        
        logger.info("Teste de adição de material ao produto concluído com sucesso")


class TestProducao(ERPRomaTestCase):
    """Testes para o módulo de produção."""
    
    def test_criar_producao(self):
        """Testa criação de produção."""
        # Cria dados necessários
        self.create_test_data()
        
        # Cria uma nova produção
        response = self.client.post('/producao/nova', data={
            'data': datetime.now().strftime('%Y-%m-%d'),
            'cliente_id': '1',
            'observacao': 'Produção de teste'
        }, follow_redirects=True)
        
        self.assertIn(b'Produ', response.data)  # "Produção criada com sucesso"
        
        # Verifica se a produção foi criada
        producao = Producao.query.filter_by(observacao='Produção de teste').first()
        self.assertIsNotNone(producao)
        self.assertEqual(producao.cliente_id, 1)
        
        logger.info("Teste de criação de produção concluído com sucesso")
    
    def test_adicionar_item_producao(self):
        """Testa adição de item à produção."""
        # Cria dados necessários
        self.create_test_data()
        
        # Cria uma produção
        producao = Producao(
            data=datetime.now(),
            cliente_id=1,
            observacao='Produção para teste de itens',
            status='em_andamento'
        )
        db.session.add(producao)
        db.session.commit()
        
        # Adiciona um item à produção
        response = self.client.post(f'/producao/{producao.id}/adicionar-item', data={
            'produto_id': '1',
            'quantidade': '10',
            'valor_unitario': '50.00'
        }, follow_redirects=True)
        
        self.assertIn(b'Item adicionado com sucesso', response.data)
        
        # Verifica se o item foi adicionado
        producao = Producao.query.get(producao.id)
        self.assertEqual(len(producao.itens), 1)
        self.assertEqual(producao.itens[0].produto_id, 1)
        self.assertEqual(producao.itens[0].quantidade, 10)
        
        logger.info("Teste de adição de item à produção concluído com sucesso")


class TestFinanceiro(ERPRomaTestCase):
    """Testes para o módulo financeiro."""
    
    def test_criar_movimentacao(self):
        """Testa criação de movimentação financeira."""
        # Cria uma nova movimentação
        response = self.client.post('/financeiro/movimentacao/nova', data={
            'data': datetime.now().strftime('%Y-%m-%d'),
            'tipo': 'receita',
            'categoria': 'Venda',
            'descricao': 'Movimentação de teste',
            'valor': '500.00',
            'forma_pagamento': 'pix',
            'status': 'confirmado'
        }, follow_redirects=True)
        
        self.assertIn(b'Movimenta', response.data)  # "Movimentação criada com sucesso"
        
        # Verifica se a movimentação foi criada
        movimentacao = Movimentacao.query.filter_by(descricao='Movimentação de teste').first()
        self.assertIsNotNone(movimentacao)
        self.assertEqual(movimentacao.tipo, 'receita')
        self.assertEqual(movimentacao.valor, 500.00)
        
        logger.info("Teste de criação de movimentação concluído com sucesso")
    
    def test_criar_nota_fiscal(self):
        """Testa criação de nota fiscal."""
        # Cria dados necessários
        self.create_test_data()
        
        # Cria uma nova nota fiscal
        response = self.client.post('/financeiro/nota-fiscal/nova', data={
            'numero': 'NF-TEST',
            'serie': '1',
            'data_emissao': datetime.now().strftime('%Y-%m-%d'),
            'cliente_id': '1',
            'valor_total': '1000.00',
            'status': 'emitida'
        }, follow_redirects=True)
        
        self.assertIn(b'Nota fiscal criada com sucesso', response.data)
        
        # Verifica se a nota fiscal foi criada
        nota = NotaFiscal.query.filter_by(numero='NF-TEST').first()
        self.assertIsNotNone(nota)
        self.assertEqual(nota.cliente_id, 1)
        self.assertEqual(nota.valor_total, 1000.00)
        
        logger.info("Teste de criação de nota fiscal concluído com sucesso")


class TestBackupSeguranca(ERPRomaTestCase):
    """Testes para o módulo de backup e segurança."""
    
    def test_criar_backup(self):
        """Testa criação de backup."""
        # Cria dados de teste
        self.create_test_data()
        
        # Cria um backup
        backup_path = backup_manager.create_backup('test')
        
        # Verifica se o backup foi criado
        self.assertIsNotNone(backup_path)
        self.assertTrue(os.path.exists(backup_path))
        
        # Limpa o arquivo de backup
        if os.path.exists(backup_path):
            os.remove(backup_path)
        
        logger.info("Teste de criação de backup concluído com sucesso")
    
    def test_validacao_senha(self):
        """Testa validação de força de senha."""
        # Senha fraca
        resultado, erros = security_manager.validate_password_strength('123456')
        self.assertFalse(resultado)
        self.assertTrue(len(erros) > 0)
        
        # Senha forte
        resultado, erros = security_manager.validate_password_strength('Teste@123456')
        self.assertTrue(resultado)
        self.assertEqual(len(erros), 0)
        
        logger.info("Teste de validação de senha concluído com sucesso")


class TestIntegracao(ERPRomaTestCase):
    """Testes de integração entre módulos."""
    
    def test_fluxo_completo(self):
        """Testa um fluxo completo do sistema."""
        # Cria cliente
        cliente = Cliente(
            nome='Cliente Integração',
            tipo='juridica',
            cnpj='12345678901234',
            email='integracao@cliente.com',
            telefone='11987654321',
            endereco='Rua Integração, 123',
            cidade='São Paulo',
            estado='SP',
            cep='01234567',
            ativo=True
        )
        db.session.add(cliente)
        
        # Cria fornecedor
        fornecedor = Fornecedor(
            nome='Fornecedor Integração',
            tipo='juridica',
            cnpj='98765432109876',
            email='integracao@fornecedor.com',
            telefone='11987654321',
            endereco='Av. Integração, 456',
            cidade='São Paulo',
            estado='SP',
            cep='01234567',
            ativo=True
        )
        db.session.add(fornecedor)
        
        # Cria material
        material = Material(
            nome='Material Integração',
            descricao='Material para teste de integração',
            unidade='un',
            preco_unitario=15.0,
            estoque_atual=100,
            estoque_minimo=20,
            fornecedor_id=1,
            ativo=True
        )
        db.session.add(material)
        
        # Cria produto
        produto = Produto(
            nome='Produto Integração',
            descricao='Produto para teste de integração',
            preco_venda=99.90,
            estoque_atual=0,
            estoque_minimo=10,
            ncm='62092000',
            origem=0,
            ativo=True
        )
        db.session.add(produto)
        db.session.commit()
        
        # Adiciona material ao produto
        produto.adicionar_material(material.id, 2)
        db.session.commit()
        
        # Cria produção
        producao = Producao(
            data=datetime.now(),
            cliente_id=cliente.id,
            observacao='Produção de integração',
            status='em_andamento'
        )
        db.session.add(producao)
        db.session.commit()
        
        # Adiciona item à produção
        producao.adicionar_item(produto.id, 10)
        db.session.commit()
        
        # Finaliza produção
        estoque_material_antes = material.estoque_atual
        estoque_produto_antes = produto.estoque_atual
        
        producao.finalizar()
        db.session.commit()
        
        # Verifica se o estoque foi atualizado
        material_atualizado = Material.query.get(material.id)
        produto_atualizado = Produto.query.get(produto.id)
        
        # Material deve ter sido consumido
        self.assertEqual(material_atualizado.estoque_atual, estoque_material_antes - (2 * 10))
        
        # Produto deve ter sido produzido
        self.assertEqual(produto_atualizado.estoque_atual, estoque_produto_antes + 10)
        
        # Cria movimentação financeira
        movimentacao = Movimentacao(
            data=datetime.now(),
            tipo='receita',
            categoria='Venda',
            descricao='Recebimento da produção',
            valor=producao.valor_total,
            forma_pagamento='pix',
            status='confirmado'
        )
        db.session.add(movimentacao)
        
        # Cria nota fiscal
        nota = NotaFiscal(
            numero='NF-INT',
            serie='1',
            data_emissao=datetime.now(),
            cliente_id=cliente.id,
            valor_total=producao.valor_total,
            status='emitida'
        )
        db.session.add(nota)
        db.session.commit()
        
        # Verifica se tudo foi criado corretamente
        self.assertEqual(producao.status, 'finalizada')
        self.assertEqual(nota.cliente_id, cliente.id)
        self.assertEqual(movimentacao.valor, producao.valor_total)
        
        logger.info("Teste de fluxo completo concluído com sucesso")


class TestPerformance(ERPRomaTestCase):
    """Testes de performance do sistema."""
    
    def test_carga(self):
        """Testa o sistema com carga de dados."""
        # Cria muitos dados para testar performance
        start_time = time.time()
        
        # Cria 50 clientes
        for i in range(50):
            cliente = Cliente(
                nome=f'Cliente Performance {i+1}',
                tipo='juridica',
                cnpj=f'1234567890{i:04}',
                email=f'performance{i+1}@cliente.com',
                telefone=f'1198765432{i % 10}',
                endereco=f'Rua Performance, {i+1}',
                cidade='São Paulo',
                estado='SP',
                cep=f'0123456{i % 10}',
                ativo=True
            )
            db.session.add(cliente)
        
        # Cria 20 produtos
        for i in range(20):
            produto = Produto(
                nome=f'Produto Performance {i+1}',
                descricao=f'Produto para teste de performance {i+1}',
                preco_venda=50.0 + i,
                estoque_atual=100,
                estoque_minimo=10,
                ncm='62092000',
                origem=0,
                ativo=True
            )
            db.session.add(produto)
        
        # Cria 100 movimentações
        for i in range(100):
            tipo = 'receita' if i % 2 == 0 else 'despesa'
            movimentacao = Movimentacao(
                data=datetime.now() - timedelta(days=i % 30),
                tipo=tipo,
                categoria='Venda' if tipo == 'receita' else 'Compra',
                descricao=f'Movimentação performance {i+1}',
                valor=random.randint(100, 1000) + random.random(),
                forma_pagamento='pix',
                status='confirmado'
            )
            db.session.add(movimentacao)
        
        db.session.commit()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verifica se a execução foi rápida o suficiente
        self.assertLess(execution_time, 5.0, f"Teste de carga demorou muito: {execution_time:.2f} segundos")
        
        # Verifica se os dados foram criados
        self.assertEqual(Cliente.query.count(), 50)
        self.assertEqual(Produto.query.count(), 20)
        self.assertEqual(Movimentacao.query.count(), 100)
        
        logger.info(f"Teste de carga concluído em {execution_time:.2f} segundos")


def run_tests():
    """Executa todos os testes."""
    # Cria diretório de logs se não existir
    Path('logs').mkdir(parents=True, exist_ok=True)
    
    # Executa os testes
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestUsuarios))
    test_suite.addTest(unittest.makeSuite(TestClientes))
    test_suite.addTest(unittest.makeSuite(TestProdutos))
    test_suite.addTest(unittest.makeSuite(TestProducao))
    test_suite.addTest(unittest.makeSuite(TestFinanceiro))
    test_suite.addTest(unittest.makeSuite(TestBackupSeguranca))
    test_suite.addTest(unittest.makeSuite(TestIntegracao))
    test_suite.addTest(unittest.makeSuite(TestPerformance))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Retorna código de saída
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())

