import os
import pandas as pd
import sqlalchemy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

str_db = f"sqlite:///{os.path.join(DATA_DIR, 'banco.db')}"
engine = sqlalchemy.create_engine(str_db)
conn = engine.connect()

str_db2 = f"sqlite:///{os.path.join(DATA_DIR, 'data.db')}"
engine2 = sqlalchemy.create_engine(str_db2)
conn2 = engine2.connect()

#
with open(os.path.join(BASE_DIR,'src','sql', 'tabelao.sql'), encoding='utf-8') as f:
    query = f.read()
df = pd.read_sql_query(query, conn)
df.to_sql("empresas", conn2,index=None, if_exists='replace')
df.to_csv(os.path.join(DATA_DIR,'empresas.csv'),index=None,sep=';')

#
with open(os.path.join(BASE_DIR,'src','sql', 'socios.sql'), encoding='utf-8') as f:
    query = f.read()
df = pd.read_sql_query(query, conn)
df.to_sql("socios", conn2,index=None, if_exists='replace')
df.to_csv(os.path.join(DATA_DIR,'socios.csv'),index=None,sep=';')

#
with open(os.path.join(BASE_DIR,'src','sql', 'cpf.sql'), encoding='utf-8') as f:
    query = f.read()
df = pd.read_sql_query(query, conn)
df.to_sql("cpf", conn2,index=None, if_exists='replace')
df.to_csv(os.path.join(DATA_DIR,'cpf.csv'),index=None,sep=';')