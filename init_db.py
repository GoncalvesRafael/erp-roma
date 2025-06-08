#!/usr/bin/env python3
"""
Script para inicializar o banco de dados do ERP ROMA
"""

import os
import sys
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Usuario, Cliente, Produto, Material, Fornecedor

def init_database():
    """Inicializa o banco de dados com dados básicos."""
    
    app = create_app()
    
    with app.app_context():
        # Remove todas as tabelas existentes e recria
        db.drop_all()
        db.create_all()
        
        print("Banco de dados criado com sucesso!")
        
        # Cria usuário administrador padrão
        admin = Usuario(
            nome='Administrador',
            email='admin@romaconfeccoes.com',
            senha='admin123',
            tipo='administrador'
        )
        db.session.add(admin)
        
        # Cria alguns produtos básicos baseados na planilha
        produtos = [
            Produto('1001', 'ECOBAG - NATURE', 'Ecobag', 15.00, 22.00),
            Produto('1002', 'MOCHILA ATHENA', 'Athena', 50.00, 75.00),
            Produto('1003', 'MOCHILA BERNA', 'Berna', 70.00, 106.00),
            Produto('1004', 'MOCHILA CELLA', 'Cella', 40.00, 58.00),
            Produto('1005', 'MOCHILA ZURICH', 'Zurich', 60.00, 85.00),
            Produto('1006', 'NECESSAIRE SIENA', 'Siena', 25.00, 39.00),
            Produto('1007', 'PASTA EXECUTIVA MILANO', 'Milano', 35.00, 54.00),
            Produto('1008', 'POCHETE OLIMPIUS', 'Olimpius', 22.00, 35.00),
            Produto('1009', 'SHOULDERBAG FLORA', 'Flora', 25.00, 37.00),
            Produto('1010', 'MALA ALPHA2', 'Alpha2', 75.00, 110.00),
            Produto('1011', 'MALA DELTA', 'Delta', 70.00, 108.00)
        ]
        
        for produto in produtos:
            db.session.add(produto)
        
        # Cria alguns clientes básicos
        clientes = [
            Cliente('Dona Chica Slingueria', '12.345.678/0001-90', 'contato@donachica.com', '(21) 99999-9999'),
            Cliente('Telecine', '23.456.789/0001-01', 'compras@telecine.com', '(21) 88888-8888'),
            Cliente('Globosat', '34.567.890/0001-12', 'fornecedores@globosat.com', '(21) 77777-7777'),
            Cliente('Megapix', '45.678.901/0001-23', 'comercial@megapix.com', '(21) 66666-6666')
        ]
        
        for cliente in clientes:
            db.session.add(cliente)
        
        # Cria alguns materiais básicos
        materiais = [
            Material('TEC001', 'Tecido Córdoba Preto', 'tecido', 'M', 25.00),
            Material('TEC002', 'Tecido Nylon 600 Azul', 'tecido', 'M', 30.00),
            Material('TEC003', 'Tecido Duratran Verde', 'tecido', 'M', 28.00),
            Material('AVI001', 'Zíper 30cm Preto', 'aviamento', 'UN', 3.50),
            Material('AVI002', 'Fivela Plástica 25mm', 'aviamento', 'UN', 2.00),
            Material('AVI003', 'Alça Regulável 25mm', 'aviamento', 'M', 8.00)
        ]
        
        for material in materiais:
            material.estoque_atual = 100.0  # Estoque inicial
            material.estoque_minimo = 10.0
            db.session.add(material)
        
        # Cria alguns fornecedores básicos
        fornecedores = [
            Fornecedor('Tecidos São Paulo Ltda', '56.789.012/0001-34', 'vendas@tecidossp.com', '(11) 3333-3333'),
            Fornecedor('Aviamentos Rio', '67.890.123/0001-45', 'comercial@aviamentosrio.com', '(21) 4444-4444'),
            Fornecedor('Metais e Acessórios', '78.901.234/0001-56', 'pedidos@metais.com', '(11) 5555-5555')
        ]
        
        for fornecedor in fornecedores:
            db.session.add(fornecedor)
        
        # Salva todas as alterações
        db.session.commit()
        
        print("Dados iniciais inseridos com sucesso!")
        print(f"Usuário administrador criado: admin@romaconfeccoes.com / admin123")
        print(f"Total de produtos: {len(produtos)}")
        print(f"Total de clientes: {len(clientes)}")
        print(f"Total de materiais: {len(materiais)}")
        print(f"Total de fornecedores: {len(fornecedores)}")

if __name__ == '__main__':
    init_database()

