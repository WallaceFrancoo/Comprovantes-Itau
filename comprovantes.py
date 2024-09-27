from PyPDF2 import PdfReader
import re
import parametros
# Funções de processamento para cada tipo de comprovante
def processar_comprovante_transferencia(texto_pagina):

    nome_recebedor = "Nome do recebedor não encontrado"
    data_transferencia = "Data da transferência não encontrada"
    valor_transferencia = "Valor não encontrado"

    # Procurar o nome do recebedor
    match_nome = re.search(r"nome do recebedor:\s*(.*?)\s*(chave:)", texto_pagina, re.DOTALL | re.IGNORECASE)
    if match_nome:
        nome_recebedor = match_nome.group(1).strip()

    else:
        match_nome = re.search(r"Nome:\s*(.*?)\s*(Agência:)", texto_pagina, re.DOTALL | re.IGNORECASE)
        if match_nome:
            nome_recebedor = match_nome.group(1).strip()
        else:
            match_nome = re.search(r"nome do recebedor:\s*(.*?)\s*(CPF / CNPJ do recebedor:)", texto_pagina, re.DOTALL | re.IGNORECASE)
            if match_nome:
                nome_recebedor = match_nome.group(1).strip()

    # Procurar a data da transferência
    match_data = re.search(r"data da transferência:\s*(.*?)\s*(tipo de pagamento:)", texto_pagina,
                           re.DOTALL | re.IGNORECASE)
    if match_data:
        data_transferencia = match_data.group(1).strip()
    else:
        match_data = re.search(r"Transferência efetuada em \s*(.*?)\s*( às)", texto_pagina, re.DOTALL | re.IGNORECASE)
        if match_data:
            data_transferencia = match_data.group(1).strip()

    # Procurar o valor
    match_valor = re.search(r"valor:\s*(.*?)\s*(data da transferência:)", texto_pagina, re.DOTALL | re.IGNORECASE)
    if match_valor:
        valor_transferencia = match_valor.group(1).strip()
    else:
        match_valor = re.search(r"Valor:\s*(.*?)\s*(Informações fornecidas)", texto_pagina, re.DOTALL | re.IGNORECASE)
        if match_valor:
            valor_transferencia = match_valor.group(1).strip()
    linhadolancamento = f"Data: {data_transferencia} | Valor: {valor_transferencia} | Recebedor: {nome_recebedor}"
    print(linhadolancamento)
    pass

def processar_comprovante_pagamento_tributos_municipais_1(texto_pagina):
    # Seu código para processar "Banco Itaú - Comprovante de Pagamento Tributos Municipais"
    nome_recebedor = "Nome do recebedor não encontrado"
    data_transferencia = "Data da transferência não encontrada"
    valor_transferencia = "Valor não encontrado"
    # Procurar nome
    match_nome = re.search(r"Identificação no extrato:\s*(.*?)\s*(Dados da conta)", texto_pagina, re.DOTALL | re.IGNORECASE)
    if match_nome:
        nome_recebedor = match_nome.group(1).strip()
    # Procurar a data da transferência
    match_data = re.search(r"Operação efetuada em\s*(.*?)\s*(às)", texto_pagina,
                           re.DOTALL | re.IGNORECASE)
    if match_data:
        data_transferencia = match_data.group(1).strip()
    # Procurar o valor
    match_valor = re.search(r"Valor do documento:\s*(.*?)\s*(Informações fornecidas)", texto_pagina, re.DOTALL | re.IGNORECASE)
    if match_valor:
        valor_transferencia = match_valor.group(1).strip()

    linhadolancamento = f"Data: {data_transferencia} | Valor: {valor_transferencia} | Recebedor: {nome_recebedor}"
    print(linhadolancamento)
    pass

