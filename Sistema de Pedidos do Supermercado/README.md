# Sistema de Pedidos do Supermercado.

O projeto foi elaborado com um propósito de ter um sistema para ajudar as pessoas nos pedidos dos clientes nos supermercados. Pensando num sentido mais amplo, podemos pensar em qualquer coisa, como entrega de produtos de Mercado, Loja de Roupa, Comida e etc.

O programa foi dividido em 4 scripts: BD_SQL, GOOGLE_SHEETS, CAIXA e GERENTE. E um bloco de notas (.txt) que tem os códigos SQL para: criar um banco de dados, criar tabelas (são 3) e por último inserindo os dados. E agora vou explicar um pouco cada um dos scripts.

## BD_SQL
É um script que existem 4 principais funções: id_produtos, mudando_coluna_colocado, mudando_coluna_processos e main (que tem dois scripts auxiliares: selecionar_colocado e arrumando_lista)

- Referente a função Main e seus auxiliares, são divididos em duas partes. Um lado faz o processamento dos dados do Caixa e outro do Gerente. Pois suas entradas e saídas são diferentes, e precisam ser tratados diferentes;
- Referente a função id_produtos, retorna um dicionário (key = código do produto, value = Nome do produto) existem no mercado;
- Referente as funções mudando_coluna_colocado, mudando_coluna_processos, basicamente atualizam a base de dados.

O script é basicamente comandos python utilizando SQL, para fazer atualizações e seleções das tabalas. E para auxiliar esse armazenamento e requerimento, foi usado o software XAMPP, habilitando o MySql e o Apache.

## GOOGLE_SHEETS
O código foi pego no "https://developers.google.com/sheets/api/quickstart/python" e adaptando no meu contexto. Precisa fazer as etapas 1 e 2, mostrado no link, para baixar as libs e a ativar automaticamente a API do Google Sheets, e com isso vai vir um arquivo JSON e colocar junto (na mesma pasta) com os scripts.

Agora faz um Google Sheet, pega uma parte do URL, (depois do https://docs.google.com/spreadsheets/d/ e antes do /edit#gid=0) e essa parte, vamos chamar de CÓDIGO_PLANILHA. E fazer duas alterações de estéticas, na célula A1 colocar em maiúsculos e negritos (QUAIS SÃO OS CLIENTES QUE JÁ FORAM ATENDIDOS) E na célula D1 colocar em maiúsculos e negritos (QUANTOS CLIENTES FORAM ATENDIDOS).

Agora você tem duas opções, um mais prático e outro não. Esse CÓDIGO_PLANILHA, pode trocar com um já estabelecidos ou rodas o script GERENTE e tem a opção de colocar outra planilha.

## CAIXA
Quando rodar o código, basta seguir as instruções que o script vai mostrar. 

Existe dois tipos de barra de código. Primeiro é o ID do cliente, para saber quem é o cliente que vai ser atendidos e por ultimo o código dos produtos que o cliente pediram, caso coloque CÓDIGO DE PRODUTO que o cliente não pediu vai aparecer a mensagem ERROR.

## GERENTE
Nesse script, basicamente, pega uma lista dos clientes atendidos (que foi requerido no script BD_SQL) e atualizar o Google Sheets com base nessa lista.

PS: Se for a primeira vez que rodar o código, vai precisar aceitar as condições do google para ter acesso no google sheets.
# GAP
Seria interessante um app para alimentar o Banco de Dados, uma tela mais agradável para acessar o Script CAIXA e GERENTE para ficar algo mais agradável.

# LIB para Rodar o Código
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
- prettytable
