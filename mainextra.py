import os
 
from interface import menu_modo_entrada, menu_tipo_predefinido, pedir_nome_arquivo
from leituraArq import ler_arquivo, identificar_tipo
from automatofd import executar_afd
from automatoafnd import executar_afnd
from automatoap import ler_arquivo_ap, executar_ap
from automatomt import ler_arquivo_mt, executar_mt

TIPOS = {
    "AF":  (ler_arquivo,    executar_afd),
    "AFD": (ler_arquivo,    executar_afd),
    "AFN": (ler_arquivo,    executar_afnd),
    "AFND": (ler_arquivo,   executar_afnd),
    "AP":  (ler_arquivo_ap, executar_ap),
    "MT":  (ler_arquivo_mt, executar_mt),
    "ALL": (ler_arquivo_mt, executar_mt),
}

ARQUIVOS_PREDEFINIDOS = {
    "1": "entrada.txt",
    "2": "entrada_afnd.txt",
    "3": "entrada_ap.txt",
    "4": "entrada_mt.txt",
}

def processar_arquivo(nome_arquivo):
    tipo = identificar_tipo(nome_arquivo)
 
    if tipo is None:
        print("\nO arquivo não possui a linha de cabeçalho @TIPO (ex.: @AF, @AFN, @AP, @MT, @ALL).\n")
        return
 
    if tipo not in TIPOS:
        print(f"\nTipo de autômato não suportado: {tipo}\n")
        return
 
    leitor, executor = TIPOS[tipo]
    dados = leitor(nome_arquivo)
    executor(dados)

def fluxo_predefinido():
    while True:
        opcao = menu_tipo_predefinido()
 
        if opcao == "0":
            break
 
        if opcao in ARQUIVOS_PREDEFINIDOS:
            nome_arquivo = ARQUIVOS_PREDEFINIDOS[opcao]
            try:
                processar_arquivo(nome_arquivo)
            except FileNotFoundError:
                print(f"\nArquivo '{nome_arquivo}' não encontrado na pasta do projeto.\n")
        else:
            print("\nOpção inválida.\n")

def fluxo_arquivo_digitado():
    nome_arquivo = pedir_nome_arquivo()
 
    if not nome_arquivo:
        print("\nNenhum nome de arquivo informado.\n")
        return
 
    try:
        processar_arquivo(nome_arquivo)
    except FileNotFoundError:
        print(f"\nArquivo '{nome_arquivo}' não encontrado.\n")

def main():
    while True:
        opcao = menu_modo_entrada()
 
        if opcao == "1":
            fluxo_predefinido() 
        elif opcao == "2":
            fluxo_arquivo_digitado() 
        elif opcao == "0":
            print("\nEncerrando programa...")
            break 
        else:
            print("\nOpção inválida.\n")

if __name__ == "__main__":
    main()
