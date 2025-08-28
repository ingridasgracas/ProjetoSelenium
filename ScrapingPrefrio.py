from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
import os
from typing import List, Dict, Optional

def setup_driver() -> webdriver.Chrome:
    """Configura e retorna o driver do Chrome."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")  # Executa em modo headless
    return webdriver.Chrome(options=options)

def get_link_final(driver: webdriver.Chrome, url: str, wait: WebDriverWait) -> Optional[str]:
    """Tenta obter o link final de uma página de serviço."""
    try:
        driver.get(url)
        time.sleep(1)  # Pequena pausa para carregar
        botao = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Acessar serviço')]")))
        return botao.get_attribute("href")
    except (TimeoutException, NoSuchElementException):
        print(f"Não foi possível obter o link final para: {url}")
        return None

# Lista de serviços da Prefeitura do Rio
servicos = [
    # Educação
    {"Categoria": "Educação", "Serviço": "Consultar Declaração de Escolaridade", "URL": "https://pref.rio/servicos/categoria/educacao/68687/carioca-digital"},
    {"Categoria": "Educação", "Serviço": "Informações sobre avaliação de aluno incluído", "URL": "https://pref.rio/servicos/categoria/educacao/10603372091675/1746"},
    {"Categoria": "Educação", "Serviço": "Material Rioeduca", "URL": "https://pref.rio/servicos/categoria/educacao/90643/carioca-digital"},
    {"Categoria": "Educação", "Serviço": "Incluir Aluno para acompanhamento escolar", "URL": "https://pref.rio/servicos/categoria/educacao/68617/carioca-digital"},
    {"Categoria": "Educação", "Serviço": "Consultar Calendário Escolar", "URL": "https://pref.rio/servicos/categoria/educacao/68683/carioca-digital"},
    {"Categoria": "Educação", "Serviço": "Matrícula em Creche Municipal", "URL": "https://pref.rio/servicos/categoria/educacao/70742/carioca-digital"},
    {"Categoria": "Educação", "Serviço": "Informações sobre o auxílio educação", "URL": "https://pref.rio/servicos/categoria/educacao/10822819825691/1746"},
    {"Categoria": "Educação", "Serviço": "Matrícula na Pré-Escola, Ensino Fundamental e Educação de Jovens e Adultos", "URL": "https://pref.rio/servicos/categoria/educacao/70758/carioca-digital"},
    {"Categoria": "Educação", "Serviço": "Atendimento em Ouvidoria - SME", "URL": "https://pref.rio/servicos/categoria/educacao/10618383693979/1746"},
    {"Categoria": "Educação", "Serviço": "Informações sobre matrícula na rede municipal - 2025", "URL": "https://pref.rio/servicos/categoria/educacao/31273172690203/1746"},
    {"Categoria": "Educação", "Serviço": "Consulta à Merenda Escolar", "URL": "https://pref.rio/servicos/categoria/educacao/69334/carioca-digital"},
    {"Categoria": "Educação", "Serviço": "consulta de Endereço das Escolas Públicas Municipais", "URL": "https://pref.rio/servicos/categoria/educacao/92245/carioca-digital"},
    {"Categoria": "Educação", "Serviço": "Suporte Técnico às Plataformas MultiRio", "URL": "https://pref.rio/servicos/categoria/educacao/10605210315163/1746"},
    {"Categoria": "Educação", "Serviço": "O que é Nave do Conhecimento?", "URL": "https://pref.rio/servicos/categoria/educacao/88208/carioca-digital"},
    {"Categoria": "Educação", "Serviço": "Matrícula na Educação Especial", "URL": "https://pref.rio/servicos/categoria/educacao/70721/carioca-digital"},
    {"Categoria": "Educação", "Serviço": "Verificação de legalização/licenciamento de estabelecimento de educação infantil", "URL": "https://pref.rio/servicos/categoria/educacao/10603589891995/1746"},
    {"Categoria": "Educação", "Serviço": "Informação sobre os produtos e projetos da MultiRio", "URL": "https://pref.rio/servicos/categoria/educacao/106245/carioca-digital"},
    {"Categoria": "Educação", "Serviço": "Informações sobre a inclusão de alunos da Educação Especial", "URL": "https://pref.rio/servicos/categoria/educacao/10603313155483/1746"},
    {"Categoria": "Educação", "Serviço": "Informações sobre envio de material educativo para a MultiRio", "URL": "https://pref.rio/servicos/categoria/educacao/10605164173211/1746"},
    {"Categoria": "Educação", "Serviço": "Informações sobre doação de livros", "URL": "https://pref.rio/servicos/categoria/educacao/10602999705115/1746"},

    # Cidade
    {"Categoria": "Cidade", "Serviço": "Reparo de buraco, deformação ou afundamento na pista", "URL": "https://pref.rio/servicos/categoria/cidade/10221381930523/1746"},
    {"Categoria": "Cidade", "Serviço": "Reparo de Luminária", "URL": "https://pref.rio/servicos/categoria/cidade/14187518715931/1746"},
    {"Categoria": "Cidade", "Serviço": "Remoção de entulho e bens inservíveis", "URL": "https://pref.rio/servicos/categoria/cidade/10219766128667/1746"},
    {"Categoria": "Cidade", "Serviço": "Manutenção/Desobstrução de ramais de águas pluviais e ralos", "URL": "https://pref.rio/servicos/categoria/cidade/10221176323867/1746"},
    {"Categoria": "Cidade", "Serviço": "Remoção de resíduos no logradouro", "URL": "https://pref.rio/servicos/categoria/cidade/10221449761795/1746"},
    {"Categoria": "Cidade", "Serviço": "Varrição de logradouro", "URL": "https://pref.rio/servicos/categoria/cidade/10735195018011/1746"},
    {"Categoria": "Cidade", "Serviço": "Reposição de tampão ou grelha", "URL": "https://pref.rio/servicos/categoria/cidade/10272405094043/1746"},
    {"Categoria": "Cidade", "Serviço": "Verificação de frequência irregular da coleta domiciliar com retirada do resíduo", "URL": "https://pref.rio/servicos/categoria/cidade/10734140106779/1746"},
    {"Categoria": "Cidade", "Serviço": "Capina em logradouro", "URL": "https://pref.rio/servicos/categoria/cidade/10221022905115/1746"},
    {"Categoria": "Cidade", "Serviço": "Fiscalização de obras em imóvel privado", "URL": "https://pref.rio/servicos/categoria/cidade/10822996862875/1746"},
    {"Categoria": "Cidade", "Serviço": "Remoção de veículo abandonado em via pública", "URL": "https://pref.rio/servicos/categoria/cidade/10221186863003/1746"},
    {"Categoria": "Cidade", "Serviço": "Remoção de resíduos de poda", "URL": "https://pref.rio/servicos/categoria/cidade/10735131383451/1746"},
    {"Categoria": "Cidade", "Serviço": "Fiscalização da ocupação de área pública", "URL": "https://pref.rio/servicos/categoria/cidade/14208565911963/1746"},
    {"Categoria": "Cidade", "Serviço": "Fiscalização de obstáculo fixo na calçada", "URL": "https://pref.rio/servicos/categoria/cidade/10275708915099/1746"},
    {"Categoria": "Cidade", "Serviço": "Fiscalização de buraco na calçada", "URL": "https://pref.rio/servicos/categoria/cidade/10275708915099/1746"},
    {"Categoria": "Cidade", "Serviço": "Consultar Certidão de Habite-se/Aceitação", "URL": "https://pref.rio/servicos/categoria/cidade/82661/carioca-digital"},
    {"Categoria": "Cidade", "Serviço": "Informações sobre processos da Rio-Águas", "URL": "https://pref.rio/servicos/categoria/cidade/77868/carioca-digital"},
    {"Categoria": "Cidade", "Serviço": "Reparo de cabo de iluminação pública", "URL": "https://pref.rio/servicos/categoria/cidade/14191400984987/1746"},
    {"Categoria": "Cidade", "Serviço": "Limpeza de papeleira, contêiner e caçamba da COMLURB", "URL": "https://pref.rio/servicos/categoria/cidade/10734897643291/1746"},
    {"Categoria": "Cidade", "Serviço": "Limpeza de praças e parques", "URL": "https://pref.rio/servicos/categoria/cidade/10734900601371/1746"},

    # Transporte
    {"Categoria": "Transporte", "Serviço": "Fiscalização de estacionamento irregular de veículo", "URL": "https://pref.rio/servicos/categoria/transporte/10872633493659/1746"},
    {"Categoria": "Transporte", "Serviço": "Cartão de Estacionamento para Idoso", "URL": "https://pref.rio/servicos/categoria/transporte/69155/carioca-digital"},
    {"Categoria": "Transporte", "Serviço": "Fiscalização de má conduta do motorista/despachante", "URL": "https://pref.rio/servicos/categoria/transporte/14207792262299/1746"},
    {"Categoria": "Transporte", "Serviço": "Reparo de sinal de trânsito apagado", "URL": "https://pref.rio/servicos/categoria/transporte/10220783937691/1746"},
    {"Categoria": "Transporte", "Serviço": "Informações sobre gratuidade em ônibus", "URL": "https://pref.rio/servicos/categoria/transporte/10246609668891/1746"},
    {"Categoria": "Transporte", "Serviço": "Verificação de ar condicionado inoperante no ônibus", "URL": "https://pref.rio/servicos/categoria/transporte/10870066623003/1746"},
    {"Categoria": "Transporte", "Serviço": "Cartão de estacionamento para pessoas com deficiência – PCD", "URL": "https://pref.rio/servicos/categoria/transporte/10872531918363/1746"},
    {"Categoria": "Transporte", "Serviço": "Fiscalização de má condição do ônibus", "URL": "https://pref.rio/servicos/categoria/transporte/14207681718299/1746"},
    {"Categoria": "Transporte", "Serviço": "Informações sobre a Jaé", "URL": "https://pref.rio/servicos/categoria/transporte/91583/carioca-digital"},
    {"Categoria": "Transporte", "Serviço": "Consulta de Multas por Permissão em Taxi", "URL": "https://pref.rio/servicos/categoria/transporte/91841/carioca-digital"},
    {"Categoria": "Transporte", "Serviço": "Cadastramento para obtenção de Riocard Especial", "URL": "https://pref.rio/servicos/categoria/transporte/10869907577755/1746"},
    {"Categoria": "Transporte", "Serviço": "Multa de Trânsito – 2ª Instância", "URL": "https://pref.rio/servicos/categoria/transporte/89838/carioca-digital"},
    {"Categoria": "Transporte", "Serviço": "Emissão de boleto para pagamento de multa (DARM) no VLT", "URL": "https://pref.rio/servicos/categoria/transporte/99086/carioca-digital"},
    {"Categoria": "Transporte", "Serviço": "Solicitação de manutenção de sinalização gráfica vertical viária", "URL": "https://pref.rio/servicos/categoria/transporte/10873508661659/1746"},
    {"Categoria": "Transporte", "Serviço": "Passe Livre", "URL": "https://pref.rio/servicos/categoria/transporte/72584/carioca-digital"},
    {"Categoria": "Transporte", "Serviço": "Solicitação de balizamento de trânsito", "URL": "https://pref.rio/servicos/categoria/transporte/10873513958555/1746"},
    {"Categoria": "Transporte", "Serviço": "Reparo de sinal de trânsito em amarelo piscante", "URL": "https://pref.rio/servicos/categoria/transporte/10873296416411/1746"},
    {"Categoria": "Transporte", "Serviço": "Reparo de sinal de trânsito abalroado ou ausente ou virado", "URL": "https://pref.rio/servicos/categoria/transporte/10873296416411/1746"},
    {"Categoria": "Transporte", "Serviço": "Fiscalização da atuação do guardador de estacionamento Rio Rotativo", "URL": "https://pref.rio/servicos/categoria/transporte/10872589397531/1746"},
    {"Categoria": "Transporte", "Serviço": "Emissão de Taxas por Permissão em Taxi", "URL": "https://pref.rio/servicos/categoria/transporte/91836/carioca-digital"},

    # Licenças
    {"Categoria": "Licenças", "Serviço": "Licença Sanitária de Funcionamento", "URL": "https://pref.rio/servicos/categoria/licencas/69823/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Autorização para exibição de publicidade", "URL": "https://pref.rio/servicos/categoria/licencas/105555/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Concessão de alvará de licença de estabelecimento pela internet", "URL": "https://pref.rio/servicos/categoria/licencas/69572/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Solicitação de orientações sobre o alvará pela internet", "URL": "https://pref.rio/servicos/categoria/licencas/10619035948443/1746"},
    {"Categoria": "Licenças", "Serviço": "Autorização / legalização de comércio ambulante", "URL": "https://pref.rio/servicos/categoria/licencas/68976/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Segunda via de alvará", "URL": "https://pref.rio/servicos/categoria/licencas/68976/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Alvará a Jato", "URL": "https://pref.rio/servicos/categoria/licencas/91037/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Pesquisa de existência de alvará", "URL": "https://pref.rio/servicos/categoria/licencas/78566/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Fiscalização de alimentos, indústria de alimentos e estabelecimentos de ensino", "URL": "https://pref.rio/servicos/categoria/licencas/15042296187547/1746"},
    {"Categoria": "Licenças", "Serviço": "Minhas Empresas/Cadastrar Procurador de Empresa", "URL": "https://pref.rio/servicos/categoria/licencas/68859/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Consulta de Situação Cadastral por Permissão", "URL": "https://pref.rio/servicos/categoria/licencas/69771/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Autorização de funcionamento para banca de jornal e revistas", "URL": "https://pref.rio/servicos/categoria/licencas/69582/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Fiscalização de atividades econômicas sem alvará", "URL": "https://pref.rio/servicos/categoria/licencas/10221222516123/1746"},
    {"Categoria": "Licenças", "Serviço": "Informação sobre Fiscalização de comércio ambulante", "URL": "https://pref.rio/servicos/categoria/licencas/10764598956187/1746"},
    {"Categoria": "Licenças", "Serviço": "Baixa de alvará de licença de estabelecimento", "URL": "https://pref.rio/servicos/categoria/licencas/68981/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Agendamento de atendimento presencial", "URL": "https://pref.rio/servicos/categoria/licencas/82682/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Minhas Bancas de jornais e revistas", "URL": "https://pref.rio/servicos/categoria/licencas/69067/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Autorização para Publicidade Vinculada a Eventos", "URL": "https://pref.rio/servicos/categoria/licencas/89312/carioca-digital"},
    {"Categoria": "Licenças", "Serviço": "Fiscalização de serviços de embelezamento e atividades físicas", "URL": "https://pref.rio/servicos/categoria/licencas/14206697563291/1746"},
    {"Categoria": "Licenças", "Serviço": "Licença para construção ou modificação de edificação/ LICIN, prorrogação de licença", "URL": "https://pref.rio/servicos/categoria/licencas/82573/carioca-digital"},

    # Animais
    {"Categoria": "Animais", "Serviço": "Vistoria técnica em situações de maus tratos de animais domésticos", "URL": "https://pref.rio/servicos/categoria/animais/10242348321307/1746"},
    {"Categoria": "Animais", "Serviço": "Atendimento clínico consultas e exames em animais", "URL": "https://pref.rio/servicos/categoria/animais/72777/carioca-digital"},
    {"Categoria": "Animais", "Serviço": "Remoção de cavalos, bois, porcos e cabras soltos ou gravemente feridos em via pública", "URL": "https://pref.rio/servicos/categoria/animais/14206085972635/1746"},
    {"Categoria": "Animais", "Serviço": "Remoção de animais mortos no logradouro", "URL": "https://pref.rio/servicos/categoria/animais/10735113229467/1746"},
    {"Categoria": "Animais", "Serviço": "Avaliação de cães e gatos suspeitos de raiva animal", "URL": "https://pref.rio/servicos/categoria/animais/10769417877531/1746"},
    {"Categoria": "Animais", "Serviço": "Vistoria em logradouros públicos ou privados para avaliação de gatos errantes com suspeita de Esporotricose", "URL": "https://pref.rio/servicos/categoria/animais/10769448781851/1746"},
    {"Categoria": "Animais", "Serviço": "Captura para análise de morcegos caídos ou que atacaram pessoas e/ou animais", "URL": "https://pref.rio/servicos/categoria/animais/10244670472731/1746"},
    {"Categoria": "Animais", "Serviço": "Atendimento domiciliar para vacinação antirrábica animal", "URL": "https://pref.rio/servicos/categoria/animais/10769393994267/1746"},
    {"Categoria": "Animais", "Serviço": "Selo Amigo dos Animais", "URL": "https://pref.rio/servicos/categoria/animais/90609/carioca-digital"},
    {"Categoria": "Animais", "Serviço": "Realização de exames laboratoriais em animais", "URL": "https://pref.rio/servicos/categoria/animais/10735588434715/1746"},
    {"Categoria": "Animais", "Serviço": "Sepultamento no cemitério de pequenos animais", "URL": "https://pref.rio/servicos/categoria/animais/9894548857243/1746"},
    {"Categoria": "Animais", "Serviço": "Cemitérios e Crematórios Particulares Para Animais", "URL": "https://pref.rio/servicos/categoria/animais/103663/carioca-digital"},
    {"Categoria": "Animais", "Serviço": "Fiscalização de eventos com exposição de animais", "URL": "https://pref.rio/servicos/categoria/animais/10769796985243/1746"},
    {"Categoria": "Animais", "Serviço": "Atendimento a reações adversas à vacinação antirrábica animal", "URL": "https://pref.rio/servicos/categoria/animais/10769413378715/1746"},
    {"Categoria": "Animais", "Serviço": "Fiscalização de criações de cães, gatos, cavalos, bois, porcos, cabras e aves para fins comerciais", "URL": "https://pref.rio/servicos/categoria/animais/10769791026843/1746"},
    {"Categoria": "Animais", "Serviço": "Análise de cães com suspeita de Leishmaniose", "URL": "https://pref.rio/servicos/categoria/animais/10769815640475/1746"},
    {"Categoria": "Animais", "Serviço": "Treinamento e noções básicas de normas sanitárias e boas práticas para petshops", "URL": "https://pref.rio/servicos/categoria/animais/72501/carioca-digital"},
    {"Categoria": "Animais", "Serviço": "Realização de exames laboratoriais para diagnóstico de raiva animal", "URL": "https://pref.rio/servicos/categoria/animais/10735594729755/1746"},
    {"Categoria": "Animais", "Serviço": "Análise, orientação ou fiscalização de casos de animais peçonhentos ou venenosos", "URL": "https://pref.rio/servicos/categoria/animais/10769350508187/1746"},

    # Ambiente
    {"Categoria": "Ambiente", "Serviço": "Controle de roedores e caramujos africanos", "URL": "https://pref.rio/servicos/categoria/ambiente/10734204259739/1746"},
    {"Categoria": "Ambiente", "Serviço": "Poda de árvore em logradouro", "URL": "https://pref.rio/servicos/categoria/ambiente/10220671680795/1746"},
    {"Categoria": "Ambiente", "Serviço": "Resgate de animais silvestres", "URL": "https://pref.rio/servicos/categoria/ambiente/9893467480603/1746"},
    {"Categoria": "Ambiente", "Serviço": "Remoção de árvore em logradouro", "URL": "https://pref.rio/servicos/categoria/ambiente/10735595148315/1746"},
    {"Categoria": "Ambiente", "Serviço": "Avaliação de risco de queda da árvore", "URL": "https://pref.rio/servicos/categoria/ambiente/10821516479131/1746"},
    {"Categoria": "Ambiente", "Serviço": "Fiscalização de carros de som", "URL": "https://pref.rio/servicos/categoria/ambiente/10858511419163/1746"},
    {"Categoria": "Ambiente", "Serviço": "Fiscalização de corte, sacrifício de árvore ou remoção de vegetação", "URL": "https://pref.rio/servicos/categoria/ambiente/10821210051099/1746"},
    {"Categoria": "Ambiente", "Serviço": "Fiscalização de poluição sonora", "URL": "https://pref.rio/servicos/categoria/ambiente/10822326091803/1746"},
    {"Categoria": "Ambiente", "Serviço": "Solicitação de plantio de árvore em área pública", "URL": "https://pref.rio/servicos/categoria/ambiente/10801075133723/1746"},
    {"Categoria": "Ambiente", "Serviço": "Certidão Municipal de Inexigibilidade de Licenciamento Ambiental", "URL": "https://pref.rio/servicos/categoria/ambiente/82560/carioca-digital"},
    {"Categoria": "Ambiente", "Serviço": "Autorização de poda ou remoção de árvore em área particular", "URL": "https://pref.rio/servicos/categoria/ambiente/76072/carioca-digital"},
    {"Categoria": "Ambiente", "Serviço": "Fiscalização de Poluição do ar", "URL": "https://pref.rio/servicos/categoria/ambiente/10822321713691/1746"},
    {"Categoria": "Ambiente", "Serviço": "Relação de licenças ambientais emitidas", "URL": "https://pref.rio/servicos/categoria/ambiente/82675/carioca-digital"},
    {"Categoria": "Ambiente", "Serviço": "Poda de árvores em áreas privadas", "URL": "https://pref.rio/servicos/categoria/ambiente/76126/carioca-digital"},
    {"Categoria": "Ambiente", "Serviço": "Autorização de poda ou remoção de árvore em área pública", "URL": "https://pref.rio/servicos/categoria/ambiente/76072/carioca-digital"},
    {"Categoria": "Ambiente", "Serviço": "Poluição hídrica ou da água", "URL": "https://pref.rio/servicos/categoria/ambiente/10822324804891/1746"},
    {"Categoria": "Ambiente", "Serviço": "Verificação de frequência irregular de coleta seletiva", "URL": "https://pref.rio/servicos/categoria/ambiente/10734082516251/1746"},
    {"Categoria": "Ambiente", "Serviço": "Arborização para HABITE-SE", "URL": "https://pref.rio/servicos/categoria/ambiente/76130/carioca-digital"},
    {"Categoria": "Ambiente", "Serviço": "Fiscalização de desmatamento", "URL": "https://pref.rio/servicos/categoria/ambiente/10821275797275/1746"},
    {"Categoria": "Ambiente", "Serviço": "Análise, orientação ou fiscalização de pombos em instituições", "URL": "https://pref.rio/servicos/categoria/ambiente/10769377431067/1746"},

    # Saúde
    {"Categoria": "Saúde", "Serviço": "Solicitação de transporte da gestante para a maternidade", "URL": "https://pref.rio/servicos/categoria/saude/10735826487067/1746"},
    {"Categoria": "Saúde", "Serviço": "Vistoria em foco de Aedes Aegypti", "URL": "https://pref.rio/servicos/categoria/saude/10221081525787/1746"},
    {"Categoria": "Saúde", "Serviço": "Solicitação de vacinação em domicílio", "URL": "https://pref.rio/servicos/categoria/saude/33440989114651/1746"},
    {"Categoria": "Saúde", "Serviço": "Atendimento em Unidades de Atenção Primária em Saúde", "URL": "https://pref.rio/servicos/categoria/saude/10730171791131/1746"},
    {"Categoria": "Saúde", "Serviço": "Acesso a outros Requerimentos da Vigilância Sanitária", "URL": "https://pref.rio/servicos/categoria/saude/69845/carioca-digital"},
    {"Categoria": "Saúde", "Serviço": "Vistoria em local com presença de insetos", "URL": "https://pref.rio/servicos/categoria/saude/10244568071067/1746"},
    {"Categoria": "Saúde", "Serviço": "Atendimento em Policlínicas", "URL": "https://pref.rio/servicos/categoria/saude/10729690213787/1746"},
    {"Categoria": "Saúde", "Serviço": "Fiscalização de estabelecimentos de serviços de saúde", "URL": "https://pref.rio/servicos/categoria/saude/15311237178267/1746"},
    {"Categoria": "Saúde", "Serviço": "Inscrição em programa de antitabagismo", "URL": "https://pref.rio/servicos/categoria/saude/71235/carioca-digital"},
    {"Categoria": "Saúde", "Serviço": "Análise, orientação ou fiscalização de morcegos em instituições públicas", "URL": "https://pref.rio/servicos/categoria/saude/10769352760347/1746"},
    {"Categoria": "Saúde", "Serviço": "Treinamento Noções básicas de higiene na manipulação de alimentos", "URL": "https://pref.rio/servicos/categoria/saude/72478/carioca-digital"},
    {"Categoria": "Saúde", "Serviço": "Atendimento à Saúde do Adulto", "URL": "https://pref.rio/servicos/categoria/saude/10730118160411/1746"},
    {"Categoria": "Saúde", "Serviço": "Cadastramento para obtenção de Cartão Nacional SUS", "URL": "https://pref.rio/servicos/categoria/saude/10730622523675/1746"},
    {"Categoria": "Saúde", "Serviço": "Disponibilização de cursos, palestras e treinamentos na área da Vigilância Sanitária", "URL": "https://pref.rio/servicos/categoria/saude/72459/carioca-digital"},
    {"Categoria": "Saúde", "Serviço": "Atendimento à Saúde da Criança e do Adolescente", "URL": "https://pref.rio/servicos/categoria/saude/10730049310107/1746"},
    {"Categoria": "Saúde", "Serviço": "Atendimento em Centros de Reabilitação", "URL": "https://pref.rio/servicos/categoria/saude/10729631964187/1746"},
    {"Categoria": "Saúde", "Serviço": "Captura para análise de macacos ou micos achados mortos", "URL": "https://pref.rio/servicos/categoria/saude/10769330142491/1746"},
    {"Categoria": "Saúde", "Serviço": "Verificação de descumprimento dos prazos para atendimento", "URL": "https://pref.rio/servicos/categoria/saude/78297/carioca-digital"},
    {"Categoria": "Saúde", "Serviço": "Avaliação de surto por doença transmitida por alimentos e água", "URL": "https://pref.rio/servicos/categoria/saude/10763993854107/1746"},
    {"Categoria": "Saúde", "Serviço": "Atendimento em Hospitais Especializados", "URL": "https://pref.rio/servicos/categoria/saude/10729869001755/1746"},

    # Cidadania
    {"Categoria": "Cidadania", "Serviço": "Cadastro e acesso ao Portal Carioca Digital", "URL": "https://pref.rio/servicos/categoria/cidadania/77560/carioca-digital"},
    {"Categoria": "Cidadania", "Serviço": "Consultar Minhas Solicitações", "URL": "https://pref.rio/servicos/categoria/cidadania/89017/carioca-digital"},
    {"Categoria": "Cidadania", "Serviço": "Certidão Negativa de Débito (nada consta)", "URL": "https://pref.rio/servicos/categoria/cidadania/10858939404955/1746"},
    {"Categoria": "Cidadania", "Serviço": "Solicitação de correção de falhas e de cadastro no portal e app 1746", "URL": "https://pref.rio/servicos/categoria/cidadania/10835703629595/1746"},
    {"Categoria": "Cidadania", "Serviço": "Solicitação de serviços para os povos e comunidades tradicionais", "URL": "https://pref.rio/servicos/categoria/cidadania/19495199226139/1746"},
    {"Categoria": "Cidadania", "Serviço": "Pedido de Acesso à Informação", "URL": "https://pref.rio/servicos/categoria/cidadania/9567624997403/1746"},
    {"Categoria": "Cidadania", "Serviço": "Cópia ou Certidão de inteiro teor de documento ou processo", "URL": "https://pref.rio/servicos/categoria/cidadania/103709/carioca-digital"},
    {"Categoria": "Cidadania", "Serviço": "Consulta de Processos Administrativos Eletrônicos", "URL": "https://pref.rio/servicos/categoria/cidadania/88424/carioca-digital"},
    {"Categoria": "Cidadania", "Serviço": "Consulta de dados no Portal da Transparência Rio", "URL": "https://pref.rio/servicos/categoria/cidadania/81712/carioca-digital"},
    {"Categoria": "Cidadania", "Serviço": "Certidão de histórico de reconhecimento de logradouro", "URL": "https://pref.rio/servicos/categoria/cidadania/10858885321755/1746"},
    {"Categoria": "Cidadania", "Serviço": "Certidão de Histórico de Revisão de Numeração", "URL": "https://pref.rio/servicos/categoria/cidadania/83861/carioca-digital"},
    {"Categoria": "Cidadania", "Serviço": "Insatisfação com o atendimento da Central 1746", "URL": "https://pref.rio/servicos/categoria/cidadania/10835733794715/1746"},
    {"Categoria": "Cidadania", "Serviço": "Consulta ao Acervo do Arquivo Geral da Cidade do Rio de Janeiro", "URL": "https://pref.rio/servicos/categoria/cidadania/81556/carioca-digital"},
    {"Categoria": "Cidadania", "Serviço": "Solicitação da gravação do atendimento 1746", "URL": "https://pref.rio/servicos/categoria/cidadania/10835710164123/1746"},
    {"Categoria": "Cidadania", "Serviço": "Notificação de Casos de Intolerância Étnico-Racial", "URL": "https://pref.rio/servicos/categoria/cidadania/17789434460187/1746"},
    {"Categoria": "Cidadania", "Serviço": "Consulta à Legislação", "URL": "https://pref.rio/servicos/categoria/cidadania/78775/carioca-digital"},
    {"Categoria": "Cidadania", "Serviço": "Eventos de conciliação do Procon Carioca", "URL": "https://pref.rio/servicos/categoria/cidadania/10619440114331/1746"},
    {"Categoria": "Cidadania", "Serviço": "Certificado de Aceitação das Condições de Acessibilidade", "URL": "https://pref.rio/servicos/categoria/cidadania/70850/carioca-digital"},
    {"Categoria": "Cidadania", "Serviço": "Consulta de Processos Administrativos Físicos", "URL": "https://pref.rio/servicos/categoria/cidadania/93077/carioca-digital"},
    {"Categoria": "Cidadania", "Serviço": "Verificação de Autenticidade de Documentos", "URL": "https://pref.rio/servicos/categoria/cidadania/88180/carioca-digital"},

    # Família
    {"Categoria": "Família", "Serviço": "Informações sobre o Cadastro Único", "URL": "https://pref.rio/servicos/categoria/familia/72307/carioca-digital"},
    {"Categoria": "Família", "Serviço": "CADRio Agendamento", "URL": "https://pref.rio/servicos/categoria/familia/92294/carioca-digital"},
    {"Categoria": "Família", "Serviço": "Informações sobre o Programa Bolsa Família", "URL": "https://pref.rio/servicos/categoria/familia/10245041321371/1746"},
    {"Categoria": "Família", "Serviço": "Pessoas em situação de rua", "URL": "https://pref.rio/servicos/categoria/familia/10221121590427/1746"},
    {"Categoria": "Família", "Serviço": "Verificação de negligência com idoso", "URL": "https://pref.rio/servicos/categoria/familia/16520177628187/1746"},
    {"Categoria": "Família", "Serviço": "Solicitação de atendimento do Conselho Tutelar", "URL": "https://pref.rio/servicos/categoria/familia/16931805418011/1746"},
    {"Categoria": "Família", "Serviço": "Informações sobre a Carteira da Pessoa Idosa", "URL": "https://pref.rio/servicos/categoria/familia/10246636010395/1746"},
    {"Categoria": "Família", "Serviço": "Informações sobre o Programa Cartão Família Carioca", "URL": "https://pref.rio/servicos/categoria/familia/72410/carioca-digital"},
    {"Categoria": "Família", "Serviço": "Solicitação de atendimento social", "URL": "https://pref.rio/servicos/categoria/familia/14208514847515/1746"},
    {"Categoria": "Família", "Serviço": "Informações sobre o auxílio funeral", "URL": "https://pref.rio/servicos/categoria/familia/10822836882587/1746"},
    {"Categoria": "Família", "Serviço": "Solicitação de Assistência Domiciliar ao Idoso (PADI)", "URL": "https://pref.rio/servicos/categoria/familia/71176/carioca-digital"},
    {"Categoria": "Família", "Serviço": "Territórios Sociais", "URL": "https://pref.rio/servicos/categoria/familia/84085/carioca-digital"},
    {"Categoria": "Família", "Serviço": "Informações sobre inscrição e atualização do Cadastro Único", "URL": "https://pref.rio/servicos/categoria/familia/10244935327515/1746"},
    {"Categoria": "Família", "Serviço": "Informações sobre consulta e estorno de pagamento de benefícios", "URL": "https://pref.rio/servicos/categoria/familia/10822810014491/1746"},
    {"Categoria": "Família", "Serviço": "Fiscalização de abrigos para idosos", "URL": "https://pref.rio/servicos/categoria/familia/10244826205339/1746"},
    {"Categoria": "Família", "Serviço": "Informações sobre Assistência Financeira para funeral", "URL": "https://pref.rio/servicos/categoria/familia/10733248673051/1746"},
    {"Categoria": "Família", "Serviço": "Informações sobre a rede de enfrentamento às violências contra a mulher", "URL": "https://pref.rio/servicos/categoria/familia/10822486200091/1746"},
    {"Categoria": "Família", "Serviço": "Informações sobre o Programa Auxílio Gás dos Brasileiros", "URL": "https://pref.rio/servicos/categoria/familia/10245015233819/1746"},
    {"Categoria": "Família", "Serviço": "Informações sobre o Benefício de Prestação Continuada", "URL": "https://pref.rio/servicos/categoria/familia/10244939553179/1746"},
    {"Categoria": "Família", "Serviço": "Informações sobre acolhimento institucional", "URL": "https://pref.rio/servicos/categoria/familia/10244866638875/1746"},

    # Taxas
    {"Categoria": "Taxas", "Serviço": "ITBI – Simulação de Valor e Pedido de Guia", "URL": "https://pref.rio/servicos/categoria/taxas/83019/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "IPTU 2025", "URL": "https://pref.rio/servicos/categoria/taxas/84670/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "Parcelamento em dívida ativa", "URL": "https://pref.rio/servicos/categoria/taxas/82000/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "ISS – Comprovante de Inscrição", "URL": "https://pref.rio/servicos/categoria/taxas/82000/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "Emissão de certidão de dívida ativa", "URL": "https://pref.rio/servicos/categoria/taxas/81974/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "Pagamento à vista em dívida ativa", "URL": "https://pref.rio/servicos/categoria/taxas/82010/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "IPTU – Formulário de Alteração de Titularidade", "URL": "https://pref.rio/servicos/categoria/taxas/84746/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "IPTU – Certidão de Valor Venal", "URL": "https://pref.rio/servicos/categoria/taxas/84365/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "IPTU – Notificação de Lançamento", "URL": "https://pref.rio/servicos/categoria/taxas/84393/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "ISS – Confissão de dívida", "URL": "https://pref.rio/servicos/categoria/taxas/85315/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "IPTU – Consulta a logradouros", "URL": "https://pref.rio/servicos/categoria/taxas/84727/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "IPTU – Atualização de CPF/CNPJ", "URL": "https://pref.rio/servicos/categoria/taxas/86251/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "IPTU – Alteração de nome do proprietário", "URL": "https://pref.rio/servicos/categoria/taxas/84708/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "Emissão de Guia de Pagamento de Dívida Ativa em Atraso", "URL": "https://pref.rio/servicos/categoria/taxas/82013/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "Emissão Guia de Liquidação de Parcelamento", "URL": "https://pref.rio/servicos/categoria/taxas/74652/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "ISS – Pedido para emissão de certidão de Visto Fiscal", "URL": "https://pref.rio/servicos/categoria/taxas/83239/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "Dívida Ativa – Segunda Via de Cotas de Pagamento", "URL": "https://pref.rio/servicos/categoria/taxas/68789/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "Impressão de Taxa de Uso de Área Pública (TUAP)", "URL": "https://pref.rio/servicos/categoria/taxas/102070/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "IPTU – Autenticidade da Certidão", "URL": "https://pref.rio/servicos/categoria/taxas/84388/carioca-digital"},
    {"Categoria": "Taxas", "Serviço": "Ressarcimento de Taxas de Diárias", "URL": "https://pref.rio/servicos/categoria/taxas/100881/carioca-digital"},

    # Servidor
    {"Categoria": "Servidor", "Serviço": "Contracheque de servidor inativo e pensionista", "URL": "https://pref.rio/servicos/categoria/servidor/10824283848603/1746"},
    {"Categoria": "Servidor", "Serviço": "Consultar Validade de Contracheque", "URL": "https://pref.rio/servicos/categoria/servidor/68596/carioca-digital"},
    {"Categoria": "Servidor", "Serviço": "Benefícios relacionados ao falecimento do servidor", "URL": "https://pref.rio/servicos/categoria/servidor/10822734879771/1746"},
    {"Categoria": "Servidor", "Serviço": "Informações sobre o auxílio moradia", "URL": "https://pref.rio/servicos/categoria/servidor/10822897174683/1746"},
    {"Categoria": "Servidor", "Serviço": "Isenção de Imposto de Renda", "URL": "https://pref.rio/servicos/categoria/servidor/10823808737179/1746"},
    {"Categoria": "Servidor", "Serviço": "Informações sobre financiamento imobiliário no Previ-Rio", "URL": "https://pref.rio/servicos/categoria/servidor/10823657080859/1746"},
    {"Categoria": "Servidor", "Serviço": "Informações sobre empresas conveniadas", "URL": "https://pref.rio/servicos/categoria/servidor/10823964025499/1746"},
    {"Categoria": "Servidor", "Serviço": "Requerimento de Adiantamento de décimo terceiro", "URL": "https://pref.rio/servicos/categoria/servidor/78796/carioca-digital"},
    {"Categoria": "Servidor", "Serviço": "Informações sobre concursos públicos", "URL": "https://pref.rio/servicos/categoria/servidor/10859594080283/1746"},
    {"Categoria": "Servidor", "Serviço": "Informações sobre o auxílio natalidade", "URL": "https://pref.rio/servicos/categoria/servidor/10733298246939/1746"},
    {"Categoria": "Servidor", "Serviço": "Informações sobre o auxílio medicamento", "URL": "https://pref.rio/servicos/categoria/servidor/10822895234331/1746"},
    {"Categoria": "Servidor", "Serviço": "Averbação de tempo de contribuição", "URL": "https://pref.rio/servicos/categoria/servidor/79025/carioca-digital"},
    {"Categoria": "Servidor", "Serviço": "Redução de Carga Horária", "URL": "https://pref.rio/servicos/categoria/servidor/92881/carioca-digital"},
    {"Categoria": "Servidor", "Serviço": "Informações sobre senha para os benefícios", "URL": "https://pref.rio/servicos/categoria/servidor/10822922792731/1746"},
    {"Categoria": "Servidor", "Serviço": "Informações sobre Pecúlio", "URL": "https://pref.rio/servicos/categoria/servidor/10822916498331/1746"},
    {"Categoria": "Servidor", "Serviço": "Declaração do Imposto de Renda na Fonte", "URL": "https://pref.rio/servicos/categoria/servidor/76421/carioca-digital"},
    {"Categoria": "Servidor", "Serviço": "Informações sobre isenção de taxa de inscrição", "URL": "https://pref.rio/servicos/categoria/servidor/72331/carioca-digital"},
    {"Categoria": "Servidor", "Serviço": "Solicitação de Boletim de Inspeção Médica (BIM)", "URL": "https://pref.rio/servicos/categoria/servidor/104199/carioca-digital"},
    {"Categoria": "Servidor", "Serviço": "Consulta à Comissão de Integridade Pública (CIP)", "URL": "https://pref.rio/servicos/categoria/servidor/105499/carioca-digital"},

    # Cultura
    {"Categoria": "Cultura", "Serviço": "Visitação ao Museu do Universo no Planetário do Rio", "URL": "https://pref.rio/servicos/categoria/cultura/88400/carioca-digital"},
    {"Categoria": "Cultura", "Serviço": "Observação do Céu no Planetário do Rio", "URL": "https://pref.rio/servicos/categoria/cultura/88497/carioca-digital"},
    {"Categoria": "Cultura", "Serviço": "Sessões de cúpula no Planetário do Rio", "URL": "https://pref.rio/servicos/categoria/cultura/88500/carioca-digital"},
    {"Categoria": "Cultura", "Serviço": "Cursos de Astronomia no Planetário do Rio", "URL": "https://pref.rio/servicos/categoria/cultura/88190/carioca-digital"},
    {"Categoria": "Cultura", "Serviço": "Bibliotecas da Cultura", "URL": "https://pref.rio/servicos/categoria/cultura/75726/carioca-digital"},
    {"Categoria": "Cultura", "Serviço": "Requerimento de Inclusão e Exclusão de Técnica Artística", "URL": "https://pref.rio/servicos/categoria/cultura/19010400548123/1746"},
    {"Categoria": "Cultura", "Serviço": "Apoio à produções audiovisuais", "URL": "https://pref.rio/servicos/categoria/cultura/87459/carioca-digital"},
    {"Categoria": "Cultura", "Serviço": "Informações sobre o Programa Zonas de Cultura", "URL": "https://pref.rio/servicos/categoria/cultura/10419922514075/1746"},
    {"Categoria": "Cultura", "Serviço": "CONSELHO MUNICIPAL DE POLÍTICA CULTURAL", "URL": "https://pref.rio/servicos/categoria/cultura/75595/carioca-digital"},
    {"Categoria": "Cultura", "Serviço": "CALENDÁRIO DA REDE DE RODAS DE SAMBA", "URL": "https://pref.rio/servicos/categoria/cultura/76510/carioca-digital"},
    {"Categoria": "Cultura", "Serviço": "Cultura e arte", "URL": "https://pref.rio/servicos/categoria/cultura/77809/carioca-digital"},
    {"Categoria": "Cultura", "Serviço": "Venda de ingressos para os desfiles no Sambódromo", "URL": "https://pref.rio/servicos/categoria/cultura/78377/carioca-digital"},
    {"Categoria": "Cultura", "Serviço": "Concurso para Eleição da Rainha do Carnaval", "URL": "https://pref.rio/servicos/categoria/cultura/78442/carioca-digital"},
    {"Categoria": "Cultura", "Serviço": "Informações sobre o turismo em comunidade", "URL": "https://pref.rio/servicos/categoria/cultura/10420763037723/1746"},
    {"Categoria": "Cultura", "Serviço": "Informações sobre entretenimento noturno", "URL": "https://pref.rio/servicos/categoria/cultura/10420322968091/1746"},
    {"Categoria": "Cultura", "Serviço": "Informações sobre dados estatísticos de turismo", "URL": "https://pref.rio/servicos/categoria/cultura/10419727212571/1746"},
    {"Categoria": "Cultura", "Serviço": "Informações sobre gastronomia", "URL": "https://pref.rio/servicos/categoria/cultura/10419727212571/1746"},
    {"Categoria": "Cultura", "Serviço": "Informações sobre bailes de carnaval", "URL": "https://pref.rio/servicos/categoria/cultura/10412065825947/1746"},
    {"Categoria": "Cultura", "Serviço": "Disponibilização do acervo da Biblioteca da PGM", "URL": "https://pref.rio/servicos/categoria/cultura/10602830449563/1746"},
    {"Categoria": "Cultura", "Serviço": "Bibliotecas públicas municipais", "URL": "https://pref.rio/servicos/categoria/cultura/10602786909595/1746"},

    # Emergência
    {"Categoria": "Emergência", "Serviço": "Vistoria em imóvel com rachadura e infiltração", "URL": "https://pref.rio/servicos/categoria/emergencia/10421754087707/1746"},
    {"Categoria": "Emergência", "Serviço": "Vistoria em ameaça de desabamento de estrutura", "URL": "https://pref.rio/servicos/categoria/emergencia/10421554350619/1746"},
    {"Categoria": "Emergência", "Serviço": "Emissão de Cópia Autêntica (Vistoria da Defesa Civil)", "URL": "https://pref.rio/servicos/categoria/emergencia/78769/carioca-digital"},
    {"Categoria": "Emergência", "Serviço": "Vistoria em desabamento de estrutura", "URL": "https://pref.rio/servicos/categoria/emergencia/10421712339867/1746"},
    {"Categoria": "Emergência", "Serviço": "Vistoria em ameaça de deslizamento", "URL": "https://pref.rio/servicos/categoria/emergencia/10422149135003/1746"},
    {"Categoria": "Emergência", "Serviço": "Vistoria pós-incêndio", "URL": "https://pref.rio/servicos/categoria/emergencia/10421971980571/1746"},
    {"Categoria": "Emergência", "Serviço": "Vistoria em queda de muro de arrimo", "URL": "https://pref.rio/servicos/categoria/emergencia/10421807662107/1746"},
    {"Categoria": "Emergência", "Serviço": "Vistoria em deslizamento de encosta", "URL": "https://pref.rio/servicos/categoria/emergencia/10422188885019/1746"},
    {"Categoria": "Emergência", "Serviço": "Vistoria em queda de revestimento interno", "URL": "https://pref.rio/servicos/categoria/emergencia/10421965289499/1746"},
    {"Categoria": "Emergência", "Serviço": "Vistoria em ameaça de rolamento de pedra", "URL": "https://pref.rio/servicos/categoria/emergencia/80803/carioca-digital"},
    {"Categoria": "Emergência", "Serviço": "Vistoria em estrutura sinistrada por incêndio", "URL": "https://pref.rio/servicos/categoria/emergencia/80900/carioca-digital"},
    {"Categoria": "Emergência", "Serviço": "Vistoria em rolamento de pedra", "URL": "https://pref.rio/servicos/categoria/emergencia/10422242181531/1746"},
    {"Categoria": "Emergência", "Serviço": "Informações sobre auto de interdição", "URL": "https://pref.rio/servicos/categoria/emergencia/10422311262491/1746"},
    {"Categoria": "Emergência", "Serviço": "Informações sobre imóvel interditado em comunidade", "URL": "https://pref.rio/servicos/categoria/emergencia/10834639942555/1746"},
    {"Categoria": "Emergência", "Serviço": "Informações sobre participação da Defesa Civil", "URL": "https://pref.rio/servicos/categoria/emergencia/10421035612315/1746"},
    {"Categoria": "Emergência", "Serviço": "Informações sobre NUPDEC", "URL": "https://pref.rio/servicos/categoria/emergencia/35576129576347/1746"},
    {"Categoria": "Emergência", "Serviço": "Atendimento em Coordenação de Emergência Regional", "URL": "https://pref.rio/servicos/categoria/emergencia/10729741265179/1746"},
    {"Categoria": "Emergência", "Serviço": "Informações sobre incêndio no Parque Nacional", "URL": "https://pref.rio/servicos/categoria/emergencia/10821287077275/1746"},
    {"Categoria": "Emergência", "Serviço": "Informações sobre mensagens de alerta", "URL": "https://pref.rio/servicos/categoria/emergencia/10421078641307/1746"},

    # Trabalho
    {"Categoria": "Trabalho", "Serviço": "Informação sobre trabalho na MultiRio", "URL": "https://pref.rio/servicos/categoria/trabalho/75543/carioca-digital"},
    {"Categoria": "Trabalho", "Serviço": "Consulta e encaminhamento para vagas de emprego", "URL": "https://pref.rio/servicos/categoria/trabalho/70982/carioca-digital"},
    {"Categoria": "Trabalho", "Serviço": "Cartão Refeição Prato Feito Carioca", "URL": "https://pref.rio/servicos/categoria/trabalho/86866/carioca-digital"},
    {"Categoria": "Trabalho", "Serviço": "Carteira de Trabalho digital", "URL": "https://pref.rio/servicos/categoria/trabalho/70730/carioca-digital"},
    {"Categoria": "Trabalho", "Serviço": "Cursos gratuitos de tecnologia", "URL": "https://pref.rio/servicos/categoria/trabalho/89966/carioca-digital"},
    {"Categoria": "Trabalho", "Serviço": "Informações para empresas sobre PCD", "URL": "https://pref.rio/servicos/categoria/trabalho/10837066859291/1746"},
    {"Categoria": "Trabalho", "Serviço": "Informações sobre guia de turismo", "URL": "https://pref.rio/servicos/categoria/trabalho/10837094833307/1746"},
    {"Categoria": "Trabalho", "Serviço": "Inscrições para Cursos de Capacitação", "URL": "https://pref.rio/servicos/categoria/trabalho/10822636753563/1746"},
    {"Categoria": "Trabalho", "Serviço": "Informações sobre o CRIP", "URL": "https://pref.rio/servicos/categoria/trabalho/32872302095899/1746"},
    {"Categoria": "Trabalho", "Serviço": "Informações sobre empreendedorismo comunitário", "URL": "https://pref.rio/servicos/categoria/trabalho/10247029082523/1746"},
    {"Categoria": "Trabalho", "Serviço": "Informações sobre os Postos do Trabalhador", "URL": "https://pref.rio/servicos/categoria/trabalho/10836279005339/1746"},
    {"Categoria": "Trabalho", "Serviço": "Informações sobre inclusão de PCD", "URL": "https://pref.rio/servicos/categoria/trabalho/10836996886811/1746"},
    {"Categoria": "Trabalho", "Serviço": "Informações sobre o balcão de talentos", "URL": "https://pref.rio/servicos/categoria/trabalho/10733579762971/1746"},
    {"Categoria": "Trabalho", "Serviço": "Informações sobre estágio na Prefeitura", "URL": "https://pref.rio/servicos/categoria/trabalho/10837133841435/1746"},
    {"Categoria": "Trabalho", "Serviço": "Cursos voltados para pessoas com deficiência", "URL": "https://pref.rio/servicos/categoria/trabalho/10836130687131/1746"},
    {"Categoria": "Trabalho", "Serviço": "Informações sobre o programa Empreenda Rio", "URL": "https://pref.rio/servicos/categoria/trabalho/20815379193755/1746"},
    {"Categoria": "Trabalho", "Serviço": "Informações sobre o FORSOFT", "URL": "https://pref.rio/servicos/categoria/trabalho/10836181631003/1746"},
    {"Categoria": "Trabalho", "Serviço": "Informação sobre saque do PIS/PASEP", "URL": "https://pref.rio/servicos/categoria/trabalho/10834017208859/1746"},
    {"Categoria": "Trabalho", "Serviço": "Informações sobre cursos de qualificação", "URL": "https://pref.rio/servicos/categoria/trabalho/10836152220827/1746"},

    # Esportes
    {"Categoria": "Esportes", "Serviço": "Informações sobre atividades esportivas gratuitas", "URL": "https://pref.rio/servicos/categoria/esportes/10390775086363/1746"},
    {"Categoria": "Esportes", "Serviço": "Manutenção de ATI", "URL": "https://pref.rio/servicos/categoria/esportes/10391614994971/1746"},
    {"Categoria": "Esportes", "Serviço": "Esportes", "URL": "https://pref.rio/servicos/categoria/esportes/77811/carioca-digital"},
    {"Categoria": "Esportes", "Serviço": "Projetos esportivos - custeio", "URL": "https://pref.rio/servicos/categoria/esportes/10391618294299/1746"},
    {"Categoria": "Esportes", "Serviço": "Secretaria Municipal de Esportes", "URL": "https://pref.rio/servicos/categoria/esportes/72707/carioca-digital"},
    {"Categoria": "Esportes", "Serviço": "Instalação de ATI", "URL": "https://pref.rio/servicos/categoria/esportes/86836/carioca-digital"},
    {"Categoria": "Esportes", "Serviço": "Informações sobre Projeto Vida Ativa", "URL": "https://pref.rio/servicos/categoria/esportes/10391568912027/1746"},
    {"Categoria": "Esportes", "Serviço": "Subsecretaria de Esportes e Lazer", "URL": "https://pref.rio/servicos/categoria/esportes/10412600341275/1746"},
    {"Categoria": "Esportes", "Serviço": "Informações sobre quadras no Aterro", "URL": "https://pref.rio/servicos/categoria/esportes/10391459954331/1746"},
    {"Categoria": "Esportes", "Serviço": "Informações sobre material esportivo", "URL": "https://pref.rio/servicos/categoria/esportes/10391408871195/1746"},
    {"Categoria": "Esportes", "Serviço": "Eventos esportivos - patrocínio", "URL": "https://pref.rio/servicos/categoria/esportes/10387499197211/1746"},

    # Segurança
    {"Categoria": "Segurança", "Serviço": "Fiscalização de perturbação do sossego", "URL": "https://pref.rio/servicos/categoria/seguranca/10221320061979/1746"},
    {"Categoria": "Segurança", "Serviço": "Informações sobre prática irregular de esportes", "URL": "https://pref.rio/servicos/categoria/seguranca/10858508655387/1746"},
    {"Categoria": "Segurança", "Serviço": "Informações sobre câmeras de monitoramento", "URL": "https://pref.rio/servicos/categoria/seguranca/10872730317339/1746"},
    {"Categoria": "Segurança", "Serviço": "Informações sobre delitos em cemitério", "URL": "https://pref.rio/servicos/categoria/seguranca/10835235716891/1746"},
    {"Categoria": "Segurança", "Serviço": "Informações sobre assalto a turista", "URL": "https://pref.rio/servicos/categoria/seguranca/10420837594139/1746"},
    {"Categoria": "Segurança", "Serviço": "Informações sobre unidades da Guarda Municipal", "URL": "https://pref.rio/servicos/categoria/seguranca/10836768212507/1746"},
    {"Categoria": "Segurança", "Serviço": "Turista assaltado", "URL": "https://pref.rio/servicos/categoria/seguranca/78138/carioca-digital"}
]

def coletar_links(servicos: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Coleta os links finais de todos os serviços."""
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    resultado = []
    
    try:
        for s in servicos:
            link_final = get_link_final(driver, s["URL"], wait)
            resultado.append({
                "Categoria": s["Categoria"],
                "Serviço": s["Serviço"],
                "URL Serviço": s["URL"],
                "Link Final": link_final
            })
            print(f"Coletado: {s['Serviço']} -> {link_final}")
    finally:
        driver.quit()
    
    return resultado

def salvar_resultados(resultado: List[Dict[str, str]], nome_arquivo: str = "servicos_pref_rio_links.xlsx"):
    """Salva os resultados em um arquivo Excel."""
    df = pd.DataFrame(resultado)
    df.to_excel(nome_arquivo, index=False)
    print(f"Arquivo Excel '{nome_arquivo}' gerado com sucesso!")

def main():
    """Função principal do script."""
    # Cria diretório de saída se não existir
    os.makedirs("output", exist_ok=True)
    
    # Coleta os links
    resultado = coletar_links(servicos)
    
    # Salva os resultados
    salvar_resultados(resultado, "output/servicos_pref_rio_links.xlsx")

if __name__ == "__main__":
    main()
