# Sistema de Monitoramento de Produção

O projeto foi elaborado com o propósito de ter um sistema de monitoramento de produção.

O problema em questão que foi orientado nas seguintes premissas. 

-> Uma empresa produz de acordo com ordens de serviço, que passam por 2 estações de trabalho, em sequência fixa;

-> Cada vez que a ordem chega na estação de trabalho, o operador cadastra a chegada no sistema;

-> Cada vez que a ordem sai da estação de trabalho, o operador cadastra a saída no sistema;

O Projeto ainda tem que permitir os seguintes relatórios:

-> Quais ordens foram produzidas;

-> Quais ordens ainda estão em produção;

-> Quais ordens estão sendo produzidas na segunda estação de trabalho;

-> Quanto tempo, em média, uma ordem fica no sistema;

E guardar os dados no banco de dados SQL, e pra auxiliar esse armazenamento foi usado o software XAMPP.


O código cria uma base de dados com algumas colunas e o horário é guardado usando a data estabelecido pelo computador local. O código pode ser adaptando, aumentando colunas, seus critérios e o mais importante, DEPENDENDO DO NEGOCIO.
