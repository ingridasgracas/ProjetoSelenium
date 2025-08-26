from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://pref.rio/")

    # Espera até que links estejam disponíveis
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

    # Coleta todos os <a> da página
    all_links = driver.find_elements(By.TAG_NAME, "a")

    dados = []
    for link in all_links:
        href = link.get_attribute("href")
        texto = link.text.strip()

        if href and texto:  # só pega links que têm texto visível
            # filtro básico: ignora links internos de navegação tipo "#", "javascript:"
            if not href.startswith("javascript") and not href.endswith("#"):
                dados.append({"Servico": texto, "URL": href})

    # Converte para DataFrame
    df = pd.DataFrame(dados).drop_duplicates()

    # Salva em CSV e Excel
    df.to_csv("links_pref_rio.csv", index=False, encoding="utf-8-sig")
    df.to_excel("links_pref_rio.xlsx", index=False)

    print(f"✅ Arquivos gerados com {len(df)} links úteis")

finally:
    driver.quit()
