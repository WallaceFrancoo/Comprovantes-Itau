import PyPDF2
import re

# Lista de termos irrelevantes que devem ser removidos
termos_irrelevantes = [
    "G = aplicação programada",
    "P = poupança automática",
    "Para demais siglas, consulte as Notas",
    "Explicativas no final do extrato",
    "> Menu Conta Corrente > Extrato",
    "Explicativas no",
    "Este material está disponível na Internet  Mensal",
    "final do",
    "D = débito a compensar",
    "extrato"
]

# Função para remover os termos irrelevantes
def limpar_texto(texto):
    for termo in termos_irrelevantes:
        texto = texto.replace(termo, "")
    return texto.strip()
def remover_ultima_linha(output_txt_path):
    # Lê todas as linhas do arquivo
    with open(output_txt_path, "r", encoding="utf-8") as file:
        linhas = file.readlines()

    # Remove a última linha
    if linhas:
        linhas = linhas[:-1]  # Remove a última linha

    # Reescreve o arquivo sem a última linha
    with open(output_txt_path, "w", encoding="utf-8") as file:
        file.writelines(linhas)
def extrair_eventos_itau(pdf_path, output_txt_path):
    eventos_diarios = []
    data_atual = None
    evento_atual = []
    processar_linhas = False  # Flag para iniciar e parar o processamento
    ignorar_proxima_linha = False  # Flag para ignorar a próxima linha
    ignorar_linha_anterior = False  # Flag para ignorar a linha anterior até "(débitos)"
    ultima_linha = None  # Armazena a última linha processada
    ultima_linha_com_valor = None  # Variável para armazenar a última linha com valor

    # Regex para identificar valores e datas
    regex_valor = r'^-?\d{1,3}(?:\.\d{3})*(?:,\d{2})?$'
    regex_data = r'(?<!\d)\b\d{2}/\d{2}\b(?!\d)'
    # Regex para identificar linhas que precisam ser ignoradas
    regex_ignorar_linha = r'^\d{6}\s+\w{5}\s+\d{2}/\d{2}/\d{4}\s+\w+\s+\w+\s+\w+$'

    # Variável para indicar se o último valor processado foi negativo
    def validar_data(data):
        dia, mes = map(int, data.split('/'))
        if 1 <= dia <= 31 and 1 <= mes <= 12:
            return True
        return False
    # Abrir o arquivo PDF
    with open(pdf_path, "rb") as file:
        # Criar um leitor de PDF
        reader = PyPDF2.PdfReader(file)
        # Abrir o arquivo de texto para escrita
        with open(output_txt_path, "w", encoding="utf-8") as output_file:
            # Percorrer todas as páginas do PDF
            for page_num in range(len(reader.pages)):
                # Extrair o texto da página atual
                page = reader.pages[page_num]
                texto = page.extract_text()
                if texto:
                    # Dividir o texto por linhas
                    linhas = texto.split('\n')
                    for linha in linhas:
                        # Verifica se a linha contém o início da seção a ser processada
                        if "C = crédito a compensar" in linha:
                            print("Iniciando processamento de linhas a partir desta linha:")
                            processar_linhas = True  # Iniciar o processamento
                            continue
                        elif "Saldo em C/C" in linha:
                            print("Finalizando processamento de linhas.")
                            # Remover a última linha adicionada
                            if evento_atual:
                                evento_atual.pop()  # Remove a última linha da lista de eventos
                            processar_linhas = False  # Parar o processamento
                            break
                        if processar_linhas:
                            # Remove os termos irrelevantes
                            linha = limpar_texto(linha)
                            # Verifica se a linha contém uma data
                            match_data = re.search(regex_data, linha)
                            if re.match(regex_ignorar_linha, linha):
                                print(f"Ignorando linha: {linha}")
                                continue  # Ignora a linha atual
                            # Se uma nova data é encontrada, ela é definida como data_atual
                                # Se uma nova data é encontrada, ela é definida como data_atual
                            if match_data:
                                data_encontrada = match_data.group(0)
                                if validar_data(data_encontrada):
                                    data_atual = data_encontrada
                                    print(f"Data encontrada e atualizada: {data_atual}")
                                    continue  # Pular para a próxima linha
                            # Se a linha contém "SALDO APLIC AUT MAIS", ignora a linha
                            if "SALDO APLIC AUT MAIS" in linha:
                                print(f"Ignorando a linha atual: {linha}")
                                ignorar_proxima_linha = True  # Ignorar a próxima linha
                                continue  # Continua o processamento
                            # Ignorar a próxima linha após "SALDO APLIC AUT MAIS"
                            if ignorar_proxima_linha:
                                print(f"Ignorando a linha: {linha}")
                                ignorar_proxima_linha = False  # Reseta a flag
                                continue  # Ignora a linha atual
                            # Se a linha contém "mensal", remove a última linha e ignora até encontrar "(débitos)"
                            if "mensal" in linha:
                                if evento_atual and ultima_linha:
                                    evento_atual.pop()  # Remove a última linha adicionada
                                ignorar_linha_anterior = True  # Ativa a flag para ignorar até encontrar "(débitos)"
                                continue  # Ignora a linha atual
                            # Se a linha contém "(débitos)", desativa a flag de ignorar
                            if "(débitos)" in linha:
                                ignorar_linha_anterior = False
                                print("Reiniciando a captura de eventos.")
                                continue  # Ignora a linha atual
                            # Ignorar linhas se a flag ignorar_linha_anterior estiver ativa
                            if ignorar_linha_anterior:
                                print(f"Ignorando linha devido a 'mensal': {linha}")
                                continue  # Ignora a linha atual enquanto está ignorando
                            # Adiciona a linha aos eventos do dia atual, se não estiver vazia
                            if linha:
                                # Se não há data atual, continuar para a próxima linha
                                if not data_atual:
                                    print(f"Sem data definida, pulando linha: {linha}")
                                    continue
                                # Verifica se a linha contém um sinal de menos isolado
                                if linha == "-":
                                    print(f"Ignorando linha isolada com '-': {linha}")
                                    continue  # Ignora essa linha e passa para a próxima
                                # Verifica se a linha atual é um valor
                                if re.search(regex_valor, linha):
                                    # Se a última linha também for um valor, ignora a linha atual
                                    if ultima_linha and re.search(regex_valor, ultima_linha):
                                            # Ignora o valor se a última linha foi um valor positivo
                                            print(f"Ignorando a linha atual (valor após outro valor): {linha}")
                                            continue
                                    else:
                                        if ultima_linha_com_valor and ultima_linha_com_valor.endswith('-'):
                                            # Se a última linha tinha um traço, essa linha é ignorada
                                            print(f"Ignorando a linha atual (valor após outro valor com '-'): {linha}")
                                            ultima_linha_com_valor = None  # Reseta após ignorar a linha
                                            continue
                                        else:
                                            # Adiciona a linha atual, mantendo a data se válida
                                            linha_completa = f"{data_atual + ' ' if data_atual else ''}{linha}"
                                            print(f"Linha adicionada com valor: {linha_completa}")
                                            evento_atual.append(linha_completa)
                                            output_file.write(linha_completa + '\n')
                                else:
                                    # Verifica se a linha é uma descrição (não um valor)
                                    if "TRANSF" in linha or "PIX" in linha:  # Adicione outras palavras-chave conforme necessário
                                        # Adiciona a linha de descrição
                                        linha_completa = f"{data_atual + ' ' if data_atual else ''}{linha}"
                                        print(f"Linha adicionada como descrição: {linha_completa}")
                                        evento_atual.append(linha_completa)
                                        output_file.write(linha_completa + '\n')
                                    elif data_atual and re.search(regex_data, linha):
                                        # Retira a data da linha e a mantém
                                        linha_completa = f"{data_atual + ' ' if data_atual else ''}{linha}"
                                        print(f"Linha adicionada: {linha_completa}")
                                        evento_atual.append(linha_completa)
                                        output_file.write(linha_completa + '\n')
                                    else:
                                        # Caso não tenha uma data, apenas adiciona a linha normal
                                        linha_completa = f"{data_atual + ' ' if data_atual else ''}{linha}"
                                        print(f"Linha adicionada: {linha_completa}")
                                        evento_atual.append(linha_completa)
                                        output_file.write(linha_completa + '\n')
                            # Atualiza a última linha processada
                            ultima_linha = linha
                            ultima_linha_com_valor = linha
                # Após processar todas as linhas, verifica se ainda há eventos pendentes
                if evento_atual and data_atual:
                    eventos_diarios.append({'Data': data_atual, 'Eventos': evento_atual})
    return eventos_diarios
# Caminho para o arquivo PDF do extrato e arquivo TXT de saída
pdf_path = "C:/Users/Wallace/Pictures/848/formigas.pdf"
output_txt_path = "C:/Users/Wallace/Pictures/848/formigas.txt"

# Extrair eventos por dia
eventos = extrair_eventos_itau(pdf_path, output_txt_path)
#remover_ultima_linha(output_txt_path)


