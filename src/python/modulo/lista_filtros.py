import os
import pandas as pd

#Filtro lateral por região do país, UF, período da competência, raçacor, sexo, região

def lista_filtros(SQL_DIR, conn, coluna):
    with open(os.path.join(SQL_DIR, 'filtros', f'{coluna}.sql'), 'r', encoding='utf-8') as f:
        query = f.read()
    data = pd.read_sql_query(query, conn)
    return list(data['coluna'])