#%%
import os
import pandas as pd
import sqlalchemy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

str_db = f"sqlite:///{os.path.join(DATA_DIR, 'banco.db')}"
engine = sqlalchemy.create_engine(str_db)
conn = engine.connect()

with open(os.path.join(BASE_DIR,'src','sql', 'tabelao.sql')) as f:
    query = f.read()

df = pd.read_sql_query(query, conn)
df.to_csv(os.path.join(DATA_DIR, 'data.csv'))

# %%
