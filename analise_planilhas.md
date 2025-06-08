# Análise Detalhada das Planilhas - Roma Confecções

## 1. Planilha de Custos dos Produtos

**URL:** https://docs.google.com/spreadsheets/d/1QKILUGtUuBAAN7stiFO3-dQ6PtDKuV19ihPtXcEA64o/edit?usp=sharing

**Estrutura identificada:**
- Aba principal: "Tabela de Preços - 2025"
- Colunas:
  - A: Produto (nome do produto)
  - B: Código (código numérico do produto)
  - C: A partir (preço unitário)
  - D: Qtde mínima (quantidade mínima para o preço)

**Produtos identificados:**
- ECOBAG - NATURE (1001) - R$22,00 - Qtde mín: 200
- MOCHILA ATHENA (1002) - R$75,00 - Qtde mín: 100
- MOCHILA BERNA (1003) - R$106,00 - Qtde mín: 100
- MOCHILA CELLA (1004) - R$58,00 - Qtde mín: 100
- MOCHILA ZURICH (1005) - R$85,00 - Qtde mín: 100
- NECESSAIRE SIENA (1006) - R$39,00 - Qtde mín: 200
- PASTA EXECUTIVA MILANO (1007) - R$54,00 - Qtde mín: 200
- POCHETE OLIMPIUS (1008) - R$35,00 - Qtde mín: 200
- SHOULDERBAG FLORA (1009) - R$37,00 - Qtde mín: 100
- MALA ALPHA2 (1010) - R$110,00 - Qtde mín: 100
- MALA DELTA (1011) - R$108,00 - Qtde mín: 100

**Observações:**
- Múltiplas abas com diferentes projetos/clientes específicos
- Estrutura de custos detalhada por produto

## 2. Planilha de Fechamento Mensal/Produção Diária

**URL:** https://docs.google.com/spreadsheets/d/1Tmp28xoMKmYNC8hlVM5VmAsawQWohQXyhga94MiEkJo/edit?usp=sharing

**Estrutura identificada:**
- Aba principal: "FechamentoMensal"
- Colunas:
  - A: Data (formato DD/MM/AAAA)
  - B: Empresa (cliente)
  - C: Modelo (tipo de produto)
  - D: Produto (especificação do produto)
  - E: Quantidade (unidades produzidas)
  - F: Valor unitário (preço por unidade)
  - G: Valor total (quantidade × valor unitário)
  - H: mes_ano (período de referência)

**Dados de exemplo identificados:**
- Período: setembro de 2024
- Principais clientes: Dona Chica, Criaturas, Fechamento Extra
- Produtos: Evolutiva, Pocket, Lençol, Pochete G, etc.
- Valores unitários variando de R$12,00 a R$1.538,23
- Quantidades variando de 1 a 30 unidades

**Observações:**
- Dados de produção diária com detalhamento por cliente
- Fórmula IMPORTRANGE conectando com outra planilha
- Múltiplas abas: ProducaoDados, Página4, FechamentoMensal, Pagamento, Produtos

## 3. Planilha de Livro Caixa

**URL:** https://docs.google.com/spreadsheets/d/1NK0tjsybLuFFUCCcDQqmNt1bhs0ibZXrIn2ZJ3LGKug/edit?usp=sharing

**Estrutura identificada:**
- Aba principal: "LivroCaixa"
- Colunas:
  - A: DATA (formato DD mmm. AAAA)
  - B: DESCRIÇÃO (descrição da movimentação)
  - C: ENTRADA (valores de entrada)
  - D: SAÍDA (valores de saída)
  - E: TIPO (categoria da movimentação)

**Tipos de movimentação identificados:**
- CUSTO (gastos operacionais)
- INSUMO (compra de materiais)
- PROLABORE (retirada dos sócios)
- FUNCIONÁRIO (pagamento de funcionários)
- EXPEDIÇÃO (custos de envio)
- ENTRADA (receitas)

**Observações:**
- Controle financeiro detalhado
- Múltiplas abas: LivroCaixa, CustoDetalhado, PivotTable, Dashboard
- Totalizadores de entrada e saída
- Período analisado: agosto de 2022

## Requisitos Funcionais do Sistema

### 1. Importação de Dados
- Conectar com Google Sheets API para importar dados automaticamente
- Processar dados das três planilhas principais
- Validar integridade dos dados importados
- Atualizar dados periodicamente

### 2. Processamento de Dados
- Integrar dados de custos com dados de produção
- Calcular margens de lucro por produto
- Analisar performance por cliente
- Calcular indicadores financeiros

### 3. Análises e Relatórios
- Análise de custos por produto
- Análise de produção por período
- Análise de rentabilidade por cliente
- Análise de fluxo de caixa
- Comparativos mensais/anuais

### 4. Visualizações
- Dashboard principal com KPIs
- Gráficos de produção por período
- Gráficos de faturamento por cliente
- Gráficos de custos vs receitas
- Análise de tendências

### 5. Interface de Usuário
- Interface web responsiva
- Filtros por período, cliente, produto
- Exportação de relatórios
- Visualização de dados em tempo real

## Métricas e Indicadores Propostos

### Indicadores de Produção
- Quantidade total produzida por período
- Produção por produto
- Produção por cliente
- Média de produção diária

### Indicadores Financeiros
- Faturamento total por período
- Faturamento por cliente
- Faturamento por produto
- Margem de lucro por produto
- Ticket médio por cliente

### Indicadores de Custos
- Custo total por período
- Custo por categoria
- Custo por produto
- Relação custo/receita

### Indicadores de Performance
- Produtos mais vendidos
- Clientes mais rentáveis
- Sazonalidade de vendas
- Eficiência operacional

