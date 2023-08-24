# Consulta CNPJ

## Descrição
O projeto visa consultar e validar os dados dos cnpjs contidos na planilha input.csv

## Preparação do Ambiente
Será necessário fazer a instalação das bibliotecas.
Para isso está disponível um arquivo requirements.txt

Basta ativar seu ambiente virtual python e rodar o rodar o seguinte comando:

`pip install -r {caminho}\requirements.txt`

## Modo de execução
Ao executar a automação, basta chamar o arquivo main.py

`python {caminho}\main.py`

## Exceções e atualizações futuras
O processo ainda não passa pelo captcha automaticamente, para isso se faz necessário entrar manualmente, mesmo que pelo prompt de execução do processo.

Em alguns casos o site não consegue abrir o documento por falha na requisição. Atualmente o comportamento é ir para o próximo CNPJ dando continuidade ao processo.

## Finalização do processo

Caso queira finalizar o processo antecipadamente e mesmo assim obter o resultado dos itens já extraídos, basta entrar com o valor 0 quando solicitado.

Caso contrário o processo irá finalizar apenas quando consultar todos os itens da fila, ou caso retorne algum erro.