from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Baixa e usa a versão correta do ChromeDriver automaticamente
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.google.com")
print("ChromeDriver atualizado e funcionando!")
driver.quit()

