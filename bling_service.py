"""
Serviço de integração com a API do Bling
"""

import requests
import json
from datetime import datetime
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.models.financeiro import NotaFiscal
from flask import current_app
import os

class BlingService:
    """Serviço para integração com a API do Bling."""
    
    def __init__(self):
        self.api_key = os.getenv('BLING_API_KEY', '')
        self.base_url = 'https://bling.com.br/Api/v2'
        
    def _make_request(self, endpoint, method='GET', data=None):
        """Faz uma requisição para a API do Bling."""
        url = f"{self.base_url}/{endpoint}"
        
        params = {'apikey': self.api_key}
        if method == 'GET':
            params.update(data or {})
            response = requests.get(url, params=params)
        else:
            response = requests.post(url, params=params, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro na API do Bling: {response.status_code} - {response.text}")
    
    def criar_nota_fiscal(self, nota_fiscal):
        """Cria uma nota fiscal no Bling."""
        if not self.api_key:
            raise Exception("API Key do Bling não configurada")
        
        # Monta o XML da nota fiscal
        xml_nota = self._montar_xml_nota_fiscal(nota_fiscal)
        
        data = {
            'xml': xml_nota
        }
        
        try:
            response = self._make_request('notafiscal/json/', method='POST', data=data)
            
            if 'retorno' in response and 'notasfiscais' in response['retorno']:
                nota_bling = response['retorno']['notasfiscais'][0]['notafiscal']
                
                # Atualiza a nota fiscal local com os dados do Bling
                nota_fiscal.numero_bling = nota_bling.get('numero', '')
                nota_fiscal.chave_acesso = nota_bling.get('chaveAcesso', '')
                nota_fiscal.status = 'emitida'
                nota_fiscal.data_emissao_bling = datetime.now()
                
                return True
            else:
                raise Exception("Resposta inválida da API do Bling")
                
        except Exception as e:
            nota_fiscal.status = 'erro'
            nota_fiscal.observacoes_erro = str(e)
            raise e
    
    def _montar_xml_nota_fiscal(self, nota_fiscal):
        """Monta o XML da nota fiscal para envio ao Bling."""
        cliente = nota_fiscal.cliente
        
        # Formatação de campos conforme padrão do Bling
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <pedido>
            <data>{nota_fiscal.data_emissao.strftime('%d/%m/%Y')}</data>
            <numero>{nota_fiscal.numero}</numero>
            <serie>{nota_fiscal.serie}</serie>
            <cliente>
                <nome>{cliente.nome}</nome>
                <tipoPessoa>{self._determinar_tipo_pessoa(cliente.cnpj)}</tipoPessoa>
                <cpf_cnpj>{cliente.cnpj.replace('.', '').replace('/', '').replace('-', '')}</cpf_cnpj>
                <ie>{cliente.inscricao_estadual or ''}</ie>
                <endereco>{cliente.logradouro}</endereco>
                <numero>{cliente.numero}</numero>
                <complemento>{cliente.complemento or ''}</complemento>
                <bairro>{cliente.bairro}</bairro>
                <cep>{cliente.cep.replace('-', '')}</cep>
                <cidade>{cliente.cidade}</cidade>
                <uf>{cliente.estado}</uf>
                <email>{cliente.email}</email>
                <fone>{cliente.telefone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')}</fone>
            </cliente>
            <itens>
                {self._montar_itens_nota(nota_fiscal)}
            </itens>
            <parcelas>
                <parcela>
                    <data>{nota_fiscal.data_vencimento.strftime('%d/%m/%Y') if nota_fiscal.data_vencimento else nota_fiscal.data_emissao.strftime('%d/%m/%Y')}</data>
                    <vlr>{nota_fiscal.valor_total}</vlr>
                    <obs>Pagamento à vista</obs>
                </parcela>
            </parcelas>
            <transporte>
                <transportadora></transportadora>
                <tipo_frete>0</tipo_frete>
                <qtde_volumes>1</qtde_volumes>
            </transporte>
            <vlr_frete>0</vlr_frete>
            <vlr_seguro>0</vlr_seguro>
            <vlr_despesas>0</vlr_despesas>
            <vlr_desconto>0</vlr_desconto>
            <obs>{nota_fiscal.observacoes or ''}</obs>
            <obs_internas>Emitido pelo ERP ROMA</obs_internas>
        </pedido>"""
        
        return xml
    
    def _montar_itens_nota(self, nota_fiscal):
        """Monta os itens da nota fiscal."""
        # Na implementação real, buscaríamos os itens relacionados à nota fiscal
        # Por enquanto, vamos criar um item genérico
        
        # Verificamos se a nota tem itens relacionados
        if hasattr(nota_fiscal, 'itens') and nota_fiscal.itens:
            itens_xml = ""
            for item in nota_fiscal.itens:
                produto = item.produto
                itens_xml += f"""
                <item>
                    <codigo>{produto.codigo}</codigo>
                    <descricao>{produto.nome}</descricao>
                    <un>{produto.unidade_medida}</un>
                    <qtde>{item.quantidade}</qtde>
                    <vlr_unit>{item.valor_unitario}</vlr_unit>
                    <tipo>P</tipo>
                    <peso_bruto>0.000</peso_bruto>
                    <peso_liq>0.000</peso_liq>
                    <class_fiscal>{produto.ncm if hasattr(produto, 'ncm') and produto.ncm else '62092000'}</class_fiscal>
                    <origem>0</origem>
                </item>"""
            return itens_xml
        else:
            # Item genérico se não houver itens específicos
            return f"""
            <item>
                <codigo>SERVICO</codigo>
                <descricao>Serviços de confecção</descricao>
                <un>UN</un>
                <qtde>1</qtde>
                <vlr_unit>{nota_fiscal.valor_total}</vlr_unit>
                <tipo>P</tipo>
                <peso_bruto>0.000</peso_bruto>
                <peso_liq>0.000</peso_liq>
                <class_fiscal>62092000</class_fiscal>
                <origem>0</origem>
            </item>"""
    
    def _determinar_tipo_pessoa(self, cnpj):
        """Determina o tipo de pessoa com base no CNPJ/CPF."""
        # Remove caracteres não numéricos
        documento = ''.join(filter(str.isdigit, cnpj))
        
        if len(documento) == 11:
            return 'F'  # Pessoa Física
        else:
            return 'J'  # Pessoa Jurídica
    
    def consultar_nota_fiscal(self, numero, serie):
        """Consulta uma nota fiscal no Bling."""
        if not self.api_key:
            raise Exception("API Key do Bling não configurada")
        
        data = {
            'numero': numero,
            'serie': serie
        }
        
        response = self._make_request('notafiscal/json/', data=data)
        
        if 'retorno' in response and 'notasfiscais' in response['retorno']:
            return response['retorno']['notasfiscais'][0]['notafiscal']
        else:
            return None
    
    def listar_notas_fiscais(self, data_inicio=None, data_fim=None):
        """Lista notas fiscais do Bling."""
        if not self.api_key:
            raise Exception("API Key do Bling não configurada")
        
        data = {}
        if data_inicio:
            data['dataEmissaoInicial'] = data_inicio.strftime('%d/%m/%Y')
        if data_fim:
            data['dataEmissaoFinal'] = data_fim.strftime('%d/%m/%Y')
        
        response = self._make_request('notasfiscais/json/', data=data)
        
        if 'retorno' in response and 'notasfiscais' in response['retorno']:
            return response['retorno']['notasfiscais']
        else:
            return []
    
    def sincronizar_clientes(self):
        """Sincroniza clientes com o Bling."""
        if not self.api_key:
            raise Exception("API Key do Bling não configurada")
        
        try:
            response = self._make_request('contatos/json/')
            
            if 'retorno' in response and 'contatos' in response['retorno']:
                contatos_bling = response['retorno']['contatos']
                
                for contato_data in contatos_bling:
                    contato = contato_data['contato']
                    
                    # Verifica se o cliente já existe
                    cliente_existente = Cliente.query.filter_by(
                        cnpj=contato.get('cnpj', '')
                    ).first()
                    
                    if not cliente_existente and contato.get('cnpj'):
                        # Cria novo cliente
                        novo_cliente = Cliente(
                            nome=contato.get('nome', ''),
                            cnpj=contato.get('cnpj', ''),
                            inscricao_estadual=contato.get('ie', ''),
                            email=contato.get('email', ''),
                            telefone=contato.get('telefone', ''),
                            logradouro=contato.get('endereco', ''),
                            numero=contato.get('numero', ''),
                            bairro=contato.get('bairro', ''),
                            cidade=contato.get('cidade', ''),
                            estado=contato.get('uf', ''),
                            cep=contato.get('cep', ''),
                            ativo=True
                        )
                        
                        from app import db
                        db.session.add(novo_cliente)
                
                from app import db
                db.session.commit()
                return len(contatos_bling)
                
        except Exception as e:
            raise Exception(f"Erro ao sincronizar clientes: {str(e)}")
    
    def testar_conexao(self):
        """Testa a conexão com a API do Bling."""
        if not self.api_key:
            return False, "API Key não configurada"
        
        try:
            response = self._make_request('situacao/json/')
            
            if 'retorno' in response:
                return True, "Conexão estabelecida com sucesso"
            else:
                return False, "Resposta inválida da API"
                
        except Exception as e:
            return False, f"Erro na conexão: {str(e)}"

