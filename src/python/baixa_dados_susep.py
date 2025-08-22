import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import logging
from datetime import datetime

# Configuração de logging
log_filename = "webscraper.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Função para formatar a mensagem de log com timestamp
def log_message(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"{timestamp} - {message}"
    if level == "info":
        logging.info(formatted_message)
        print(formatted_message)
    elif level == "warning":
        logging.warning(formatted_message)
        print(formatted_message)
    elif level == "error":
        logging.error(formatted_message)
        print(formatted_message)

# Configuração do driver
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Executa sem abrir o navegador
options.add_argument("--disable-gpu")

# Configurar o ChromeDriverManager
caminho = ChromeDriverManager().install()
service = Service(caminho)
driver = webdriver.Chrome(service=service, options=options)

# Acessa a página
url = "https://www2.susep.gov.br/safe/Corretores/pesquisa"
driver.get(url)
wait = WebDriverWait(driver, 30)

time.sleep(10)

# Abre o filtro
filtro = wait.until(EC.element_to_be_clickable((By.ID, "situacao")))
filtro_select = Select(filtro)
filtro_select.select_by_visible_text("Somente ativos")
log_message("info","Filtro 'Somente ativos' selecionado.")

time.sleep(10)

def apertar_botao():
    try:
        # Localiza a div pai
        div_actions = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "actions.justify-content-start"))
        )

        # Localiza o botão DENTRO da div pai
        botao_pesquisar = div_actions.find_element(By.XPATH, ".//button[@type='submit']")
        botao_pesquisar.click()
        log_message("info","Botão Pesquisar clicado com sucesso (XPath relativo à div).")

    except Exception as e:
        log_message("error",f"Erro ao clicar no botão Pesquisar (XPath relativo à div):{e}")
    
apertar_botao()
time.sleep(1)
apertar_botao()
time.sleep(10)

# Define a função para extrair os dados de uma página e salvar em CSV
def extrair_e_salvar(driver, filename):
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "br-table")))
    tabela = driver.find_element(By.CLASS_NAME, "table")  
    linhas = tabela.find_elements(By.TAG_NAME, "tr")
    
    dados = []

    # Extrai os dados
    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, "td")
        if colunas:
            dados.append([coluna.text for coluna in colunas])
    
    # Salva os dados em CSV (append)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        if csvfile.tell() == 0: #Escreve o cabeçalho apenas se o arquivo estiver vazio
            # Extrai cabeçalho da primeira linha
            try:
                header_row = driver.find_element(By.CSS_SELECTOR, 'thead tr')
                header_cols = header_row.find_elements(By.TAG_NAME, 'th')
                header = [col.text for col in header_cols]
                writer.writerow(header)
                log_message("info","Cabecalho escrito no arquivo CSV.")
            except:
                log_message("error",f"Erro ao extrair cabeçalho, utilizando cabeçalho padrão: {e}")
                writer.writerow(['Nome', 'Número de corretor', 'CPF/CNPJ', 'Situação', 'Produtos', 'Certidão'])

        writer.writerows(dados)
    end_time = time.time()
    total_time = end_time - start_time
    log_message("info", f"Dados da página extraídos e adicionados em '{filename} em {total_time:.2f} segundos'")
    

start_time = time.time()

total_paginas = 5598  # Valor chumbado, caso não encontre o elemento
try:
    total_paginas_elemento = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='br-table']/div[@class='table']/table/tfoot/tr/td[contains(text(),'de')]")))
    texto_paginacao = total_paginas_elemento.text
    if " de " in texto_paginacao:
        total_paginas = int(texto_paginacao.split(' de ')[1].replace('.', '')) // 25
        if int(texto_paginacao.split(' de ')[1].replace('.', '')) % 25 > 0:
            total_paginas += 1
    else:
        total_paginas = 1  # Se não tiver "de", é apenas uma página
    log_message("info",f"Total de páginas encontrado: {total_paginas}")
except Exception as e:
    logging.warning("Não foi possível encontrar o número de páginas. Assumindo que há apenas uma página.")
    logging.exception(e)

try:
    pagina_select = wait.until(EC.presence_of_element_located((By.ID, "tipoPessoa")))
    select_pagina = Select(pagina_select)
    options = select_pagina.options  # Obter todas as opções
    log_message("info", f"Opções disponíveis no dropdown: {[option.text for option in options]}")
except Exception as e:
    log_message("error", f"Erro ao tentar obter as opções do dropdown: {e}")

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
filename = f"dados_susep_{timestamp}.csv"

for pagina in range(107, total_paginas+1):  # Começa da página 1
    log_message("info",f"Extraindo página {pagina}/{total_paginas}")

    try:
        extrair_e_salvar(driver, filename)
    except:
        log_message("erro",f"Deu merda na pagina: {pagina}")

    if pagina < total_paginas:
        try:
            # Encontra o elemento select
            pagina_selects = wait.until(EC.presence_of_all_elements_located((By.ID, "tipoPessoa")))
            pagina_select = pagina_selects[-1]
            select_pagina = Select(pagina_select)

            # Seleciona a página desejada
            select_pagina.select_by_value(str(pagina + 1))  # Converte para string

            log_message("info", f"Selecionando página {pagina + 1} no dropdown.")
            time.sleep(10)

        except Exception as e:
            logging.error(f"Erro ao selecionar a página {pagina + 1} no dropdown: {e}")
            # Tentar selecionar página por página
            log_message("warning", "Tentando selecionar página por página:")
            page_found = False
            for tentativa_pagina in range(pagina + 1, total_paginas + 1):  # Tenta TODAS as páginas até o total
                try:
                    # Localiza o elemento select NOVAMENTE dentro do loop
                    pagina_select = wait.until(EC.presence_of_element_located((By.ID, "tipoPessoa")))

                    # Espera as opções carregarem dentro do dropdown (mais importante)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#tipoPessoa option[value="{tentativa_pagina}"]')))

                    select_pagina = Select(pagina_select)
                    select_pagina.select_by_value(str(tentativa_pagina))
                    log_message("info", f"Página {tentativa_pagina} selecionada com sucesso após tentativa individual.")
                    time.sleep(10)
                    page_found = True
                    break # Encontrou a página, interrompe o loop de tentativas
                except Exception as e2:
                    log_message("warning", f"Falha ao tentar selecionar página {tentativa_pagina} individualmente: {e2}")

            if not page_found:
                log_message("error", "Falha ao avançar para a próxima página, mesmo após tentativas individuais.")
                break


# Fecha o navegador
driver.quit()

print("Extração concluída!")

time.sleep(20)

