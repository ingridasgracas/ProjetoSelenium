from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=chrome_options)

try:
    # 1 - Abre o site inicial
    driver.get("https://pref.rio/")

    wait = WebDriverWait(driver, 20)

    # 2 - Clica no botão azul de transição para Serviços
    botao_servicos = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/servicos']"))
    )
    botao_servicos.click()

    # 3 - Aguarda carregar a página de serviços
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

    # Dá um tempo extra pra renderizar tudo
    time.sleep(3)

    # Captura todas as categorias e links
    categorias = driver.find_elements(By.CSS_SELECTOR, "section a")

    dados = []
    for item in categorias:
        href = item.get_attribute("href")
        texto = item.text.strip()

        if href and texto:
            dados.append({
                "Categoria/Serviço": texto,
                "URL": href
            })

    # Converte para DataFrame
    df = pd.DataFrame(dados).drop_duplicates()

    # 4 - Exporta para Excel
    df.to_excel("servicos_pref_rio.xlsx", index=False)

    print(f"✅ Arquivo gerado: servicos_pref_rio.xlsx com {len(df)} registros")

finally:
    driver.quit()
