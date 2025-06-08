# Manual do Usuário - ERP ROMA

**Sistema de Gestão Empresarial para Roma Confecções**

---

**Versão:** 1.0  
**Data:** Dezembro 2024  
**Autor:** Manus AI  
**Empresa:** Roma Confecções  

---

## Sumário

1. [Introdução](#introdução)
2. [Primeiros Passos](#primeiros-passos)
3. [Módulo de Usuários](#módulo-de-usuários)
4. [Módulo de Clientes](#módulo-de-clientes)
5. [Módulo de Produtos](#módulo-de-produtos)
6. [Módulo de Fornecedores](#módulo-de-fornecedores)
7. [Módulo de Estoque](#módulo-de-estoque)
8. [Módulo de Produção](#módulo-de-produção)
9. [Módulo Financeiro](#módulo-financeiro)
10. [Dashboard e Relatórios](#dashboard-e-relatórios)
11. [Administração](#administração)
12. [Integração com Bling](#integração-com-bling)
13. [Backup e Segurança](#backup-e-segurança)
14. [Solução de Problemas](#solução-de-problemas)
15. [Glossário](#glossário)

---

## Introdução

O ERP ROMA é um sistema de gestão empresarial desenvolvido especificamente para a Roma Confecções, uma empresa especializada na fabricação de mochilas e acessórios para o mercado B2B. Este sistema foi projetado para centralizar, automatizar e sincronizar todas as operações da fábrica, proporcionando maior eficiência, controle e visibilidade dos processos empresariais.

### Características Principais

O ERP ROMA oferece uma solução completa e integrada que abrange todos os aspectos operacionais da Roma Confecções. O sistema foi desenvolvido com foco na simplicidade de uso, sem comprometer a robustez e funcionalidade necessárias para uma gestão empresarial eficaz.

Entre as principais características do sistema, destacam-se a gestão completa de usuários com diferentes níveis de acesso, permitindo que administradores, gestores e visualizadores tenham permissões adequadas às suas funções. O cadastro de clientes é abrangente, incluindo informações completas de contato, endereço e dados fiscais, essenciais para a emissão de documentos fiscais e controle comercial.

O controle de produtos é detalhado, incluindo composição de materiais, preços, estoques e informações fiscais como NCM e origem. Esta funcionalidade é fundamental para o cálculo preciso de custos e para a emissão de notas fiscais em conformidade com a legislação brasileira.

A gestão de fornecedores permite o cadastro completo de parceiros comerciais, facilitando o controle de compras e a gestão de relacionamentos comerciais. O módulo de estoque oferece controle em tempo real de materiais e produtos acabados, com alertas de estoque mínimo e histórico completo de movimentações.

O módulo de produção é o coração do sistema, permitindo o registro detalhado de todas as produções realizadas, com controle de itens produzidos, quantidades, valores e consumo automático de materiais. Este módulo está totalmente integrado com o controle de estoque, garantindo a precisão das informações.

O módulo financeiro oferece controle completo do fluxo de caixa, com categorização de receitas e despesas, múltiplas formas de pagamento e relatórios detalhados. A integração com o sistema de notas fiscais garante que todas as movimentações financeiras estejam devidamente documentadas.

### Benefícios do Sistema

A implementação do ERP ROMA traz diversos benefícios para a Roma Confecções. A centralização de informações elimina a necessidade de múltiplas planilhas e sistemas isolados, reduzindo significativamente o risco de erros e inconsistências. A automação de processos, como o consumo de materiais na produção e a atualização de estoques, economiza tempo e garante maior precisão nas operações.

O controle em tempo real permite tomadas de decisão mais rápidas e assertivas, baseadas em informações atualizadas e confiáveis. Os relatórios e dashboards oferecem visibilidade completa do negócio, facilitando o acompanhamento de indicadores de performance e a identificação de oportunidades de melhoria.

A integração com o Bling para emissão fiscal automatiza um processo crítico e complexo, garantindo conformidade com a legislação e reduzindo significativamente o tempo necessário para a emissão de notas fiscais. O sistema de backup automático e as funcionalidades de segurança protegem as informações empresariais contra perdas e acessos não autorizados.

### Arquitetura do Sistema

O ERP ROMA foi desenvolvido utilizando tecnologias modernas e confiáveis. A aplicação web é construída com Flask, um framework Python robusto e flexível, que garante performance e escalabilidade. O banco de dados SQLite oferece confiabilidade e simplicidade de manutenção, adequado para o porte da Roma Confecções.

A interface de usuário utiliza TailwindCSS para um design moderno e responsivo, garantindo uma experiência de uso agradável tanto em computadores quanto em dispositivos móveis. O sistema de autenticação e autorização garante que apenas usuários autorizados tenham acesso às funcionalidades, com diferentes níveis de permissão conforme o perfil do usuário.

A arquitetura modular do sistema facilita a manutenção e futuras expansões, permitindo que novas funcionalidades sejam adicionadas sem comprometer o funcionamento das existentes. A integração com APIs externas, como o Bling, é realizada de forma segura e confiável, com tratamento adequado de erros e validações.

---

## Primeiros Passos

### Acessando o Sistema

Para acessar o ERP ROMA, abra seu navegador web preferido e digite o endereço fornecido pelo administrador do sistema. A tela de login será exibida, solicitando seu e-mail e senha de acesso.

O sistema foi otimizado para funcionar nos principais navegadores modernos, incluindo Google Chrome, Mozilla Firefox, Safari e Microsoft Edge. Para uma melhor experiência, recomenda-se utilizar as versões mais recentes destes navegadores.

### Realizando o Login

Na tela de login, insira seu e-mail cadastrado no campo "E-mail" e sua senha no campo "Senha". Certifique-se de digitar as informações corretamente, respeitando maiúsculas e minúsculas. Caso tenha esquecido sua senha, entre em contato com o administrador do sistema para solicitar uma nova senha.

Após inserir suas credenciais, clique no botão "Entrar" para acessar o sistema. Se as informações estiverem corretas, você será redirecionado para o dashboard principal. Caso contrário, uma mensagem de erro será exibida, solicitando que verifique suas credenciais.

### Navegação no Sistema

A interface do ERP ROMA foi projetada para ser intuitiva e fácil de usar. A navegação principal está localizada na barra lateral esquerda, onde você encontrará todos os módulos do sistema organizados de forma lógica.

O cabeçalho superior exibe o logo da Roma Confecções, o título da página atual e informações do usuário logado. No canto superior direito, você encontrará o menu do usuário, onde pode alterar sua senha ou fazer logout do sistema.

Cada módulo possui sua própria estrutura de navegação, com opções para listar, criar, editar e visualizar registros. Os botões de ação são claramente identificados com ícones e textos descritivos, facilitando a identificação das funcionalidades disponíveis.

### Alterando sua Senha

Para alterar sua senha, clique no seu nome no canto superior direito da tela e selecione "Alterar Senha" no menu suspenso. Na tela que se abrirá, digite sua senha atual no campo "Senha Atual", depois digite sua nova senha nos campos "Nova Senha" e "Confirmar Nova Senha".

O sistema possui validações de segurança para senhas, exigindo que a nova senha tenha pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e símbolos especiais. Esta política de senhas garante maior segurança para sua conta e para o sistema como um todo.

Após preencher todos os campos corretamente, clique em "Alterar Senha" para confirmar a alteração. Uma mensagem de confirmação será exibida, e você poderá continuar usando o sistema normalmente com sua nova senha.

### Fazendo Logout

Para sair do sistema com segurança, clique no seu nome no canto superior direito da tela e selecione "Sair" no menu suspenso. Você será redirecionado para a tela de login, e sua sessão será encerrada de forma segura.

É importante sempre fazer logout quando terminar de usar o sistema, especialmente se estiver utilizando um computador compartilhado. Isso garante que outras pessoas não tenham acesso às informações do sistema usando sua conta.

---



## Módulo de Usuários

O módulo de usuários é responsável pelo gerenciamento de todas as pessoas que têm acesso ao sistema ERP ROMA. Este módulo é fundamental para manter a segurança e organização do sistema, permitindo que diferentes usuários tenham acesso apenas às funcionalidades apropriadas para suas funções na empresa.

### Perfis de Usuário

O sistema ERP ROMA trabalha com três perfis distintos de usuário, cada um com permissões específicas adequadas às responsabilidades de cada função na empresa.

O perfil de **Administrador** possui acesso completo a todas as funcionalidades do sistema. Usuários com este perfil podem criar, editar e excluir registros em todos os módulos, além de ter acesso exclusivo às funcionalidades de administração, como gerenciamento de usuários, configurações de backup e monitoramento de segurança. Este perfil deve ser atribuído apenas aos responsáveis pela gestão geral do sistema e da empresa.

O perfil de **Gestor** tem acesso à maioria das funcionalidades operacionais do sistema, podendo gerenciar clientes, produtos, fornecedores, produção e finanças. No entanto, gestores não têm acesso às funcionalidades administrativas do sistema, como criação de usuários ou configurações de segurança. Este perfil é adequado para supervisores e coordenadores que precisam de acesso amplo às operações, mas não às configurações críticas do sistema.

O perfil de **Visualizador** possui acesso apenas para consulta e visualização de informações. Usuários com este perfil podem acessar relatórios, dashboards e consultar registros, mas não podem criar, editar ou excluir informações. Este perfil é ideal para funcionários que precisam consultar informações para suas atividades, mas não têm responsabilidade pela manutenção dos dados.

### Listagem de Usuários

Para acessar a listagem de usuários, clique em "Usuários" na barra lateral esquerda. A tela exibirá uma tabela com todos os usuários cadastrados no sistema, mostrando informações como nome, e-mail, perfil, status (ativo/inativo) e data do último acesso.

A listagem inclui funcionalidades de busca que permitem localizar rapidamente usuários específicos. Digite o nome ou e-mail do usuário desejado no campo de busca e pressione Enter ou clique no ícone de lupa para filtrar os resultados. A busca é realizada em tempo real, facilitando a localização de usuários em sistemas com muitos cadastros.

Cada linha da tabela possui botões de ação que permitem visualizar detalhes do usuário, editar informações ou desativar/ativar a conta. O botão "Ver" abre uma tela com informações detalhadas do usuário, incluindo histórico de acessos e atividades recentes. O botão "Editar" permite alterar informações do usuário, como nome, e-mail e perfil. O botão "Ativar/Desativar" permite controlar o acesso do usuário ao sistema sem excluir permanentemente a conta.

### Cadastrando Novos Usuários

Para cadastrar um novo usuário, clique no botão "Novo Usuário" localizado no canto superior direito da listagem de usuários. Um formulário será exibido com os campos necessários para o cadastro.

O campo "Nome Completo" deve conter o nome completo do usuário, incluindo nome e sobrenome. Esta informação será exibida no sistema e em relatórios, portanto deve ser preenchida de forma clara e profissional.

O campo "E-mail" deve conter um endereço de e-mail válido e único no sistema. Este e-mail será utilizado como login do usuário e também para comunicações do sistema, como notificações de alteração de senha ou alertas importantes.

O campo "Perfil" permite selecionar o nível de acesso do usuário entre Administrador, Gestor ou Visualizador. Escolha o perfil mais adequado às responsabilidades do usuário na empresa, seguindo o princípio do menor privilégio necessário.

Os campos "Senha" e "Confirmar Senha" devem conter uma senha segura que atenda aos critérios de segurança do sistema. A senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e símbolos especiais. A confirmação da senha garante que não houve erro de digitação.

Após preencher todos os campos, clique em "Salvar" para criar o usuário. O sistema validará as informações e, se tudo estiver correto, o usuário será criado e uma mensagem de confirmação será exibida. O novo usuário poderá fazer login imediatamente usando o e-mail e senha cadastrados.

### Editando Usuários

Para editar informações de um usuário existente, localize o usuário na listagem e clique no botão "Editar" correspondente. Um formulário será exibido com as informações atuais do usuário, permitindo alterações.

Você pode alterar o nome, e-mail e perfil do usuário conforme necessário. Caso precise alterar a senha do usuário, marque a opção "Alterar Senha" e preencha os campos de nova senha. Se esta opção não for marcada, a senha atual do usuário será mantida.

É importante ter cuidado ao alterar o perfil de usuários, especialmente ao conceder ou remover privilégios de administrador. Certifique-se de que a alteração está alinhada com as responsabilidades do usuário na empresa e com as políticas de segurança estabelecidas.

Após fazer as alterações necessárias, clique em "Salvar" para confirmar as modificações. O sistema validará as informações e atualizará o cadastro do usuário. Se o usuário estiver logado no momento da alteração, ele precisará fazer login novamente para que as mudanças de perfil tenham efeito.

### Desativando Usuários

Em vez de excluir usuários permanentemente, o sistema permite desativar contas quando um funcionário deixa a empresa ou temporariamente não precisa de acesso ao sistema. Para desativar um usuário, localize-o na listagem e clique no botão "Desativar".

Usuários desativados não conseguem fazer login no sistema, mas seus registros e histórico de atividades são preservados. Isso é importante para manter a integridade dos dados históricos e para auditoria. Caso o usuário precise ter acesso novamente no futuro, a conta pode ser reativada facilmente.

Para reativar um usuário, localize-o na listagem (usuários desativados aparecem com status "Inativo") e clique no botão "Ativar". O usuário poderá fazer login imediatamente usando suas credenciais anteriores.

---

## Módulo de Clientes

O módulo de clientes é essencial para o gerenciamento de todos os relacionamentos comerciais da Roma Confecções. Este módulo permite o cadastro completo de informações dos clientes, incluindo dados pessoais, de contato, endereço e informações fiscais necessárias para a emissão de notas fiscais e controle comercial.

### Características do Cadastro de Clientes

O cadastro de clientes do ERP ROMA foi desenvolvido para atender às necessidades específicas do mercado B2B brasileiro, incluindo todas as informações necessárias para relacionamentos comerciais e conformidade fiscal. O sistema suporta tanto pessoas físicas quanto jurídicas, adaptando automaticamente os campos obrigatórios conforme o tipo de cliente.

Para pessoas jurídicas, o sistema coleta informações como razão social, nome fantasia, CNPJ, inscrição estadual e municipal, além de dados de contato e endereço completo. Para pessoas físicas, são coletados nome completo, CPF, RG e demais informações de contato. Esta flexibilidade permite que a Roma Confecções mantenha relacionamentos tanto com empresas quanto com pessoas físicas, conforme a necessidade do negócio.

O sistema inclui validações automáticas para documentos como CNPJ e CPF, garantindo que apenas números válidos sejam aceitos. Além disso, o sistema verifica a unicidade destes documentos, impedindo o cadastro duplicado de clientes com o mesmo CNPJ ou CPF.

### Listagem de Clientes

Para acessar a listagem de clientes, clique em "Clientes" na barra lateral esquerda. A tela exibirá uma tabela com todos os clientes cadastrados, mostrando informações essenciais como nome/razão social, tipo (pessoa física ou jurídica), documento (CPF/CNPJ), e-mail, telefone e status.

A listagem inclui funcionalidades avançadas de busca e filtro que facilitam a localização de clientes específicos. Você pode buscar por nome, razão social, CNPJ, CPF ou e-mail digitando no campo de busca. O sistema realiza a busca em tempo real, exibindo apenas os clientes que correspondem aos critérios informados.

Além da busca textual, você pode filtrar clientes por tipo (pessoa física ou jurídica) e status (ativo ou inativo) usando os filtros disponíveis acima da tabela. Estes filtros podem ser combinados para refinar ainda mais os resultados, facilitando a gestão de grandes bases de clientes.

Cada linha da tabela possui botões de ação que permitem visualizar detalhes completos do cliente, editar informações, visualizar histórico de produções e pedidos, ou desativar/ativar o cadastro. O botão "Ver" abre uma tela detalhada com todas as informações do cliente e seu histórico comercial.

### Cadastrando Novos Clientes

Para cadastrar um novo cliente, clique no botão "Novo Cliente" localizado no canto superior direito da listagem. Um formulário será exibido com campos organizados em seções lógicas para facilitar o preenchimento.

A primeira seção, "Informações Básicas", inclui campos fundamentais como tipo de pessoa (física ou jurídica), nome ou razão social, e nome fantasia (para pessoas jurídicas). O campo "Tipo" determina quais outros campos serão obrigatórios, adaptando automaticamente o formulário.

Para pessoas jurídicas, os campos "Razão Social" e "CNPJ" são obrigatórios. O campo "Nome Fantasia" é opcional, mas recomendado para facilitar a identificação do cliente. O sistema valida automaticamente o CNPJ digitado, verificando se o número é válido e se não está duplicado no sistema.

Para pessoas físicas, os campos "Nome Completo" e "CPF" são obrigatórios. O campo "RG" é opcional, mas pode ser útil para identificação adicional. Assim como com o CNPJ, o sistema valida automaticamente o CPF e verifica duplicidade.

A seção "Informações de Contato" inclui campos para e-mail, telefone principal e telefone secundário. O e-mail é obrigatório e deve ser único no sistema. Os telefones devem ser preenchidos com DDD e número, seguindo o formato brasileiro.

A seção "Endereço" coleta informações completas de localização, incluindo CEP, logradouro, número, complemento, bairro, cidade e estado. O campo CEP possui integração com serviços de consulta que preenchem automaticamente os campos de endereço quando um CEP válido é informado.

A seção "Informações Fiscais" é específica para pessoas jurídicas e inclui campos como inscrição estadual, inscrição municipal e regime tributário. Estas informações são essenciais para a emissão correta de notas fiscais.

Após preencher todos os campos obrigatórios, clique em "Salvar" para criar o cliente. O sistema validará todas as informações e, se tudo estiver correto, o cliente será cadastrado e uma mensagem de confirmação será exibida.

### Editando Clientes

Para editar informações de um cliente existente, localize o cliente na listagem e clique no botão "Editar". O formulário de edição será exibido com todas as informações atuais do cliente, permitindo alterações em qualquer campo.

É importante ter cuidado ao alterar informações fiscais como CNPJ, inscrição estadual ou endereço, pois estas alterações podem afetar a emissão de notas fiscais futuras. Certifique-se de que as informações estão corretas e atualizadas conforme a documentação oficial do cliente.

Caso o cliente tenha histórico de produções ou notas fiscais emitidas, o sistema exibirá um aviso antes de permitir alterações em campos críticos como CNPJ ou razão social. Isso garante que você esteja ciente do impacto das alterações nos registros históricos.

Após fazer as alterações necessárias, clique em "Salvar" para confirmar as modificações. O sistema validará as informações atualizadas e confirmará a alteração com uma mensagem de sucesso.

### Visualizando Detalhes e Histórico

A tela de detalhes do cliente, acessada através do botão "Ver" na listagem, oferece uma visão completa de todas as informações cadastradas e do histórico comercial do cliente com a Roma Confecções.

A seção superior exibe todas as informações cadastrais do cliente de forma organizada e clara. Logo abaixo, você encontrará abas com diferentes tipos de histórico e estatísticas relacionadas ao cliente.

A aba "Produções" mostra todas as produções realizadas para o cliente, incluindo datas, produtos, quantidades e valores. Esta informação é valiosa para entender o padrão de consumo do cliente e identificar oportunidades comerciais.

A aba "Notas Fiscais" lista todas as notas fiscais emitidas para o cliente, com informações sobre números, datas, valores e status. Isso facilita o controle fiscal e o acompanhamento de pendências.

A aba "Estatísticas" apresenta gráficos e indicadores sobre o relacionamento comercial, como volume de compras por período, produtos mais consumidos e evolução do faturamento. Estas informações são úteis para análises comerciais e tomada de decisões estratégicas.

---

## Módulo de Produtos

O módulo de produtos é fundamental para o controle de todos os itens fabricados pela Roma Confecções. Este módulo permite o cadastro detalhado de produtos, incluindo informações técnicas, comerciais, fiscais e de composição, proporcionando controle completo sobre o portfólio de produtos da empresa.

### Características do Cadastro de Produtos

O cadastro de produtos do ERP ROMA foi desenvolvido especificamente para atender às necessidades de uma indústria de confecção, incluindo funcionalidades específicas para controle de composição de materiais, cálculo de custos e gestão de estoque.

Cada produto pode ter uma composição detalhada de materiais, permitindo que o sistema calcule automaticamente os custos de produção e controle o consumo de matérias-primas durante a fabricação. Esta funcionalidade é essencial para o controle preciso de custos e para a gestão eficiente do estoque.

O sistema inclui campos específicos para informações fiscais, como NCM (Nomenclatura Comum do Mercosul) e origem do produto, que são obrigatórios para a emissão de notas fiscais em conformidade com a legislação brasileira. Para produtos têxteis como os fabricados pela Roma Confecções, o NCM padrão é 62092000.

O controle de estoque é integrado ao módulo de produção, permitindo que o sistema atualize automaticamente as quantidades disponíveis conforme os produtos são fabricados ou vendidos. Alertas de estoque mínimo ajudam a evitar rupturas e garantem que sempre haja produtos disponíveis para atender à demanda.

### Listagem de Produtos

Para acessar a listagem de produtos, clique em "Produtos" na barra lateral esquerda. A tela exibirá uma tabela com todos os produtos cadastrados, mostrando informações como nome, descrição, preço de venda, estoque atual, estoque mínimo e status.

A listagem inclui indicadores visuais que facilitam a identificação rápida de situações que requerem atenção. Produtos com estoque abaixo do mínimo são destacados em vermelho, alertando para a necessidade de produção ou reposição. Produtos inativos aparecem com formatação diferenciada, facilitando a distinção entre produtos em linha e descontinuados.

As funcionalidades de busca permitem localizar produtos por nome, descrição ou código. O sistema também oferece filtros por categoria, status (ativo/inativo) e situação de estoque (normal, baixo, zerado), facilitando a gestão de grandes catálogos de produtos.

Cada linha da tabela possui botões de ação para visualizar detalhes completos do produto, editar informações, gerenciar composição de materiais, visualizar histórico de movimentações de estoque, ou ativar/desativar o produto.

### Cadastrando Novos Produtos

Para cadastrar um novo produto, clique no botão "Novo Produto" na listagem. O formulário de cadastro está organizado em seções que agrupam informações relacionadas para facilitar o preenchimento.

A seção "Informações Básicas" inclui campos fundamentais como nome do produto, descrição detalhada e categoria. O nome deve ser claro e descritivo, facilitando a identificação do produto em listas e relatórios. A descrição pode incluir detalhes técnicos, especificações ou características especiais do produto.

A seção "Informações Comerciais" inclui o preço de venda do produto. Este preço será utilizado como padrão em produções e na emissão de notas fiscais, mas pode ser alterado conforme necessário em cada transação específica.

A seção "Controle de Estoque" permite definir as quantidades de estoque atual e estoque mínimo. O estoque atual representa a quantidade disponível no momento do cadastro, enquanto o estoque mínimo define o ponto de reposição que acionará alertas no sistema.

A seção "Informações Fiscais" é crucial para a conformidade legal e inclui campos como NCM, origem do produto e outras informações necessárias para a emissão de notas fiscais. Para produtos têxteis, o NCM padrão é 62092000, e a origem é tipicamente 0 (nacional) para produtos fabricados no Brasil.

Após preencher todas as informações básicas e salvar o produto, você poderá definir sua composição de materiais através da funcionalidade específica de gestão de composição.

### Gerenciando Composição de Materiais

A composição de materiais é uma funcionalidade avançada que permite definir quais matérias-primas são necessárias para fabricar cada produto e em que quantidades. Esta informação é fundamental para o cálculo de custos e para o controle automático de estoque durante a produção.

Para acessar a gestão de composição, visualize os detalhes de um produto e clique na aba "Composição". Nesta tela, você verá a lista atual de materiais que compõem o produto, se houver algum já cadastrado.

Para adicionar um material à composição, clique no botão "Adicionar Material". Um formulário será exibido onde você deve selecionar o material desejado da lista de materiais cadastrados e informar a quantidade necessária para produzir uma unidade do produto.

Por exemplo, se uma mochila específica requer 2 metros de tecido, 1 zíper e 2 metros de fita, você adicionaria três itens à composição: tecido (quantidade 2), zíper (quantidade 1) e fita (quantidade 2). Quando uma unidade desta mochila for produzida, o sistema automaticamente reduzirá o estoque destes materiais nas quantidades especificadas.

A composição pode ser alterada a qualquer momento, permitindo ajustes conforme mudanças no processo produtivo ou especificações do produto. No entanto, alterações na composição afetam apenas produções futuras, não alterando o histórico de produções já realizadas.

O sistema calcula automaticamente o custo de materiais do produto com base na composição e nos preços dos materiais cadastrados. Esta informação é valiosa para análises de rentabilidade e definição de preços de venda.

### Controle de Estoque de Produtos

O controle de estoque de produtos é totalmente integrado ao módulo de produção, garantindo que as quantidades sejam atualizadas automaticamente conforme os produtos são fabricados. Quando uma produção é finalizada, o sistema adiciona as quantidades produzidas ao estoque disponível.

A tela de detalhes do produto inclui uma aba "Movimentações" que mostra o histórico completo de entradas e saídas do estoque, incluindo data, tipo de movimentação, quantidade e saldo resultante. Este histórico é importante para auditoria e para entender os padrões de consumo e produção.

O sistema gera alertas automáticos quando o estoque de um produto fica abaixo do mínimo definido. Estes alertas aparecem no dashboard principal e podem ser configurados para envio por e-mail, garantindo que a equipe seja notificada rapidamente sobre a necessidade de produção.

Ajustes manuais de estoque podem ser realizados quando necessário, por exemplo, para corrigir divergências identificadas em inventários físicos. Estes ajustes são registrados no histórico de movimentações com justificativa, mantendo a rastreabilidade completa.

---


## Módulo de Produção

O módulo de produção é o coração do ERP ROMA, gerenciando todo o processo produtivo da Roma Confecções. Este módulo permite o registro detalhado de todas as produções realizadas, com controle de itens produzidos, quantidades, valores e consumo automático de materiais, garantindo precisão no controle de custos e estoques.

### Visão Geral do Processo Produtivo

O processo produtivo no ERP ROMA foi modelado para refletir o fluxo real de trabalho da Roma Confecções, desde o registro inicial da produção até sua finalização e impacto nos estoques. O sistema acompanha cada etapa do processo, garantindo controle e rastreabilidade completos.

Uma produção no sistema passa por diferentes status que refletem seu progresso: "Em Andamento", quando a produção está sendo registrada e ainda pode receber novos itens; "Finalizada", quando a produção foi concluída e os estoques foram atualizados; e "Cancelada", quando a produção foi interrompida por algum motivo e não afetará os estoques.

Cada produção está associada a um cliente específico, permitindo análises detalhadas de produção por cliente e facilitando o controle comercial. A data da produção é registrada para análises temporais e relatórios de produtividade por período.

O sistema calcula automaticamente o valor total da produção com base nos itens produzidos e seus preços de venda. Este valor pode ser utilizado posteriormente para faturamento e emissão de notas fiscais, garantindo consistência entre a produção e o faturamento.

### Listagem de Produções

Para acessar a listagem de produções, clique em "Produção" na barra lateral esquerda. A tela exibirá uma tabela com todas as produções registradas, mostrando informações como número da produção, data, cliente, valor total, status e observações.

A listagem inclui funcionalidades avançadas de busca e filtro que facilitam a localização de produções específicas. Você pode filtrar por período (hoje, esta semana, este mês, personalizado), por cliente, por status ou por faixa de valor. Estes filtros podem ser combinados para refinar ainda mais os resultados.

Cada linha da tabela possui botões de ação para visualizar detalhes completos da produção, adicionar itens (se em andamento), finalizar a produção ou cancelá-la. O botão "Ver" abre uma tela detalhada com todas as informações da produção, incluindo a lista completa de itens produzidos.

A listagem também inclui um resumo estatístico no topo da página, mostrando indicadores como total de produções no período, valor total produzido, média diária e comparativo com períodos anteriores. Estas informações são valiosas para análises rápidas de desempenho produtivo.

### Registrando Nova Produção

Para registrar uma nova produção, clique no botão "Nova Produção" na listagem. O formulário de registro inicial solicita informações básicas como data da produção, cliente e observações.

A data da produção é preenchida automaticamente com a data atual, mas pode ser alterada se necessário, por exemplo, para registrar produções de dias anteriores. O cliente deve ser selecionado da lista de clientes cadastrados no sistema, garantindo a integridade dos dados e facilitando análises futuras.

O campo de observações é opcional, mas pode ser útil para registrar informações adicionais sobre a produção, como condições especiais, detalhes de entrega ou outras notas relevantes para a equipe.

Após preencher estas informações iniciais e clicar em "Salvar", a produção será criada com status "Em Andamento" e você será redirecionado para a tela de detalhes, onde poderá adicionar os itens produzidos.

### Adicionando Itens à Produção

Na tela de detalhes de uma produção em andamento, clique no botão "Adicionar Item" para registrar os produtos fabricados. Um formulário será exibido onde você deve selecionar o produto da lista de produtos cadastrados e informar a quantidade produzida.

O sistema preencherá automaticamente o valor unitário com o preço de venda cadastrado para o produto, mas este valor pode ser alterado se necessário, por exemplo, para aplicar descontos específicos ou preços diferenciados para determinados clientes.

Após adicionar o item, o sistema calculará automaticamente o valor total (quantidade × valor unitário) e atualizará o valor total da produção. Você pode adicionar quantos itens forem necessários à mesma produção, permitindo o registro de lotes com múltiplos produtos.

Itens adicionados podem ser editados ou removidos enquanto a produção estiver com status "Em Andamento". Após a finalização da produção, não será mais possível alterar os itens, garantindo a integridade dos registros históricos e dos controles de estoque.

### Finalizando a Produção

Quando todos os itens da produção foram registrados e as informações estão corretas, você pode finalizar a produção clicando no botão "Finalizar Produção" na tela de detalhes. Uma confirmação será solicitada, pois esta ação não poderá ser desfeita e afetará os estoques.

Ao finalizar uma produção, o sistema realiza automaticamente as seguintes ações:

1. Atualiza o status da produção para "Finalizada"
2. Adiciona as quantidades produzidas ao estoque de produtos acabados
3. Reduz o estoque de materiais conforme a composição de cada produto
4. Registra a data e hora de finalização e o usuário responsável
5. Gera entradas no histórico de movimentações de estoque

Se algum material não tiver estoque suficiente para a produção, o sistema exibirá um alerta, mas permitirá a finalização, registrando um estoque negativo que deverá ser regularizado posteriormente. Esta flexibilidade é importante para não interromper o fluxo de trabalho em situações onde o estoque físico existe, mas não foi corretamente registrado no sistema.

Após a finalização, a produção não poderá mais ser editada, garantindo a integridade dos registros históricos e dos controles de estoque. Caso seja necessário corrigir alguma informação, será preciso registrar ajustes de estoque separadamente.

### Cancelando Produções

Em situações excepcionais, pode ser necessário cancelar uma produção, por exemplo, quando ela foi registrada por engano ou quando houve mudanças significativas que tornam mais prático cancelar e criar uma nova produção.

Para cancelar uma produção, ela deve estar com status "Em Andamento". Produções já finalizadas não podem ser canceladas, pois já afetaram os estoques. Na tela de detalhes da produção, clique no botão "Cancelar Produção" e confirme a ação quando solicitado.

Ao cancelar uma produção, o sistema altera seu status para "Cancelada" e a exclui de relatórios e estatísticas de produção. Produções canceladas permanecem no histórico para fins de auditoria, mas são claramente identificadas como canceladas em todas as listagens e relatórios.

### Relatórios de Produção

O módulo de produção inclui relatórios detalhados que permitem análises aprofundadas do processo produtivo. Para acessar os relatórios, clique em "Relatórios" no menu de produção.

O "Relatório de Produção por Período" permite visualizar todas as produções realizadas em um intervalo de datas específico, com totais por dia, semana ou mês. Este relatório é útil para análises de sazonalidade e planejamento de capacidade produtiva.

O "Relatório de Produção por Cliente" mostra o volume de produção para cada cliente em um período selecionado, facilitando a identificação dos principais clientes e a análise de concentração de vendas.

O "Relatório de Produção por Produto" detalha quais produtos foram mais produzidos em um determinado período, ajudando a identificar os itens mais populares e orientar decisões de estoque e desenvolvimento de produtos.

Todos os relatórios podem ser exportados em formato PDF para compartilhamento ou arquivamento, e incluem gráficos visuais que facilitam a interpretação dos dados e a identificação de tendências.

---

## Módulo Financeiro

O módulo financeiro do ERP ROMA proporciona controle completo sobre as finanças da Roma Confecções, incluindo fluxo de caixa, contas a pagar e receber, e emissão de notas fiscais. Este módulo é fundamental para manter a saúde financeira da empresa e garantir conformidade fiscal.

### Fluxo de Caixa

O fluxo de caixa é o coração do módulo financeiro, registrando todas as entradas e saídas de recursos da empresa. Para acessar o fluxo de caixa, clique em "Financeiro" na barra lateral e depois em "Fluxo de Caixa" no submenu.

A tela principal do fluxo de caixa apresenta um resumo das movimentações do período selecionado, com totais de receitas, despesas e saldo resultante. Um gráfico visual facilita a compreensão da evolução do fluxo ao longo do tempo, permitindo identificar rapidamente tendências e padrões.

A listagem de movimentações mostra todas as transações do período, incluindo data, tipo (receita ou despesa), categoria, descrição, valor e status. Filtros avançados permitem refinar a visualização por tipo, categoria, forma de pagamento, status ou faixa de valor.

Cada movimentação pode ser visualizada em detalhes, editada (se ainda não estiver confirmada) ou ter seu status alterado. O sistema mantém um histórico completo de alterações para fins de auditoria e controle.

### Registrando Movimentações Financeiras

Para registrar uma nova movimentação financeira, clique no botão "Nova Movimentação" na tela de fluxo de caixa. Um formulário será exibido solicitando as informações necessárias.

O campo "Tipo" define se a movimentação é uma receita (entrada de recursos) ou despesa (saída de recursos). Esta é a classificação mais básica e afeta como a movimentação será contabilizada no fluxo de caixa.

O campo "Categoria" permite classificar a movimentação de forma mais específica, como "Venda", "Serviço", "Compra de Material", "Aluguel", "Salários", etc. Estas categorias são fundamentais para análises detalhadas e relatórios gerenciais.

A data da movimentação é preenchida automaticamente com a data atual, mas pode ser alterada para registrar transações passadas ou futuras. Para movimentações futuras, o status será automaticamente definido como "Pendente".

O campo "Descrição" deve conter uma explicação clara sobre a movimentação, facilitando sua identificação posterior. Para receitas, pode-se incluir o nome do cliente ou o número da nota fiscal; para despesas, o fornecedor ou a finalidade do gasto.

O valor da movimentação deve ser informado sem símbolos monetários, apenas os números e a separação decimal. O sistema formatará automaticamente o valor conforme a moeda configurada (R$ para o Brasil).

O campo "Forma de Pagamento" permite registrar como a transação foi ou será liquidada: dinheiro, cartão de crédito, cartão de débito, transferência bancária, PIX, boleto, etc. Esta informação é útil para conciliações bancárias e controle de meios de pagamento.

O status da movimentação pode ser "Pendente" (ainda não efetivada), "Confirmada" (já efetivada) ou "Cancelada" (não será efetivada). Movimentações pendentes são consideradas em projeções futuras, mas não afetam o saldo atual.

Após preencher todos os campos, clique em "Salvar" para registrar a movimentação. O sistema atualizará automaticamente os totais e gráficos do fluxo de caixa.

### Categorias Financeiras

As categorias financeiras permitem uma classificação detalhada das movimentações, facilitando análises gerenciais e a identificação de oportunidades de otimização. O ERP ROMA vem com categorias pré-configuradas, mas você pode personalizar conforme as necessidades específicas da Roma Confecções.

Para gerenciar categorias, acesse "Financeiro" > "Configurações" > "Categorias". A tela exibirá a lista de categorias existentes, separadas por tipo (receita ou despesa). Você pode adicionar novas categorias, editar as existentes ou desativar as que não são mais necessárias.

Cada categoria possui um nome, uma descrição opcional e um tipo (receita ou despesa). Categorias bem definidas são essenciais para relatórios financeiros precisos e análises detalhadas de desempenho.

Exemplos de categorias de receita incluem "Venda de Produtos", "Serviços de Customização", "Devoluções", etc. Para despesas, exemplos comuns são "Compra de Materiais", "Salários", "Aluguel", "Energia Elétrica", "Marketing", entre outros.

O sistema permite a criação de subcategorias para uma classificação ainda mais detalhada. Por exemplo, dentro da categoria "Compra de Materiais", podem existir subcategorias como "Tecidos", "Aviamentos", "Embalagens", etc.

### Notas Fiscais

O módulo de notas fiscais permite o gerenciamento completo dos documentos fiscais emitidos pela Roma Confecções, com integração direta com o sistema Bling para emissão oficial. Para acessar este módulo, clique em "Financeiro" > "Notas Fiscais".

A tela principal lista todas as notas fiscais registradas no sistema, com informações como número, série, data de emissão, cliente, valor total e status. Filtros permitem refinar a visualização por período, cliente, status ou faixa de valor.

Cada nota fiscal pode ser visualizada em detalhes, incluindo todos os itens, valores, impostos e informações fiscais. Notas já emitidas podem ser consultadas, canceladas (se dentro do prazo legal) ou ter segunda via gerada.

### Emitindo Notas Fiscais

Para emitir uma nova nota fiscal, clique no botão "Nova Nota Fiscal" na listagem. O processo de emissão está dividido em etapas para facilitar o preenchimento correto de todas as informações necessárias.

Na primeira etapa, selecione o cliente para quem a nota será emitida. O sistema preencherá automaticamente todas as informações cadastrais e fiscais do cliente, como CNPJ, inscrição estadual e endereço.

Na segunda etapa, adicione os produtos que farão parte da nota fiscal. Você pode selecionar produtos do cadastro ou adicionar itens manualmente. Para cada item, informe a quantidade e o valor unitário. O sistema calculará automaticamente os valores totais e impostos aplicáveis.

Na terceira etapa, revise todas as informações da nota fiscal, incluindo dados do cliente, itens, valores e impostos. Certifique-se de que tudo está correto antes de prosseguir, pois após a emissão oficial, alterações podem ser complexas ou impossíveis.

Na etapa final, clique em "Emitir Nota Fiscal" para enviar os dados ao Bling e gerar a nota fiscal oficial. O sistema se comunicará com a API do Bling, enviando todas as informações necessárias e recebendo o número da nota, chave de acesso e link para o PDF.

Após a emissão bem-sucedida, a nota fiscal será registrada no sistema com status "Emitida" e estará disponível para consulta, impressão ou envio ao cliente. Uma movimentação financeira de receita será automaticamente criada, vinculada à nota fiscal emitida.

### Integração com Bling

A integração com o Bling permite a emissão oficial de notas fiscais diretamente do ERP ROMA, sem necessidade de retrabalho ou digitação em sistemas separados. Esta integração garante conformidade fiscal e agilidade no processo de faturamento.

Para configurar a integração, acesse "Financeiro" > "Configurações" > "Integração Bling". Você precisará informar a API Key fornecida pelo Bling, que pode ser obtida no painel administrativo da sua conta Bling.

Após configurar a API Key, o sistema realizará um teste de conexão para garantir que tudo está funcionando corretamente. Se o teste for bem-sucedido, a integração estará pronta para uso.

A integração sincroniza automaticamente informações de clientes, produtos e notas fiscais entre os sistemas, garantindo consistência e eliminando a necessidade de cadastros duplicados. Alterações em cadastros podem ser sincronizadas manualmente ou automaticamente, conforme configuração.

Todas as comunicações com o Bling são registradas em logs detalhados, permitindo auditoria e resolução de problemas caso necessário. Estes logs incluem data, hora, tipo de operação, dados enviados e resposta recebida.

### Relatórios Financeiros

O módulo financeiro inclui relatórios detalhados que permitem análises aprofundadas da saúde financeira da empresa. Para acessar os relatórios, clique em "Financeiro" > "Relatórios".

O "Relatório de Fluxo de Caixa" apresenta todas as movimentações de um período selecionado, agrupadas por dia, semana ou mês, com totais de receitas, despesas e saldo. Este relatório é fundamental para o controle financeiro diário e planejamento de curto prazo.

O "Relatório por Categoria" detalha as movimentações agrupadas por categoria, permitindo identificar as principais fontes de receita e os maiores grupos de despesa. Este relatório é valioso para análises de rentabilidade e controle de custos.

O "Relatório de Projeção" utiliza movimentações pendentes e recorrentes para projetar o fluxo de caixa futuro, ajudando no planejamento financeiro e na antecipação de necessidades de capital ou oportunidades de investimento.

O "Relatório de Notas Fiscais" lista todas as notas fiscais emitidas em um período, com totais por cliente, por produto ou por mês. Este relatório é útil para controle fiscal e análises comerciais.

Todos os relatórios podem ser exportados em formato PDF ou CSV para análises externas, apresentações ou arquivamento. Gráficos visuais complementam os dados numéricos, facilitando a interpretação e a identificação de tendências.

---

## Dashboard e Relatórios

O módulo de dashboard e relatórios do ERP ROMA proporciona uma visão consolidada e estratégica de todos os aspectos do negócio, permitindo análises rápidas e tomadas de decisão baseadas em dados. Este módulo transforma os dados operacionais em informações gerenciais valiosas para a direção da Roma Confecções.

### Dashboard Principal

O dashboard principal é a primeira tela exibida após o login no sistema, oferecendo uma visão geral do estado atual da empresa. Para acessá-lo a qualquer momento, clique em "Dashboard" na barra lateral esquerda.

A parte superior do dashboard apresenta cards com indicadores-chave de desempenho (KPIs) atualizados em tempo real, incluindo:

- Total de clientes ativos
- Total de produtos cadastrados
- Valor total em estoque
- Produções do mês atual
- Faturamento do mês atual
- Saldo financeiro atual

Cada card é colorido conforme o status do indicador (verde para positivo, amarelo para atenção, vermelho para crítico) e inclui um comparativo com o período anterior, facilitando a identificação rápida de tendências.

A seção central do dashboard contém gráficos interativos que mostram a evolução de métricas importantes ao longo do tempo, como produção mensal, faturamento, fluxo de caixa e estoque. Estes gráficos podem ser filtrados por período (semana, mês, trimestre, ano) e permitem drill-down para análises mais detalhadas.

A parte inferior do dashboard exibe listas das informações mais recentes ou que requerem atenção, como últimas produções, próximos vencimentos financeiros, produtos com estoque baixo e últimas notas fiscais emitidas. Estas listas funcionam como atalhos para os registros completos nos respectivos módulos.

### Personalizando o Dashboard

O dashboard pode ser personalizado para atender às necessidades específicas de cada usuário ou perfil. Para personalizar, clique no ícone de engrenagem no canto superior direito do dashboard.

Na tela de personalização, você pode selecionar quais KPIs deseja exibir nos cards principais, escolher os gráficos mais relevantes para seu trabalho e definir quais listas de informações devem aparecer na parte inferior.

Diferentes configurações podem ser salvas para diferentes perfis de usuário. Por exemplo, um gestor financeiro pode priorizar indicadores de faturamento e fluxo de caixa, enquanto um gestor de produção pode focar em métricas de produtividade e estoque.

As configurações de personalização são salvas por usuário, permitindo que cada pessoa tenha sua própria visão otimizada do dashboard sem afetar os demais usuários do sistema.

### Relatórios Integrados

Além do dashboard, o ERP ROMA oferece um conjunto abrangente de relatórios integrados que permitem análises detalhadas de todos os aspectos do negócio. Para acessar os relatórios, clique em "Relatórios" na barra lateral.

A tela principal de relatórios apresenta os relatórios disponíveis organizados por categoria: Clientes, Produtos, Produção, Estoque, Financeiro e Gerencial. Cada relatório pode ser configurado com filtros específicos antes de ser gerado.

O "Relatório de Clientes" permite análises detalhadas da base de clientes, incluindo volume de compras por cliente, frequência de pedidos, ticket médio e histórico de relacionamento. Este relatório é valioso para estratégias comerciais e programas de fidelização.

O "Relatório de Produtos" detalha o desempenho do portfólio, mostrando os produtos mais vendidos, margens de contribuição, giro de estoque e tendências de demanda. Estas informações são fundamentais para decisões de desenvolvimento de produtos e gestão de portfólio.

O "Relatório de Produção" analisa a eficiência produtiva, com métricas como volume diário, produtividade por período, custos de produção e utilização de capacidade. Este relatório ajuda a identificar gargalos e oportunidades de otimização no processo produtivo.

O "Relatório de Estoque" monitora níveis de estoque, rotatividade, itens sem movimento, valorizações e necessidades de reposição. O controle eficiente de estoque é crucial para equilibrar disponibilidade de produtos e capital imobilizado.

O "Relatório Financeiro" consolida informações de fluxo de caixa, contas a pagar e receber, faturamento e lucratividade. Análises financeiras detalhadas são essenciais para a saúde financeira e planejamento estratégico da empresa.

O "Relatório Gerencial" integra informações de todos os módulos em uma visão executiva consolidada, ideal para apresentações à diretoria e planejamento estratégico. Este relatório inclui indicadores-chave, análises de tendências e projeções futuras.

### Exportação e Compartilhamento

Todos os relatórios podem ser exportados em diversos formatos para uso externo ao sistema. Para exportar um relatório, clique no botão "Exportar" após gerá-lo e selecione o formato desejado.

O formato PDF é ideal para impressão e apresentações formais, preservando a formatação visual e os gráficos do relatório. Este formato é recomendado para compartilhamento com pessoas que não têm acesso ao sistema.

O formato CSV (valores separados por vírgula) é adequado para análises adicionais em ferramentas como Excel ou Google Sheets. Este formato exporta apenas os dados brutos, sem formatação visual ou gráficos.

O formato PNG está disponível para gráficos individuais, permitindo sua inclusão em apresentações ou documentos externos. Gráficos exportados mantêm alta resolução e fidelidade visual.

Além da exportação, relatórios podem ser agendados para geração e envio automático por e-mail em intervalos regulares (diário, semanal, mensal). Esta funcionalidade é útil para acompanhamento rotineiro de indicadores importantes sem necessidade de acesso manual ao sistema.

### Análises Avançadas

Para usuários que necessitam de análises mais profundas, o ERP ROMA oferece ferramentas de análise avançada acessíveis através do menu "Dashboard" > "Análises Avançadas".

A funcionalidade de "Análise Multidimensional" permite cruzar diferentes dimensões de dados (tempo, cliente, produto, região, etc.) para identificar padrões e correlações não evidentes em relatórios padrão. Esta análise utiliza conceitos de OLAP (Processamento Analítico Online) para exploração dinâmica de dados.

A "Análise de Tendências" aplica algoritmos estatísticos para identificar padrões temporais e projetar comportamentos futuros com base em dados históricos. Esta funcionalidade é valiosa para previsão de demanda, planejamento de produção e projeções financeiras.

A "Análise de Rentabilidade" calcula margens de contribuição detalhadas por produto, cliente ou canal, considerando não apenas receitas e custos diretos, mas também alocações de custos indiretos. Esta visão é fundamental para decisões estratégicas sobre mix de produtos e segmentação de clientes.

Estas análises avançadas são apresentadas em interfaces interativas que permitem ajustes de parâmetros e exploração dinâmica, proporcionando insights valiosos para a gestão estratégica da Roma Confecções.

---


## Administração

O módulo de administração do ERP ROMA fornece ferramentas avançadas para gerenciar aspectos técnicos e de segurança do sistema. Este módulo é acessível apenas para usuários com perfil de Administrador e contém funcionalidades críticas para a manutenção e configuração do sistema.

### Configurações do Sistema

A seção de configurações do sistema permite personalizar diversos aspectos do ERP ROMA para atender às necessidades específicas da Roma Confecções. Para acessar estas configurações, clique em "Administração" > "Configurações" na barra lateral.

As configurações gerais incluem informações da empresa como razão social, CNPJ, endereço e logotipo, que são utilizadas em relatórios, notas fiscais e na interface do sistema. Manter estas informações atualizadas é importante para a correta identificação da empresa em documentos oficiais.

As configurações de e-mail permitem definir os parâmetros do servidor SMTP utilizado para envio de notificações, relatórios agendados e alertas. É necessário informar o servidor, porta, usuário, senha e endereço de remetente. Um botão de teste permite verificar se as configurações estão corretas antes de salvá-las.

As configurações de backup definem a frequência, horário e local de armazenamento dos backups automáticos. É possível configurar backups diários, semanais ou mensais, e definir políticas de retenção para gerenciar o espaço em disco. Para usuários Mac, há opções específicas para sincronização com o iCloud.

As configurações de segurança permitem ajustar parâmetros como complexidade mínima de senhas, tempo de expiração de sessões inativas, número máximo de tentativas de login antes do bloqueio e duração do bloqueio. Estas configurações são importantes para manter a segurança do sistema sem comprometer a usabilidade.

As configurações fiscais incluem parâmetros para emissão de notas fiscais, como série padrão, próximo número, ambiente (homologação ou produção) e certificado digital. Estas configurações são críticas para a correta emissão de documentos fiscais em conformidade com a legislação.

### Gerenciamento de Logs

O sistema de logs do ERP ROMA registra todas as atividades importantes realizadas no sistema, permitindo auditoria completa e diagnóstico de problemas. Para acessar os logs, clique em "Administração" > "Logs" na barra lateral.

A tela principal de logs apresenta uma tabela com os registros mais recentes, incluindo data e hora, usuário, tipo de evento, módulo afetado e descrição detalhada. Filtros permitem refinar a visualização por período, usuário, tipo de evento ou módulo.

Os logs são categorizados em diferentes tipos para facilitar a análise:

- **Logs de Acesso**: registram login, logout e tentativas de acesso (bem-sucedidas ou falhas)
- **Logs de Dados**: registram criação, alteração e exclusão de registros importantes
- **Logs de Sistema**: registram eventos técnicos como início/parada do sistema, backups e manutenções
- **Logs de Segurança**: registram eventos relacionados à segurança, como alterações de senha e permissões
- **Logs de Erro**: registram erros e exceções que ocorreram durante a operação do sistema

Os logs podem ser exportados em formato CSV para análise externa ou arquivamento de longo prazo. O sistema mantém logs online por um período configurável (padrão de 90 dias), após o qual os registros mais antigos são arquivados para economizar espaço.

A análise regular dos logs é uma prática recomendada para identificar padrões suspeitos de uso, diagnosticar problemas recorrentes e entender como o sistema está sendo utilizado pelos diferentes usuários.

### Monitoramento de Sistema

A funcionalidade de monitoramento fornece informações em tempo real sobre o estado técnico do ERP ROMA, permitindo identificar problemas de performance ou recursos antes que afetem os usuários. Para acessar o monitoramento, clique em "Administração" > "Monitoramento" na barra lateral.

O painel de monitoramento exibe métricas como uso de CPU, memória e disco, tempo de resposta do banco de dados, número de usuários conectados e tempo de atividade do sistema. Gráficos históricos mostram a evolução destas métricas ao longo do tempo, facilitando a identificação de tendências e padrões.

Alertas automáticos são gerados quando métricas críticas ultrapassam limites predefinidos, como uso de disco acima de 90% ou tempo de resposta do banco de dados superior a 1 segundo. Estes alertas aparecem no painel de monitoramento e podem ser configurados para envio por e-mail aos administradores.

O monitoramento de banco de dados fornece estatísticas detalhadas sobre o desempenho e tamanho do banco de dados SQLite, incluindo número de tabelas, índices, tamanho total e tempo médio de consultas. Ferramentas de otimização permitem executar operações de manutenção como VACUUM e ANALYZE para melhorar a performance.

O monitoramento de requisições HTTP mostra estatísticas sobre o uso da aplicação web, incluindo número de requisições por minuto, tempo médio de resposta, códigos de status HTTP e endpoints mais acessados. Estas informações são valiosas para identificar gargalos de performance e padrões de uso.

### Gerenciamento de Backup

O sistema de backup do ERP ROMA garante a segurança dos dados da Roma Confecções contra perdas acidentais, falhas de hardware ou outros incidentes. Para gerenciar backups, clique em "Administração" > "Backup" na barra lateral.

A tela principal de gerenciamento de backup lista todos os backups disponíveis, incluindo data e hora, tipo (diário, semanal ou manual), tamanho, status (concluído, em andamento ou falha) e localização (local ou nuvem). Filtros permitem visualizar backups por período, tipo ou status.

Para criar um backup manual, clique no botão "Novo Backup". Um formulário será exibido onde você pode selecionar quais componentes incluir no backup (banco de dados, arquivos de configuração, logs, arquivos de upload) e definir uma descrição opcional para facilitar a identificação futura.

O processo de backup é executado em segundo plano, permitindo que você continue usando o sistema normalmente. Uma notificação será exibida quando o backup for concluído, informando o status e o tamanho do arquivo gerado.

Para restaurar um backup, selecione-o na lista e clique no botão "Restaurar". Um aviso será exibido alertando que a restauração substituirá todos os dados atuais pelos dados do backup selecionado. Esta operação deve ser realizada com extremo cuidado e preferencialmente em horários de baixo uso do sistema.

Backups podem ser baixados para armazenamento externo clicando no botão "Download" ao lado do backup desejado. Esta é uma prática recomendada para backups críticos, garantindo redundância adicional em caso de falha no servidor principal.

Para usuários Mac, a sincronização com iCloud pode ser configurada para armazenar automaticamente cópias dos backups na nuvem. Esta funcionalidade proporciona uma camada adicional de segurança, protegendo os dados contra falhas locais ou desastres físicos.

---

## Backup e Segurança

O ERP ROMA implementa um conjunto abrangente de medidas de backup e segurança para proteger os dados valiosos da Roma Confecções contra perdas, acessos não autorizados e outros riscos. Esta seção detalha as funcionalidades disponíveis e as melhores práticas para garantir a integridade e confidencialidade das informações.

### Sistema de Backup Automático

O sistema de backup automático do ERP ROMA foi projetado para funcionar sem intervenção manual, garantindo que cópias de segurança sejam criadas regularmente conforme a programação definida nas configurações.

Os backups diários são realizados automaticamente às 2:00 AM, quando o sistema tipicamente não está em uso. Estes backups incluem o banco de dados completo e são mantidos por 7 dias antes de serem substituídos. Backups diários são ideais para recuperação rápida em caso de problemas recentes.

Os backups semanais são realizados aos domingos e incluem o banco de dados, arquivos de configuração e logs. Estes backups são mantidos por 4 semanas e são mais abrangentes que os diários, permitindo recuperação de dados mais antigos se necessário.

Os backups mensais são realizados no primeiro dia de cada mês e incluem todos os componentes do sistema. Estes backups são mantidos por 12 meses e servem como arquivos históricos de longo prazo, úteis para auditoria e análises retrospectivas.

Todos os backups são compactados em formato ZIP com verificação de integridade, economizando espaço em disco e garantindo que os dados possam ser recuperados corretamente quando necessário. O sistema verifica automaticamente a integridade de cada backup após sua criação.

O sistema mantém um registro detalhado de todos os backups realizados, incluindo data, hora, tipo, tamanho, conteúdo e status. Este registro pode ser consultado na tela de gerenciamento de backup e é valioso para auditoria e verificação da política de backup.

### Sincronização com iCloud

Para usuários Mac, o ERP ROMA oferece integração com o iCloud para armazenamento redundante de backups na nuvem. Esta funcionalidade proporciona uma camada adicional de proteção, garantindo que os dados estejam seguros mesmo em caso de falha completa do servidor local.

Para configurar a sincronização com iCloud, acesse "Administração" > "Configurações" > "Backup" e ative a opção "Sincronizar com iCloud". Você precisará informar o diretório do iCloud em seu sistema e selecionar quais tipos de backup (diário, semanal, mensal) devem ser sincronizados.

A sincronização ocorre automaticamente após a conclusão de cada backup, transferindo o arquivo compactado para o diretório especificado do iCloud. O sistema verifica se a transferência foi bem-sucedida e registra o resultado no log de backups.

É importante verificar regularmente se a sincronização está funcionando corretamente e se há espaço suficiente na conta do iCloud para armazenar os backups. O sistema enviará alertas se detectar problemas na sincronização ou se o espaço estiver ficando limitado.

### Segurança de Acesso

O ERP ROMA implementa múltiplas camadas de segurança para proteger o acesso ao sistema e garantir que apenas usuários autorizados possam visualizar e manipular os dados da Roma Confecções.

O sistema de autenticação exige credenciais únicas (e-mail e senha) para cada usuário. As senhas são armazenadas de forma segura utilizando algoritmos de hash modernos (bcrypt), garantindo que mesmo em caso de acesso não autorizado ao banco de dados, as senhas originais não possam ser recuperadas.

A política de senhas fortes exige que as senhas tenham pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e símbolos especiais. Esta política pode ser ajustada nas configurações de segurança conforme as necessidades específicas da empresa.

O sistema implementa proteção contra ataques de força bruta, bloqueando temporariamente contas após múltiplas tentativas de login malsucedidas. O número de tentativas permitidas e a duração do bloqueio são configuráveis nas configurações de segurança.

Sessões inativas são automaticamente encerradas após um período configurável de inatividade (padrão de 30 minutos), exigindo nova autenticação para continuar usando o sistema. Esta medida protege contra acessos não autorizados em computadores deixados desbloqueados.

O controle de acesso baseado em perfis garante que cada usuário tenha acesso apenas às funcionalidades e dados necessários para sua função. Os três perfis padrão (Administrador, Gestor e Visualizador) podem ser complementados com permissões específicas para casos especiais.

### Logs de Auditoria

O sistema de logs de auditoria registra detalhadamente todas as ações significativas realizadas no ERP ROMA, criando um rastro completo de atividades para fins de segurança, conformidade e diagnóstico.

Cada log inclui informações como data e hora da ação, usuário responsável, endereço IP de origem, módulo afetado, tipo de ação (criação, leitura, atualização, exclusão) e detalhes específicos da operação. Esta granularidade permite reconstruir precisamente a sequência de eventos quando necessário.

Os logs de auditoria são especialmente detalhados para operações sensíveis como alterações em dados financeiros, emissão de notas fiscais, modificações de cadastros críticos e alterações de configurações do sistema. Nestas operações, o sistema registra tanto os valores antigos quanto os novos.

O acesso aos logs de auditoria é restrito a usuários com perfil de Administrador, garantindo que informações potencialmente sensíveis não sejam expostas a usuários sem necessidade de conhecê-las. Esta restrição segue o princípio de privilégio mínimo necessário.

Os logs são protegidos contra adulteração, sendo armazenados em formato que permite detectar modificações não autorizadas. Esta característica é importante para garantir a validade dos logs em caso de investigações de segurança ou auditorias formais.

### Proteção de Dados

Além da segurança de acesso, o ERP ROMA implementa medidas adicionais para proteger a integridade e confidencialidade dos dados armazenados e transmitidos pelo sistema.

Todas as comunicações entre o navegador do usuário e o servidor são criptografadas usando HTTPS/TLS, impedindo a interceptação de dados sensíveis durante a transmissão. O certificado SSL é renovado automaticamente para evitar períodos de vulnerabilidade.

O sistema implementa proteção contra ataques comuns como CSRF (Cross-Site Request Forgery), XSS (Cross-Site Scripting) e injeção de SQL. Estas proteções são fundamentais para prevenir comprometimento do sistema através de vetores de ataque conhecidos.

Validações rigorosas são aplicadas a todos os dados de entrada, tanto na interface de usuário quanto na API, garantindo que apenas dados válidos e seguros sejam aceitos e processados pelo sistema. Esta prática previne muitos tipos de ataques e erros de dados.

O acesso ao banco de dados é controlado por um sistema de abstração (ORM) que implementa práticas seguras de consulta e manipulação de dados, reduzindo significativamente o risco de vulnerabilidades de injeção de SQL ou acesso não autorizado aos dados.

Informações sensíveis como senhas, chaves de API e certificados digitais são armazenadas de forma segura, utilizando técnicas apropriadas de criptografia ou hash conforme o tipo de dado. Estas informações nunca são expostas em logs, interfaces de usuário ou relatórios.

---

## Solução de Problemas

Esta seção fornece orientações para identificar e resolver problemas comuns que podem ocorrer durante o uso do ERP ROMA. Seguindo estas instruções, muitas situações podem ser resolvidas rapidamente sem necessidade de suporte técnico especializado.

### Problemas de Login

**Problema**: Não consigo fazer login no sistema.

**Possíveis causas e soluções**:

1. **Credenciais incorretas**: Verifique se o e-mail e senha estão corretos, respeitando maiúsculas e minúsculas. Se não tiver certeza da senha, utilize a opção "Esqueci minha senha" na tela de login ou contate um administrador.

2. **Conta bloqueada**: Após múltiplas tentativas de login malsucedidas, a conta pode ser temporariamente bloqueada por segurança. Aguarde o período de bloqueio (geralmente 15 minutos) ou contate um administrador para desbloquear a conta.

3. **Conta desativada**: Sua conta pode ter sido desativada por um administrador. Contate o administrador do sistema para verificar o status da sua conta e solicitar reativação se necessário.

4. **Problemas de conexão**: Verifique se sua conexão com a internet está funcionando corretamente. Tente acessar outros sites para confirmar que o problema não é com sua conexão.

5. **Navegador incompatível ou desatualizado**: O ERP ROMA funciona melhor em navegadores modernos e atualizados. Tente utilizar Google Chrome, Mozilla Firefox, Safari ou Microsoft Edge em suas versões mais recentes.

6. **Cache do navegador**: Problemas de cache podem causar comportamentos inesperados. Tente limpar o cache do seu navegador ou acessar em uma janela anônima/privativa.

### Problemas de Performance

**Problema**: O sistema está lento ou não responde.

**Possíveis causas e soluções**:

1. **Conexão de internet lenta**: Verifique a velocidade da sua conexão. O ERP ROMA requer uma conexão estável para funcionar adequadamente. Teste sua velocidade em sites como speedtest.net e contate seu provedor se necessário.

2. **Muitas abas ou aplicativos abertos**: Feche abas e aplicativos desnecessários para liberar recursos do seu computador. Navegadores com muitas abas abertas podem consumir muita memória e afetar a performance.

3. **Hardware limitado**: Verifique se seu computador atende aos requisitos mínimos recomendados. O ERP ROMA funciona melhor em computadores com pelo menos 4GB de RAM e processadores modernos.

4. **Banco de dados grande**: Sistemas com muitos dados históricos podem ficar mais lentos com o tempo. Administradores podem executar otimizações de banco de dados através do módulo de administração.

5. **Picos de uso**: Em horários de pico, quando muitos usuários estão acessando simultaneamente, o sistema pode ficar mais lento. Se possível, realize operações intensivas em horários de menor uso.

6. **Problemas no servidor**: Em raros casos, o servidor pode estar sobrecarregado ou enfrentando problemas técnicos. Contate o administrador do sistema para verificar o status do servidor.

### Problemas com Relatórios

**Problema**: Relatórios não são gerados ou apresentam dados incorretos.

**Possíveis causas e soluções**:

1. **Filtros incorretos**: Verifique se os filtros aplicados ao relatório estão corretos. Filtros muito restritivos podem resultar em relatórios vazios ou com poucos dados.

2. **Dados inconsistentes**: Verifique se os dados base estão corretos e completos. Relatórios dependem da qualidade dos dados inseridos no sistema.

3. **Permissões insuficientes**: Alguns relatórios podem requerer permissões específicas. Verifique se seu perfil de usuário tem acesso aos dados necessários para o relatório.

4. **Cache do navegador**: Relatórios antigos podem ficar armazenados em cache. Tente limpar o cache do navegador ou usar a opção "Atualizar" no relatório.

5. **Timeout do servidor**: Relatórios muito complexos ou com grandes volumes de dados podem exceder o tempo limite do servidor. Tente reduzir o escopo do relatório ou executá-lo em horários de menor uso.

6. **Erros de cálculo**: Em raros casos, pode haver erros nas fórmulas ou lógica dos relatórios. Reporte o problema detalhadamente ao suporte técnico para investigação.

### Problemas com Notas Fiscais

**Problema**: Não consigo emitir notas fiscais ou recebo erros na emissão.

**Possíveis causas e soluções**:

1. **Configuração do Bling**: Verifique se a integração com o Bling está corretamente configurada em "Financeiro" > "Configurações" > "Integração Bling". A API Key deve estar válida e o teste de conexão deve ser bem-sucedido.

2. **Dados incompletos do cliente**: Para emissão de notas fiscais, todos os dados fiscais do cliente devem estar completos e válidos. Verifique se CNPJ, inscrição estadual e endereço estão corretamente preenchidos.

3. **Dados incompletos dos produtos**: Produtos devem ter NCM, origem e outras informações fiscais corretamente preenchidas. Verifique o cadastro dos produtos incluídos na nota fiscal.

4. **Problemas na API do Bling**: O serviço do Bling pode estar temporariamente indisponível ou com problemas. Verifique o status do serviço no site do Bling ou aguarde alguns minutos antes de tentar novamente.

5. **Certificado digital expirado**: Se você utiliza certificado digital para assinatura, verifique se ele está válido e corretamente instalado.

6. **Erros de validação**: A nota fiscal pode conter dados que não passam nas validações da SEFAZ. Leia atentamente a mensagem de erro retornada e corrija as informações conforme necessário.

### Problemas de Estoque

**Problema**: Divergências entre estoque físico e estoque no sistema.

**Possíveis causas e soluções**:

1. **Produções não finalizadas**: Verifique se todas as produções foram corretamente finalizadas no sistema. Produções em andamento não afetam o estoque até serem finalizadas.

2. **Movimentações manuais não registradas**: Certifique-se de que todas as movimentações manuais de estoque (como ajustes, perdas ou transferências) foram devidamente registradas no sistema.

3. **Composição de produtos incorreta**: Verifique se a composição de materiais dos produtos está corretamente configurada. Composições incorretas podem levar a consumos inadequados de materiais durante a produção.

4. **Estoque inicial incorreto**: Se o sistema foi recentemente implementado, verifique se o estoque inicial foi corretamente cadastrado para todos os produtos e materiais.

5. **Operações simultâneas**: Em ambientes com muitos usuários, operações simultâneas podem ocasionalmente causar inconsistências. Realize um inventário físico e ajuste o estoque no sistema conforme necessário.

6. **Bugs ou erros de sistema**: Em raros casos, pode haver problemas no próprio sistema. Documente detalhadamente a divergência e reporte ao suporte técnico para investigação.

### Contato com Suporte

Se você encontrar problemas que não consegue resolver seguindo as orientações acima, entre em contato com o suporte técnico do ERP ROMA. Para agilizar o atendimento, tenha em mãos as seguintes informações:

1. **Descrição detalhada do problema**: Explique exatamente o que está acontecendo, incluindo mensagens de erro completas, se houver.

2. **Passos para reproduzir**: Descreva passo a passo como o problema ocorre, para que o suporte possa tentar reproduzi-lo.

3. **Capturas de tela**: Sempre que possível, inclua capturas de tela mostrando o problema ou mensagens de erro.

4. **Informações do ambiente**: Navegador e versão, sistema operacional, e se o problema ocorre em diferentes dispositivos ou apenas em um específico.

5. **Logs relevantes**: Administradores podem acessar logs do sistema em "Administração" > "Logs" que podem conter informações valiosas para diagnóstico.

6. **Urgência e impacto**: Indique o nível de urgência do problema e seu impacto nas operações da empresa, para que o suporte possa priorizar adequadamente.

O suporte técnico está disponível por e-mail em suporte@romaconfeccoes.com.br ou por telefone em (11) 1234-5678, de segunda a sexta-feira, das 8h às 18h.

---

## Glossário

Este glossário define os principais termos e conceitos utilizados no ERP ROMA, facilitando a compreensão da terminologia específica do sistema e do negócio da Roma Confecções.

**API (Interface de Programação de Aplicações)**: Conjunto de rotinas e padrões que permitem a comunicação entre diferentes sistemas. No ERP ROMA, a API é utilizada principalmente para integração com o Bling.

**Backup**: Cópia de segurança dos dados do sistema, realizada periodicamente para prevenir perda de informações em caso de falhas ou acidentes.

**Bling**: Sistema externo utilizado para emissão oficial de notas fiscais, integrado ao ERP ROMA através de API.

**CNPJ (Cadastro Nacional da Pessoa Jurídica)**: Número de identificação fiscal de empresas brasileiras, utilizado no cadastro de clientes e fornecedores pessoas jurídicas.

**CPF (Cadastro de Pessoas Físicas)**: Número de identificação fiscal de pessoas físicas brasileiras, utilizado no cadastro de clientes pessoas físicas.

**Dashboard**: Painel visual que apresenta indicadores-chave e métricas importantes do negócio de forma consolidada e de fácil compreensão.

**ERP (Enterprise Resource Planning)**: Sistema de gestão empresarial que integra todos os dados e processos de uma organização em um único sistema.

**Estoque Mínimo**: Quantidade mínima de um produto ou material que deve ser mantida em estoque para evitar rupturas. Quando o estoque atual fica abaixo deste valor, o sistema gera alertas.

**Fluxo de Caixa**: Registro de todas as entradas e saídas financeiras da empresa, permitindo controle e análise da situação financeira.

**Inscrição Estadual**: Número de registro de um contribuinte do ICMS (Imposto sobre Circulação de Mercadorias e Serviços) junto à Secretaria da Fazenda Estadual.

**KPI (Key Performance Indicator)**: Indicador-chave de desempenho, métrica utilizada para avaliar o sucesso em relação a objetivos específicos.

**Log**: Registro detalhado de eventos e ações ocorridos no sistema, utilizado para auditoria, diagnóstico e segurança.

**Movimentação**: Qualquer alteração no estoque de produtos ou materiais, como entradas por produção, saídas por venda ou ajustes manuais.

**NCM (Nomenclatura Comum do Mercosul)**: Código de classificação fiscal de produtos, obrigatório para emissão de notas fiscais. Para produtos têxteis da Roma Confecções, o código típico é 62092000.

**Nota Fiscal**: Documento fiscal que registra e legaliza a transferência de propriedade de um produto ou serviço. No ERP ROMA, as notas fiscais são emitidas através da integração com o Bling.

**Perfil de Usuário**: Conjunto de permissões e acessos atribuídos a um usuário do sistema, determinando quais funcionalidades ele pode utilizar. Os perfis padrão são Administrador, Gestor e Visualizador.

**Produção**: Registro do processo de fabricação de produtos, incluindo itens produzidos, quantidades, cliente e consumo de materiais.

**SQLite**: Sistema de gerenciamento de banco de dados relacional utilizado pelo ERP ROMA para armazenamento de dados.

**Status**: Estado atual de um registro no sistema, como "Em Andamento", "Finalizado" ou "Cancelado" para produções, ou "Pendente", "Confirmada" ou "Cancelada" para movimentações financeiras.

**Usuário**: Pessoa que possui acesso ao sistema ERP ROMA, com credenciais (e-mail e senha) e perfil específicos que determinam suas permissões.

---

## Índice Remissivo

- **A**
  - Administração, 35
  - Alertas, 12, 18, 24
  - Análises Avançadas, 34
  - API, 29, 41
  - Autenticação, 8, 36

- **B**
  - Backup, 35, 36-38
  - Bling, 29-30, 40

- **C**
  - Categorias Financeiras, 27
  - Clientes, 15-17
  - Composição de Materiais, 20-21
  - Configurações, 35-36
  - CSRF, 37

- **D**
  - Dashboard, 31-34
  - Dados Fiscais, 16, 20

- **E**
  - Estoque, 21, 24, 40
  - Exportação, 33

- **F**
  - Filtros, 16, 26, 32
  - Financeiro, 26-30
  - Fluxo de Caixa, 26-27
  - Fornecedores, 17

- **G**
  - Gráficos, 27, 32, 33
  - Glossário, 41-42

- **I**
  - iCloud, 37
  - Indicadores, 31

- **L**
  - Login, 8, 39
  - Logs, 36, 37

- **M**
  - Materiais, 20-21
  - Monitoramento, 36
  - Movimentações, 21, 26-27

- **N**
  - Navegação, 8
  - NCM, 20, 29
  - Notas Fiscais, 29-30, 40

- **P**
  - Perfis de Usuário, 10, 41
  - Produção, 22-25
  - Produtos, 18-21

- **R**
  - Relatórios, 25, 28, 32-34, 39
  - Restauração, 37

- **S**
  - Segurança, 36-37
  - Senha, 8, 10, 37
  - Solução de Problemas, 39-41
  - Suporte, 41

- **U**
  - Usuários, 10-12

---

*Manual do Usuário - ERP ROMA*  
*Versão 1.0 - Dezembro 2024*  
*© 2024 Roma Confecções - Todos os direitos reservados*

