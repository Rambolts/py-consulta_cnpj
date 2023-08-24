from typing import List
from model.document import Cnpj
import pandas as pd

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