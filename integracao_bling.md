# Integração com API do Bling - ERP ROMA

## Análise da Nota Fiscal Fornecida

Com base na nota fiscal fornecida (número 60), foram identificados os seguintes campos essenciais para a integração com o Bling:

### Dados do Cliente
- **Nome/Razão Social**: DONA CHICA INGUERIA LTDA
- **CNPJ**: 21.865.535/0001-03
- **Inscrição Estadual**: 11089160
- **Endereço Completo**: Rua Gomes Carneiro, 155 - AP 504, Ipanema, Rio de Janeiro/RJ, CEP 22.071-110
- **Telefone**: (21) 98123-0105

### Dados da Nota Fiscal
- **Número**: 60
- **Série**: 1
- **Data de Emissão**: 04/06/2025
- **Data de Saída**: 04/06/2025
- **Valor Total**: R$ 57.755,00

### Itens da Nota Fiscal
Foram identificados os seguintes produtos com seus códigos e NCM:

1. **Sling de argolas** (Código: 2022ARGOLAS)
   - NCM: 62092000
   - Quantidade: 10 unidades
   - Valor unitário: R$ 18,00
   - Valor total: R$ 180,00

2. **Capuz chica chila** (Código: CFOP5101)
   - NCM: 62092000
   - Quantidade: 15 unidades
   - Valor unitário: R$ 10,00
   - Valor total: R$ 150,00

3. **Chica Chila Evolutiva** (Código: 2022EVOLUTIVA)
   - NCM: 62092000
   - Quantidade: 434 unidades
   - Valor unitário: R$ 120,00
   - Valor total: R$ 52.080,00

4. **Pochete Acoplavel** (Código: 2022ACOPLAVEL)
   - NCM: 62092000
   - Quantidade: 10 unidades
   - Valor unitário: R$ 35,00
   - Valor total: R$ 350,00

5. **Chica Chila Pocket** (Código: 2022POCKET)
   - NCM: 62092000
   - Quantidade: 30 unidades
   - Valor unitário: R$ 111,00
   - Valor total: R$ 3.330,00

6. **Chica Chila Toddler** (Código: 2022TODDLER)
   - NCM: 62092000
   - Quantidade: 15 unidades
   - Valor unitário: R$ 111,00
   - Valor total: R$ 1.665,00

### Informações Fiscais
- **NCM Padrão**: 62092000 (Outros artefatos confeccionados de matérias têxteis)
- **CFOP**: 5.101 (Venda de produção do estabelecimento)
- **CSOSN**: 0101 (Tributada pelo Simples Nacional com permissão de crédito)
- **Origem**: 0 (Nacional)

### Mapeamento de Campos no ERP ROMA

#### Modelo Cliente
```python
nome = cliente.nome                    # DONA CHICA INGUERIA LTDA
cnpj = cliente.cnpj                    # 21.865.535/0001-03
inscricao_estadual = cliente.ie        # 11089160
logradouro = cliente.endereco          # Rua Gomes Carneiro, 155 - AP 504
bairro = cliente.bairro                # Ipanema
cidade = cliente.cidade                # Rio de Janeiro
estado = cliente.uf                    # RJ
cep = cliente.cep                      # 22.071-110
telefone = cliente.fone                # (21) 98123-0105
```

#### Modelo Produto
```python
codigo = produto.codigo                # 2022ARGOLAS, 2022EVOLUTIVA, etc.
nome = produto.descricao               # Sling de argolas, Chica Chila Evolutiva, etc.
ncm = produto.class_fiscal             # 62092000
origem = produto.origem                # 0 (Nacional)
unidade_medida = produto.un            # UN (Unidade)
```

#### Modelo Nota Fiscal
```python
numero = nota.numero                   # 60
serie = nota.serie                     # 1
data_emissao = nota.data               # 04/06/2025
valor_total = nota.vlr_total           # 57.755,00
```

### XML de Integração com Bling

O XML enviado para o Bling foi estruturado seguindo o padrão da API:

```xml
<pedido>
    <data>04/06/2025</data>
    <numero>60</numero>
    <serie>1</serie>
    <cliente>
        <nome>DONA CHICA INGUERIA LTDA</nome>
        <tipoPessoa>J</tipoPessoa>
        <cpf_cnpj>21865535000103</cpf_cnpj>
        <ie>11089160</ie>
        <endereco>Rua Gomes Carneiro, 155 - AP 504</endereco>
        <bairro>Ipanema</bairro>
        <cep>22071110</cep>
        <cidade>Rio de Janeiro</cidade>
        <uf>RJ</uf>
        <fone>21981230105</fone>
    </cliente>
    <itens>
        <item>
            <codigo>2022ARGOLAS</codigo>
            <descricao>Sling de argolas</descricao>
            <un>UN</un>
            <qtde>10</qtde>
            <vlr_unit>18.00</vlr_unit>
            <tipo>P</tipo>
            <class_fiscal>62092000</class_fiscal>
            <origem>0</origem>
        </item>
        <!-- Outros itens... -->
    </itens>
</pedido>
```

### Validações Implementadas

1. **Formatação de CNPJ**: Remove pontos, barras e hífens
2. **Formatação de CEP**: Remove hífens
3. **Formatação de Telefone**: Remove parênteses, espaços e hífens
4. **Tipo de Pessoa**: Determina automaticamente (F para CPF, J para CNPJ)
5. **NCM Padrão**: 62092000 para produtos sem NCM específico
6. **Origem Padrão**: 0 (Nacional)

### Configurações Necessárias

Para utilizar a integração, é necessário configurar:

1. **API Key do Bling**: Obtida no painel administrativo do Bling
2. **Situação Padrão**: Status inicial das notas (recomendado: 1 - Pendente)
3. **Série Padrão**: Série das notas fiscais (padrão: 1)

### Testes de Integração

O sistema inclui funcionalidades para:

1. **Testar Conexão**: Verifica se a API Key está válida
2. **Sincronizar Clientes**: Importa clientes do Bling para o ERP
3. **Emitir Notas**: Envia notas fiscais para o Bling
4. **Consultar Status**: Verifica o status das notas emitidas

### Tratamento de Erros

O sistema trata os seguintes cenários de erro:

1. **API Key inválida**: Retorna erro de autenticação
2. **Dados incompletos**: Valida campos obrigatórios
3. **Nota já emitida**: Impede reemissão
4. **Erro de comunicação**: Registra erro e permite nova tentativa

Esta integração garante que todas as notas fiscais emitidas pelo ERP ROMA sejam compatíveis com o padrão do Bling e contenham todas as informações necessárias para emissão fiscal correta.