def processar_comprovante_pagamento_boleto(texto_pagina):
    # Seu código para processar "Comprovante de pagamento de boleto"
    nome_recebedor = "Nome do recebedor não encontrado"
    data_transferencia = "Data da transferência não encontrada"
    valor_transferencia = "Valor não encontrado"

    # Procurar nome
    match_nome = re.search(r"Data de pagamento:\s+.*?\s+(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", texto_pagina, re.DOTALL)
    if match_nome:
        nome_recebedor = match_nome.group(1).strip()
    else:
        match_nome = re.search(r"Data de vencimento:\s+.*?\s+(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", texto_pagina, re.DOTALL)
        if match_nome:
            nome_recebedor = match_nome.group(1).strip()
    # Procurar a data da transferência
    match_data = re.search(r"Operação efetuada em\s*(.*?)\s*(às)", texto_pagina,
                           re.DOTALL | re.IGNORECASE)
    if match_data:
        data_transferencia = match_data.group(1).strip()

    # Procurar o valor Total
    primeira_ocorrencia = re.search(r"(" + re.escape(parametros.CNPJ) + r")", texto_pagina, re.DOTALL | re.IGNORECASE)
    if primeira_ocorrencia:
        # A posição onde a primeira ocorrência termina
        posicao_primeira = primeira_ocorrencia.end()
        # Buscar a segunda ocorrência a partir dessa posição
        segunda_ocorrencia = re.search(r"(" + re.escape(parametros.CNPJ) + r")\s*(.*?)\s*(Beneficiário Final:)",
                                       texto_pagina[posicao_primeira:], re.DOTALL | re.IGNORECASE)
        if segunda_ocorrencia:
            valor_transferencia = segunda_ocorrencia.group(2).strip()
        else:
            primeira_ocorrencia = re.search(r"(" + re.escape(parametros.CNPJ) + r")", texto_pagina,
                                            re.DOTALL | re.IGNORECASE)
            if primeira_ocorrencia:
                # A posição onde a primeira ocorrência termina
                posicao_primeira = primeira_ocorrencia.end()
                # Buscar a segunda ocorrência a partir dessa posição
                segunda_ocorrencia = re.search(r"(" + re.escape(parametros.CNPJ) + r")\s*(.*?)\s*(Data de pagamento:)",
                                               texto_pagina[posicao_primeira:], re.DOTALL | re.IGNORECASE)
                if segunda_ocorrencia:
                    valor_transferencia = segunda_ocorrencia.group(2).strip()
                else:
                    posicao_primeira = primeira_ocorrencia.end()
                    # Buscar a segunda ocorrência a partir dessa posição
                    segunda_ocorrencia = re.search(
                        r"(\d{3}\.\d{3}\.\d{3}-\d{2})\s*(.*?)\s*(Beneficiário Final:)",
                        texto_pagina[posicao_primeira:], re.DOTALL | re.IGNORECASE)
                    if segunda_ocorrencia:
                        valor_transferencia = segunda_ocorrencia.group(2).strip()
                        nome_recebedor = '6'
                    else:
                        posicao_primeira = primeira_ocorrencia.end()
                        # Buscar a segunda ocorrência a partir dessa posição
                        segunda_ocorrencia = re.search(
                            r"(\d{3}\.\d{3}\.\d{3}-\d{2})\s*(.*?)\s*(Data de pagamento:)",
                            texto_pagina[posicao_primeira:], re.DOTALL | re.IGNORECASE)
                        if segunda_ocorrencia:
                            valor_transferencia = segunda_ocorrencia.group(2).strip()
                            nome_recebedor = '6'


    linhadolancamento = f"Data: {data_transferencia} | Valor: {valor_transferencia} | Recebedor: {nome_recebedor}"
    print(linhadolancamento)
    pass

def processar_comprovante_pagamento_darf(texto_pagina):
    # Seu código para processar "Comprovante de pagamento - DARF"
    nome_recebedor = "DARF TRIBUTOS"
    data_transferencia = "Data da transferência não encontrada"
    valor_transferencia = "Valor não encontrado"
    # Procurar a data da transferência
    match_data = re.search(r"data do pagamento:\s*(.*?)\s*(número do documento:)", texto_pagina,
                           re.DOTALL | re.IGNORECASE)
    if match_data:
        data_transferencia = match_data.group(1).strip()
    # Procurar o valor
    match_valor = re.search(r"valor total:\s*(.*?)\s*(autenticação:)", texto_pagina,
                            re.DOTALL | re.IGNORECASE)
    if match_valor:
        valor_transferencia = match_valor.group(1).strip()

    linhadolancamento = f"Data: {data_transferencia} | Valor: {valor_transferencia} | Recebedor: {nome_recebedor}"
    print(linhadolancamento)
    pass
