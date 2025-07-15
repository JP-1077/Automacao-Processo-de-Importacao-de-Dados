"""
================================================================================
Desenvolvedor: João Pedro Mendes Fonseca

Projeto: Automação no processo de exportação da base de dados short_call
Descrição: Realização da extração de dados de uma tabela do banco de dados SQL
SERVER. Certamente, os dados são separados por dois tipos de fornecedores e
exportados em arquivos CSV distintos para diretórios específicos. Ao final do 
processo é registrado em uma tabela de controle.

Funcionalidades:
    1. Importação de bibliotecas
    2. Conexão com Banco de Dados
    3. Extração e filtragem dos dados
    4. Exportação dos dados para diferentes arquivos
    5. Registro de log


Execução: O processo é executado diariamente atráves de uma VM (Máquina Virtual).
================================================================================
"""

# ==============================================================================
#                       ETAPA 1: Importação de bibliotecas */
# ==============================================================================

import pandas as pd # Manipulção de dados 
import pyodbc # Conexão com banco de dados 
import os # Interação com sistema operacional
import warnings # Controlar e gerenciar avisos referente ao programa sendo executado
from datetime import datetime, timedelta # Trabalhar com datas e horas e diferentes aspectos do tempo.


# ==============================================================================
#              ETAPA 2: Definição de parâmetros e data de referência */
# ==============================================================================

# Captura o horário de início do processo
start_time = datetime.now()

# Define a data referência (D-1)
ontem = datetime.now() - timedelta(days=1)
ano_ref = ontem.year
mes_ref = ontem.month

# Formata o nome do arquivo com base no mês e ano referência
anomes = f"{mes_ref:02d}_{ano_ref}"

# ==============================================================================
#              ETAPA 3: Configuração de ambiente e conexão com banco */
# ==============================================================================

# Definindo a string de conexão com o banco de dados
dados_conexao = ('Driver={SQL Server};'
                 'Server=Snepdb56c01;'
                 'Database=BDS;'
                 'Trusted_Connection=yes;')


# Identifca o usuário logado no sistema
user = os.getlogin()
print (f"Usuário: {user}")

# Estabelece a conexão com o banco
conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()
print('Conectado com sucesso ✅')

# ==============================================================================
#              ETAPA 4: Extração e filtragem dos dados */
# ==============================================================================

# Consulta SQL ocm parâmetros no ano e mês
query = """ SELECT * FROM TB_CONTRATO_SHORT_CALL WHERE ANO = ? AND MES = ? """

# Realiza a leitura da consulta armazenada na variável e utiliza o ano e mes referência capturados na etapa de definição de parâmetros.
df = pd.read_sql(query, conexao, params= (ano_ref, mes_ref))

# Filtra e separa o conjunto de dados em dois fornecedores diferentes (TMKT e CONTAX)
df_TMKT = df[df['FORNECEDOR'] == 'TMKT']
df_CONTAX = df[df['FORNECEDOR'] == 'CONTAX']

# ==============================================================================
#              ETAPA 5: Exportação dos dados para arquivos CSV */
# ==============================================================================

# Define o caminho base para salvar os arquivos
base_path = os.path.join(r"C:\Users\{}\OneDrive - TIM\MIS_TIM\0001 - ATENDIMENTO\0000 - BASES_PARCEIROS\0000 - CONTRATO".format(user))
                

# Salva os arquivos CSV nos diretórios correspondentes (TMKT e CONTAX)
df_TMKT.to_csv(os.path.join(base_path, r'TMKT\0001 - SHORT CALL\SHORT_CALL_TMKT_{}.csv').format(anomes), index=False, encoding='utf-8-sig')

df_CONTAX.to_csv(os.path.join(base_path, r'CONTAX\0001 - SHORT CALL\SHORT_CALL_CONTAX_{}.csv').format(anomes), index=False, encoding='utf-8-sig')

print("Arquivos CSV salvos com sucesso!")

# ==============================================================================
#              ETAPA 6: Registro de Log do Processo */
# ==============================================================================

# Insere Log do processo na tabela de controle 
sql = """
INSERT INTO TB_PROCS_LOG
VALUES (
    'PY_EXPORT_BASE_CONTRATO_SHORT_CALL',         -- processo
    ?,         -- horario start
    CAST(GETDATE() AS DATETIME), -- horario end
    'OK',      -- status
    NULL
)
"""
cursor.execute(sql, start_time)
conexao.commit()
print("log gerado com sucesso!")

# Encerra a conexão com o banco
cursor.close()
conexao.close()