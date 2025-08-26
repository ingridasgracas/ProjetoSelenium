from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--headless=new")  # Se quiser rodar sem abrir janela

driver = webdriver.Chrome(options=chrome_options)

try:
    # Abre o site
    driver.get("https://pref.rio/")

    # Espera o menu/carregamento (ajusta se necessário)
    wait = WebDriverWait(driver, 15)

    # Dá um tempo pro JS renderizar (pode trocar por espera explícita se achar melhor)
    time.sleep(5)

    # Procura todos os links da seção de serviços
    # Testei a estrutura: os serviços aparecem em <a> dentro de cards
    service_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/servicos/']")

    links_extraidos = []
    for link in service_links:
        href = link.get_attribute("href")
        texto = link.text.strip()
        if href and href not in links_extraidos:
            links_extraidos.append(href)
            print(f"{texto} -> {href}")

    print(f"\nTotal de links coletados: {len(links_extraidos)}")

finally:
    driver.quit()
