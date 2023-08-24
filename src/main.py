import os; os.chdir(source_dir := os.path.dirname(os.path.abspath(__file__)))
import pandas as pd

from app.configurations import AppConfig
from app.loggers import AppLogger
from datetime import datetime

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from model.document import Cnpj
from services.functions import save_result

def main(config, logger):
    logger.info("Iniciando aplicação")

    input_file  = os.path.join(config.folder_paths.input, 'input.csv')
    output_file = os.path.join(config.folder_paths.output, 'result.xlsx')
    url = config.url

    logger.info("Fazendo leitura da planilha de Input")
    input_df = pd.read_csv(input_file)

    documents = []

    logger.info("Instanciando Driver de execução")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    wait   = WebDriverWait(driver, 10)

    logger.info("Iniciando extração dos dados...")
    logger.info("")
    for _, item in input_df.iterrows():
        logger.info(f"  Processando CNPJ {item.CNPJs}")
        try:
            driver.get(url)
            driver.find_element(By.XPATH, '//*[@id="captchaSonoro"]').click()

            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="cnpj"]')))
            element = driver.find_element(By.XPATH, '//*[@id="cnpj"]')
            script = f"""
                var element = arguments[0];
                var text = "{item.CNPJs}";
                element.value = text;
                element.dispatchEvent(new Event('input'));
            """
            driver.execute_script(script, element)

            # ------------------- Inserindo Captcha -------------------
            captcha = input("Preencha aqui o valor do Captcha informado no portal. \nCaso prefira sair e continuar com os dados já processados digite 0.\n")
            if captcha == '0':
                break
            driver.find_element(By.XPATH, '//*[@id="txtTexto_captcha_serpro_gov_br"]').send_keys(captcha)

            driver.find_element(By.XPATH, '//*[@id="frmConsulta"]/div[3]/div/button[1]').click()
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="principal"]')))
            main_table_xpath = '//*[@id="principal"]/table[1]/tbody/tr/td/'
            
            # ------------- Extraindo dados do documento -------------
            documents.append(Cnpj(
                data_abertura            = driver.find_element(By.XPATH, f'{main_table_xpath}table[2]/tbody/tr/td[3]/font[2]/b').text,
                nome_empresarial         = driver.find_element(By.XPATH, f'{main_table_xpath}table[3]/tbody/tr/td/font[2]/b').text,
                nome_estabelecimento     = driver.find_element(By.XPATH, f'{main_table_xpath}table[4]/tbody/tr/td[1]/font[2]/b').text,
                codigo_desc_principal    = driver.find_element(By.XPATH, f'{main_table_xpath}table[5]/tbody/tr/td/font[2]/b').text,
                codigo_desc_secundaria   = driver.find_element(By.XPATH, f'{main_table_xpath}table[6]/tbody/tr/td/font[2]/b').text,
                codigo_desc_natureza_jur = driver.find_element(By.XPATH, f'{main_table_xpath}table[7]/tbody/tr/td/font[2]/b').text,
                logradouro               = driver.find_element(By.XPATH, f'{main_table_xpath}table[8]/tbody/tr/td[1]/font[2]/b').text,
                numero                   = driver.find_element(By.XPATH, f'{main_table_xpath}table[8]/tbody/tr/td[3]/font[2]/b').text,
                complemento              = driver.find_element(By.XPATH, f'{main_table_xpath}table[8]/tbody/tr/td[5]/font[2]/b').text,
                cep                      = driver.find_element(By.XPATH, f'{main_table_xpath}table[9]/tbody/tr/td[1]/font[2]/b').text,
                ente_federativo          = driver.find_element(By.XPATH, f'{main_table_xpath}table[11]/tbody/tr/td/font[2]/b').text,
                situacao_cadastral       = driver.find_element(By.XPATH, f'{main_table_xpath}table[12]/tbody/tr/td[1]/font[2]/b').text,
                data_situacao_cadastral  = driver.find_element(By.XPATH, f'{main_table_xpath}table[12]/tbody/tr/td[3]/font[2]/b').text
            ))
        except Exception as e:
            logger.error("Falha na extração dos dados")
            logger.error(e)

    # ---------------------- Salvando resultados ----------------------
    save_result(documents, output_file)

if __name__ == '__main__':
    datepart = '_' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logger = AppLogger.setup(log_filename=f"../logs/log{datepart}")
    config = AppConfig.setup()

    try:
        main(config, logger)
    except Exception as e:
        logger.error('Ocorreu erro na automação')
        logger.error(e)


