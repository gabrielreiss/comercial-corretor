#%%
import os
import pandas as pd
import sqlalchemy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

str_db = f"sqlite:///{os.path.join(DATA_DIR, 'banco.db')}"
engine = sqlalchemy.create_engine(str_db)
conn = engine.connect()

with open(os.path.join(BASE_DIR,'src','sql', 'cnpj.sql')) as f:
    query = f.read()

df_cnpj = pd.read_sql_query(query, conn)

# %%
import zipfile
import csv
import io

DOWNLOAD_DIR = os.path.join(BASE_DIR, 'download')

def processar_arquivo_zip(zip_path, table_name, colnames):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        arquivos_internos = zip_ref.namelist()
        print(f"Arquivos dentro de {zip_path}: {arquivos_internos}")

        for arquivo_nome in arquivos_internos:
            with zip_ref.open(arquivo_nome) as file:
                with io.TextIOWrapper(file, encoding="latin-1") as text_file:
                    # Usando chunksize para processar 100.000 linhas por vez
                    chunksize = 10**6
                    for chunk in pd.read_csv(text_file, delimiter=';', quotechar='"', 
                                             names=colnames,
                                             chunksize=chunksize):
                        # Filtrando as linhas do chunk com base em uma condição
                        #chunk = chunk[chunk['CNPJBASICO'].map(lambda x: x in set(df_cnpj['CNPJ_LIMPO'].values))]
                        print(chunk.head())  # Imprime as primeiras linhas para depuração

                        # Se o DataFrame não estiver vazio, insere no banco de dados
                        if not chunk.empty:
                            chunk.to_sql(table_name, engine, if_exists='append', index=False)

#%%
table_name = 'Empresas'
colnames = ['CNPJBASICO', 'NOME', 'NATUREZA JURIDICA','RESPONSAVEL', 'CAPITAL', 'PORTE', 'ENTE']
for i in range(10):
    zip_path = os.path.join(DOWNLOAD_DIR, f"{table_name}{i}.zip")
    if os.path.exists(zip_path):
        print(f"Processando {zip_path}...")
        processar_arquivo_zip(zip_path, table_name, colnames)
    else:
        print(f"Arquivo {zip_path} não encontrado.")

# %%
table_name = 'Estabelecimentos'
colnames = [
    'CNPJBASICO',
    'CNPJORDEM',
    'CNPJDV',
    'MATRIZFILIAL',
    'NOME',
    'SITUACAO',
    'DATASITUACAOCADASTRAL',
    'MOTIVOSITUACAOCADASTRAL',
    'NOMEDACIDADENOEXTERIOR',
    'PAIS',
    'DATADEINICIOATIVIDADE',
    'CNAEFISCALPRINCIPAL',
    'CNAEFISCALSECUNDÁRIA',
    'TIPODELOGRADOURO',
    'LOGRADOURO',
    'NUMERO',
    'COMPLEMENTO',
    'BAIRRO',
    'CEP',
    'UF',
    'MUNICIPIO',
    'DDD1',
    'TELEFONE1',
    'DDD2',
    'TELEFONE2',
    'DDDDOFAX',
    'FAX',
    'CORREIOELETRONICO',
    'SITUACAOESPECIAL',
    'DATADASITUACAOESPECIAL'    
]

for i in range(10):
    zip_path = os.path.join(DOWNLOAD_DIR, f"{table_name}{i}.zip")
    if os.path.exists(zip_path):
        print(f"Processando {zip_path}...")
        processar_arquivo_zip(zip_path, table_name, colnames)
    else:
        print(f"Arquivo {zip_path} não encontrado.")


# %%
table_name = ['Paises', 'Qualificacoes', 'Naturezas', 'Municipios', 'Motivos', 'Cnaes']
colnames = [
    'CODIGO',
    'DESCRICAO'
]

for table_name in table_name:
    zip_path = os.path.join(DOWNLOAD_DIR, f"{table_name}.zip")
    if os.path.exists(zip_path):
        print(f"Processando {zip_path}...")
        processar_arquivo_zip(zip_path, table_name, colnames)
    else:
        print(f"Arquivo {zip_path} não encontrado.")

# %%
table_name = 'Simples'
colnames = [
    'CNPJBASICO',
    'OPCAOPELOSIMPLES',
    'DATADEOPCAOPELOSIMPLES',
    'DATADEEXCLUSAODOSIMPLES',
    'OPCAOPELOMEI',
    'DATADEOPCAOPELOMEI',
    'DATADEEXCLUSAODOMEI'
]

zip_path = os.path.join(DOWNLOAD_DIR, f"{table_name}.zip")
if os.path.exists(zip_path):
    print(f"Processando {zip_path}...")
    processar_arquivo_zip(zip_path, table_name, colnames)
else:
    print(f"Arquivo {zip_path} não encontrado.")
    
    
# %%
table_name = 'Socios'
colnames = [
    'CNPJBASICO',
    'IDENTIFICADORDESOCIO',
    'NOMEDOSOCIO',
    'CNPJCPFDOSOCIO',
    'QUALIFICACAODOSOCIO',
    'DATADEENTRADASOCIEDADE',
    'PAIS',
    'REPRESENTANTELEGAL',
    'NOMEDOREPRESENTANTE',
    'QUALIFICACAODOREPRESENTANTELEGAL',
    'FAIXAETARIA'    
]

for i in range(10):
    zip_path = os.path.join(DOWNLOAD_DIR, f"{table_name}{i}.zip")
    if os.path.exists(zip_path):
        print(f"Processando {zip_path}...")
        processar_arquivo_zip(zip_path, table_name, colnames)
    else:
        print(f"Arquivo {zip_path} não encontrado.")
# %%
