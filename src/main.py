import os; os.chdir(source_dir := os.path.dirname(os.path.abspath(__file__)))
import pandas as pd

from app.configurations import AppConfig
from app.loggers import AppLogger
from datetime import datetime

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

from model.document import Cnpj
from services.functions import save_result, get_cnpj_info

def main(config, logger):
    logger.info("Iniciando aplicação")

    input_file  = os.path.join(config.folder_paths.input, 'input.csv')
    output_file = os.path.join(config.folder_paths.output, 'result.xlsx')
    url = config.url

    logger.info("Fazendo leitura da planilha de Input")
    input_df = pd.read_csv(input_file)

    logger.info("Instanciando Driver de execução")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    logger.info("Iniciando extração dos dados...")
    logger.info("")
    documents = []
    for _, item in input_df.iterrows():
        logger.info(f"  Processando CNPJ {item.CNPJs}")
        documents, continuar = get_cnpj_info(item, documents, driver, url, logger)
        if not continuar:
            break

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


