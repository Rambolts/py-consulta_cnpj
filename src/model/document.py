from pydantic import BaseModel

class Cnpj(BaseModel):
    """
    Classe CNPJ
    
    Garante a estrutura e os formatos em diversos quadros, desde planilhas a banco de dados.
    (Com mais tempo trataria os tipos com mais cuidado)
    """
    data_abertura            : str = None
    nome_empresarial         : str = None
    nome_estabelecimento     : str = None
    codigo_desc_principal    : str = None
    codigo_desc_secundaria   : str = None
    codigo_desc_natureza_jur : str = None
    logradouro               : str = None
    numero                   : str = None
    complemento              : str = None
    cep                      : str = None
    ente_federativo          : str = None
    situacao_cadastral       : str = None
    data_situacao_cadastral  : str = None