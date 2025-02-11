import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import plotly.express as px
import numpy as np
from datetime import timedelta
from modulo.lista_filtros import lista_filtros


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR  = os.path.join(BASE_DIR, 'src', 'sql')
DB_PATH  = os.path.join(DATA_DIR, 'data.db')

@st.cache_resource
def load_db():
    engine = create_engine(f'sqlite:///{DB_PATH}')
    return engine.connect()

@st.cache_data
def load_data_empresas():
    conn = load_db()
    
    with open(os.path.join(SQL_DIR, 'load_data_empresas.sql'), 'r', encoding= 'utf-8') as f:
        query = f.read()
    
    data = pd.read_sql_query(query, con = conn)
    return data

@st.cache_data
def load_data_socios():
    conn = load_db()
    
    with open(os.path.join(SQL_DIR, 'socios.sql'), 'r', encoding= 'utf-8') as f:
        query = f.read()
    
    data = pd.read_sql_query(query, con = conn)
    return data

@st.cache_data
def load_data_cpf():
    conn = load_db()
    
    with open(os.path.join(SQL_DIR, 'cpf.sql'), 'r', encoding= 'utf-8') as f:
        query = f.read()
    
    data = pd.read_sql_query(query, con = conn)
    return data

if __name__ == "__main__":
    st.title("Ferramenta para auxiliar na criação estratégias de Vendas em Seguros, Previdência e Planos de Saúde")
    st.write("Criado por: Gabriel Reiss de Castro MIBA 4120 https://www.linkedin.com/in/gabrielreissdecastro/")
    st.write("Os dados são todos públicos e foram obtidos com a base dos corretores da SUSEP, com demais cruzamento em outras bases de dados para consolidar os dados, como a base dos CNPJ da Receita Federal e informações geográficas do IBGE")
    
    #Carrega Conexão
    conn = load_db()
    
    #Carrega dados
    df = load_data_empresas()
    df["SUSEP"] = df["SUSEP"].astype("int").astype("str")
        
    #Filtros
    st.sidebar.title("Filtros")

    danos = st.sidebar.checkbox("Seguros de Danos", value=False)
    danos = int(danos)
    
    seg_pessoas = st.sidebar.checkbox("Seguro de Pessoas", value=False)
    seg_pessoas = int(seg_pessoas)
    
    capitalizacao = st.sidebar.checkbox("Planos de Capitalização", value=False)
    capitalizacao = int(capitalizacao)
    
    prev = st.sidebar.checkbox("Planos de Previdência Complementar", value=False)
    prev = int(prev)    
    
    micro = st.sidebar.checkbox("Microsseguros", value=False)
    micro = int(micro)
    
    #Aplica filtros dos checkboxes
    if danos:
        df = df.query(f"`Seguros de Danos` == {danos}")
    if seg_pessoas:
        df = df.query(f"`Seguros de Pessoas` == {seg_pessoas}")
    if capitalizacao:
        df = df.query(f"`Planos de Capitalização` == {capitalizacao}")
    if prev:
        df = df.query(f"`Planos de Previdência Complementar` == {prev}")
    if micro:
        df = df.query(f"`Microsseguros` == {micro}")                

    #Filtro da UF
    default_uf = lista_filtros(SQL_DIR, conn, 'uf')
    default_uf.insert(0, "Todos")
    if "uf" not in st.session_state:
        st.session_state.uf = "Todos"
    
    default_cidade = lista_filtros(SQL_DIR, conn, 'cidade')
    default_cidade.insert(0, "Todos")
    if "cidade" not in st.session_state:
        st.session_state.cidade = "Todos"
        
    default_bairro = lista_filtros(SQL_DIR, conn, 'bairro')
    default_bairro.insert(0, "Todos")
    if "bairro" not in st.session_state:
        st.session_state.bairro = "Todos"

    #botao do reset
    if st.sidebar.button('Resetar Filtros de Localidade'):
        st.session_state.uf = "Todos"
        st.session_state.cidade = "Todos"
        st.session_state.bairro = "Todos"    
        
    #A parte que cria as seleções
    options_uf = st.sidebar.multiselect("UF", default_uf, default=st.session_state.uf)
    options_cidade = st.sidebar.multiselect("Cidade", default_cidade, default=st.session_state.cidade)
    options_bairro = st.sidebar.multiselect("Bairro", default_bairro, default=st.session_state.bairro)
    
    
    #Isso aqui é para não bugar a seleção
    if options_uf:
        st.session_state.uf = options_uf
    if options_cidade:
        st.session_state.cidade = options_cidade
    if options_bairro:
        st.session_state.bairro = options_bairro
    
    #Filtro das seleções, enfim
    if "Todos" not in options_uf:
        df = df[df["UF"].isin(options_uf)]
    if "Todos" not in options_cidade:
        df = df[df["cidade"].isin(options_cidade)]
    if "Todos" not in options_bairro:
        df = df[df["BAIRRO"].isin(options_bairro)]

    #input de codigo susep
    susep = st.text_input("Digite parte do código do registro da SUSEP (Opcional):")
    if susep:
        df = df[df["SUSEP"].str.contains(susep, na=False, case=False)]

    #input de codigo cnpj
    cnpj = st.text_input("Digite parte do código do CNPJ sem pontos e barras (Opcional):")
    if cnpj:
        df["CNPJ_filtro"] = df["CNPJ"].str.replace(".","").str.replace("/","").str.replace("-","")
        df = df[df["CNPJ_filtro"].str.contains(cnpj, na=False, case=False)]
    
    #Limpa base dos filtros
    colunas = ["NOME", "SUSEP", "CNPJ", "LOGRADOURO", "NUMERO", "BAIRRO","cidade", "UF", "DDD1", "TELEFONE1", "DDD2", "TELEFONE2", "CORREIOELETRONICO"]
    df_vis = df[colunas]
    if df_vis.empty:
        st.write("Sem dados com esses filtros")
    else:    
        st.subheader("CNPJ's Encontrados")
        st.write(f"Foram encontratos {df_vis.shape[0]} CNPJ com esses filtros.")
        csv = df_vis.to_csv(index=False, encoding='utf-8-sig', sep=';')
        st.download_button("Download dos Dados Filtrados | encoding = utf-8-sig | separador de coluna = ;", data = csv, file_name = "data.csv", mime = "text/csv")
        del(csv)
        
        guias_titulo = ["Corretoras","Sócios"]
        guia_empresas, guia_socios = st.tabs(guias_titulo)
        
        with guia_empresas:        
            st.dataframe(df_vis)
        with guia_socios:
            df_socios = load_data_socios()
            df_socios = df_socios[df_socios["CNPJBASICO"].isin(df["CNPJBASICO"])]
            st.dataframe(df_socios[["CORRETORA", "SOCIO", "CARGO"]])
        
    #Agora a parte boa, o mapa
    df["CAPITAL"] = df["CAPITAL"].astype("str").replace("None", 1).str.replace(",",".").astype("float").fillna(1)
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        size=df["CAPITAL"].abs(),
        hover_name="NOME",
        hover_data=["DDD1", "TELEFONE1", "CORREIOELETRONICO"],
        zoom=3,
        size_max=50,
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        title="Saldo de Movimentação por Estado",
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    st.plotly_chart(fig)
    
    st.subheader("Corretores pessoas físicas encontradas")
    st.write("Por questões de LGPD, só serão informados o nome e o código da susep, até o presente momento, não foi possível filtrar por localização.")
    
    cpf = load_data_cpf()
    
    st.write(f"Foram encontratos {cpf.shape[0]} Corretores pessoas físicas.")
    csv = cpf.to_csv(index=False, encoding='utf-8-sig', sep=';')
    st.download_button("Download dos Dados dos Corretores PF | encoding = utf-8-sig | separador de coluna = ;", data = csv, file_name = "data.csv", mime = "text/csv")
    del(csv)
    cpf["COD_SUSEP"] = cpf["COD_SUSEP"].astype("int").astype("str")
    st.dataframe(cpf)
    
    st.markdown("""
                # Minhas considerações sobre as questões de estratégias comerciais com corretores:
                
                Sabemos que os custos de aquisição de novos clientes podem a ser até 21 vezes mais caro que a renovação de clientes. Podemos fazer um paralelo com o mercado de seguros de Portugal, o estudo de DA SILVA (2018) mostra que o mercado está competitivo e as seguradoras estão focadas em entender e atender às necessidades dos clientes. Isso implica que reter os clientes existentes (renovação) é crucial, pois a competição por novos clientes é acirrada e, portanto, mais custosa.

                Seguro é um produto elástico, conforme os conceitos de microeconomia, os clientes são sensíveis ao preço. Isso significa que atrair novos clientes exigirá estratégias de preços competitivas e, potencialmente, descontos e promoções dispendiosas. Manter o relacionamento com os clientes existentes, evitando ações que os afastem (como aumentos de preços inesperados), é uma forma mais econômica de garantir receita.
                
                O agente econômico que está diretamente em contato com o cliente é o corretor, então fazer ele se tornar parte do processo e atender a o cliente quando ele mais precisa, que é o momento que acontece o sinistro, se torna crucial. Como engajar o corretor a prestar um bom serviço de apoio para não perder aquele cliente? (CENSURADO pois tenho contas a pagar)

                GUIDI (2018), ressalta que entender o cliente e fazer segmentação aumentar a eficiência na aquisição e conversão de clientes. O estudo foi focado em crédito pessoal, porém podemos também aproveitar a ideia de segmentação e as ferramentas que a ciência de dados, como clusterização e random florest, para diferenciar bons e maus riscos.

                Em Silva (2024), foca em análisar os indicadores estratégicos de Custo de Aquisição do Cliente (CAC) e Lifetime Value (LTV), essenciais para avaliar a eficácia dos investimentos em marketing e vendas. Esses indicadores permitem à empresa compreender o valor que cada cliente agrega ao longo do tempo, bem como os custos associados à sua aquisição, possibilitando uma gestão mais precisa e orientada por dados. O CAC é, por definição, o custo para adquirir. O LTV é o valor que esse cliente gera ao longo do tempo. O fato de a empresa estar focando em ambos os indicadores mostra que ela está tentando equilibrar o quanto gasta para conseguir um cliente com o quanto ela vai ganhar com esse cliente no futuro. Se a renovação fosse mais cara, a empresa se preocuparia menos com o LTV. Portanto esse artigo mostra que é mais fácil e mais rentável manter um cliente do que adquirir um novo, ajudar a reduzir o churn e reter clientes.

                Portanto é necessário engajar os corretores a participarem da captação de perfis de bons riscos incentiv...(TENHO UMA IDEIA mas ficará censurada, pois preciso pagar as minhas contas também).

                #### Referências
                DA SILVA, Carolina Ferreira Duarte. Modelação da elasticidade do preço na renovação Automóvel. 2018. Dissertação de Mestrado. Universidade de Lisboa (Portugal).

                GUIDI, Carlos Eduardo Guglielme. Análise de segmentação aplicada à aquisição de clientes no setor de crédito pessoal. 2018. Tese de Doutorado.

                SILVA, Larissa Beatriz Santos. Implementação e Análise de Indicadores Estratégicos de Custo de Aquisição do Cliente (CAC) e LifeTime Value (LTV) Em Uma Empresa de ERP. 2024. 19 f. Trabalho de Conclusão de Curso (Graduação em Gestão da Informação) – Universidade Federal de Uberlândia, Uberlândia, 2024.             
                """
    )