from typing import List
from model.document import Cnpj
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

def get_cnpj_info(item, documents, driver, url, logger):
    wait = WebDriverWait(driver, 10)

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
        captcha = input("   Preencha aqui o valor do Captcha informado no portal. \n   Caso prefira sair e continuar com os dados já processados digite 0.\n   ")
        if captcha == '0':
            return documents, False
        driver.find_element(By.XPATH, '//*[@id="txtTexto_captcha_serpro_gov_br"]').send_keys(captcha)
        driver.find_element(By.XPATH, '//*[@id="frmConsulta"]/div[3]/div/button[1]').click()
        
        # --------------- Capturar falha de servidor. ---------------
        if driver.find_elements(By.XPATH, '/html/body/table/tbody/tr[2]/td/input'):
            logger.error("   Server Error - 404")
            return documents, True

        # ------------- Extraindo dados do documento -------------
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="principal"]')))
        main_table_xpath = '//*[@id="principal"]/table[1]/tbody/tr/td/'
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
        return documents, True
    
    except Exception as e:
        logger.error("Falha na extração dos dados")
        logger.error(e)
        return documents, False 

def save_result(documents: List[Cnpj], file_path) -> bool:
    data_dict_list = []
    for document in documents:
        data_dict_list.append({
            "Data Abertura": document.data_abertura,
            "Nome Empresarial": document.nome_empresarial,
            "Nome Estabelecimento": document.nome_estabelecimento,
            "Código Desc. Principal": document.codigo_desc_principal,
            "Código Desc. Secundária": document.codigo_desc_secundaria,
            "Código Desc. Natureza Jurídica": document.codigo_desc_natureza_jur,
            "Logradouro": document.logradouro,
            "Número": document.numero,
            "Complemento": document.complemento,
            "CEP": document.cep,
            "Ente Federativo": document.ente_federativo,
            "Situação Cadastral": document.situacao_cadastral,
            "Data Situação Cadastral": document.data_situacao_cadastral
        })

    df = pd.DataFrame(data_dict_list)
    df.to_excel(file_path, index=False)