def processar_comprovante_pagamento_simples_nacional(texto_pagina):
    nome_recebedor = "SIMPLES NACIONAL"
    data_transferencia = "Data da transferência não encontrada"
    valor_transferencia = "Valor não encontrado"

    # Procurar a data da transferência
    match_data = re.search(r"data do pagamento:\s*(.*?)\s*(número do documento:)", texto_pagina,
                           re.DOTALL | re.IGNORECASE)
    if match_data:
        data_transferencia = match_data.group(1).strip()
    # Procurar o valor
    match_valor = re.search(r"valor total:\s*(.*?)\s*(autenticação:)", texto_pagina,
                                re.DOTALL | re.IGNORECASE)
    if match_valor:
        valor_transferencia = match_valor.group(1).strip()

    linhadolancamento = f"Data: {data_transferencia} | Valor: {valor_transferencia} | Recebedor: {nome_recebedor}"
    print(linhadolancamento)
    pass
def processar_comprovante_pagamento_qrcode(texto_pagina):
    # Seu código para processar "Comprovante de pagamento QR Code"
    nome_recebedor = "Nome do recebedor não encontrado"
    data_transferencia = "Data da transferência não encontrada"
    valor_transferencia = "Valor não encontrado"
    # Procurar nome
    match_nome = re.search(r"nome do recebedor:\s*(.*?)\s*(CPF / CNPJ do recebedor:)", texto_pagina,
                           re.DOTALL | re.IGNORECASE)
    if match_nome:
        nome_recebedor = match_nome.group(1).strip()

    # Procurar a data da transferência
    match_data = re.search(r"Pagamento efetuado em\s*(.*?)\s*(às)", texto_pagina,
                           re.DOTALL | re.IGNORECASE)
    if match_data:
        data_transferencia = match_data.group(1).strip()
    # Procurar o valor
    match_valor = re.search(r"valor da transação:\s*(.*?)\s*(mensagem do recebedor:)", texto_pagina,
                            re.DOTALL | re.IGNORECASE)
    if match_valor:
        valor_transferencia = match_valor.group(1).strip()
    else:
        match_valor = re.search(r"valor da transação:\s*(.*?)\s*(descrição:)", texto_pagina,
                                re.DOTALL | re.IGNORECASE)
        if match_valor:
            valor_transferencia = match_valor.group(1).strip()

    linhadolancamento = f"Data: {data_transferencia}  | Valor: {valor_transferencia} | Recebedor: {nome_recebedor}"
    print(linhadolancamento)
    pass

def verificar_pagina(texto_pagina):
    if "Comprovante de Transferência" in texto_pagina:
        processar_comprovante_transferencia(texto_pagina)
    elif "Banco Itaú - Comprovante de Pagamento" in texto_pagina:
        processar_comprovante_pagamento_tributos_municipais_1(texto_pagina)
    elif "Comprovante de pagamento de boleto" in texto_pagina:
        processar_comprovante_pagamento_boleto(texto_pagina)
    elif "Comprovante de pagamento - DARF" in texto_pagina:
        processar_comprovante_pagamento_darf(texto_pagina)
    elif "Comprovante de pagamento QR Code" in texto_pagina:
        processar_comprovante_pagamento_qrcode(texto_pagina)
    elif "Comprovante de pagamento - simples nacional" in texto_pagina:
        processar_comprovante_pagamento_simples_nacional(texto_pagina)
    else:
        print("Nenhum comprovante reconhecido nesta página.")
# Função para processar o arquivo PDF
def processar_arquivo_pdf(caminho_pdf):
    reader = PdfReader(caminho_pdf)
    for i, pagina in enumerate(reader.pages):
        texto_pagina = pagina.extract_text()
        print(f"Processando página {i+1}")
        verificar_pagina(texto_pagina)
# Exemplo de uso
caminho_pdf = "C:/UserS/Wallace/Pictures/848/espiritos08C.pdf"
processar_arquivo_pdf(caminho_pdf)

