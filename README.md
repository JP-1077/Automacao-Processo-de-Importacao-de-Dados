# Automacao Processo de Importacao de Dados

## Objetivo 🎯

Automatizar a extração e exportação de dados da tabela de um banco de dados SQL Server, segmentando os dados por fornecedor e salvando as informações em arquivos e diretórios específicos.

## Tecnologias e Ferramentas 🛠

* Linguagem: Python
* Bibliotecas:
    * pandas (manipulação de dados)
    * pyodbc (conexão com SQL Server)
    * os, datetime, warnings
* Banco de Dados: SQL Server

## System Design ✍🏼

![Pipeline](Pipeline(5).png)

1. Definição de parâmetros: Captura da data de referência (D-1)
2. Conexão com banco de dados: SQL Server via pyodbc
3. Extração de dados: Filtro por ano e mês
4. Segmentação: Separação dos dados por fornecedor
5. Exportação: Geração de dois arquivos CSV (um para cada fornecedor)
6. Log de execução: Registro em TB_PROCS_LOG

## Detalhes Técnicos ⚙

### Fonte de Dados

* Banco de Dados: SQL Server
  
### Transformações

* Segmentação por Fornecedor

### Base Final 

* Criação de dois arquivos CSV com a segmentações dos dois fornecedores

## Monitoramento ✅

* Nome do Processo: PY_EXPORT_BASE_CONTRATO_SHORT_CALL
  
* Horario de Execução: 08:00
