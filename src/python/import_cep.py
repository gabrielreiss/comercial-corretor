#%%
import os
import pandas as pd
import sqlalchemy
import requests
import pandas as pd
import sqlite3
from time import sleep

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

str_db = f"sqlite:///{os.path.join(DATA_DIR, 'data.db')}"
engine = sqlalchemy.create_engine(str_db)
conn = engine.connect()

with open(os.path.join(BASE_DIR,'src','sql', 'cep.sql')) as f:
    query = f.read()

df_cnpj = pd.read_sql_query(query, conn)

df_cnpj["CEP"] = df_cnpj["CEP"].astype(str).str.zfill(8)
print(df_cnpj.head())

db_path = os.path.join(DATA_DIR, 'banco.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS localizacao (
        cep TEXT PRIMARY KEY,
        endereco TEXT,
        bairro TEXT,
        cidade TEXT,
        estado TEXT,
        latitude REAL,
        longitude REAL
    )
""")
conn.commit()

def consultar_cep(cep):
    url = f"https://cep.awesomeapi.com.br/json/{cep}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "cep": data.get("cep"),
                "endereco": data.get("address", ""),
                "bairro": data.get("neighborhood", ""),
                "cidade": data.get("city", ""),
                "estado": data.get("state", ""),
                "latitude": float(data.get("lat", 0)),
                "longitude": float(data.get("lng", 0))
            }
        else:
            print(f"Erro ao buscar {cep}: {response.status_code}")
    except Exception as e:
        print(f"Erro na requisição para {cep}: {e}")
    return None

def salvar_no_banco(dados):
    if dados:
        cursor.execute("""
            INSERT OR REPLACE INTO localizacao 
            (cep, endereco, bairro, cidade, estado, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (dados["cep"], dados["endereco"], dados["bairro"], 
              dados["cidade"], dados["estado"], dados["latitude"], dados["longitude"]))
        conn.commit()

for cep in df_cnpj["CEP"]:
    if cep:  # Evita valores nulos
        print(f"Consultando {cep}...")
        dados = consultar_cep(cep)
        if dados:
            salvar_no_banco(dados)
            print(f"Salvo: {dados}")
        sleep(1)

conn.close()
print("Processo concluído!")
