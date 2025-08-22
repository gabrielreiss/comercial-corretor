import pandas as pd
import os
import sqlalchemy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

df1 = pd.read_csv(os.path.join(DATA_DIR, "dados_susep copy.csv"))
df2 = pd.read_csv(os.path.join(DATA_DIR, "dados_susep_2025-02-06_18-54-02.csv"), sep = ";")

df3 = pd.concat([df1,df2])
del(df3["Unnamed: 5"],df1,df2)

df3 = df3[~df3['Número de corretor *'].isna()]
df3 = df3.fillna('')

produtos = [
    'Microsseguros',
    'Planos de Capitalização',
    'Seguros de Pessoas',
    'Planos de Previdência Complementar',
    'Seguros de Danos'
]

for categoria in produtos:
    df3[categoria] = df3['Produtos'].apply(lambda x: 1 if categoria in x else 0)

del(df3["Produtos"])


str_db = f"sqlite:///{os.path.join(DATA_DIR, 'banco.db')}"
engine = sqlalchemy.create_engine(str_db)
conn = engine.connect()

df3.to_sql("susep", conn, if_exists='replace')
df3.to_csv(os.path.join(DATA_DIR, "dados_tratados.csv"), sep=";", index=None)


