from cores import *


def exibir_titulo():

    print()

    print(SEPARADOR + "╔" + "═" * 58 + "╗")
    print(TITULO + "║                       TP-FTC FINAL                       ║")
    print(SEPARADOR + "╚" + "═" * 58 + "╝")

    print(INFO + " Simulador de Autômatos - FTC")
    print()

def menu_modo_entrada():
    # define os modos de entrada que o usuário pode escolher para entrar
    exibir_titulo()

    print()
    print(DESTAQUE + "MODO DE ENTRADA")
    print(SEPARADOR + "─" * 30)

    print(NEON_AMARELO + "[1]" + NEON_BRANCO + " Usar arquivo de entrada predefinido")
    print(NEON_AMARELO + "[2]" + NEON_BRANCO + " Digitar o nome de um arquivo de entrada")
    print(NEON_AMARELO + "[0]" + NEON_BRANCO + " Sair")
 
    print()
 
    return input(DESTAQUE + "Escolha uma opção: ")

def menu_tipo_predefinido():
    # escolha de uso de arquivos predefinidos nas máquinas

    print()

    print(SEPARADOR + "╔" + "═" * 58 + "╗")
    print(TITULO + "║                TIPO DE AUTÔMATO (PREDEFINIDO)            ║")
    print(SEPARADOR + "╚" + "═" * 58 + "╝")
 
    print()
 
    print(NEON_AZUL + "[1]" + NEON_BRANCO + " AFD (Autômato Finito Determinístico)")
    print(NEON_AZUL + "[2]" + NEON_BRANCO + " AFN (Autômato Finito Não Determinístico)")
    print(NEON_AZUL + "[3]" + NEON_BRANCO + " Autômato de Pilha")
    print(NEON_AZUL + "[4]" + NEON_BRANCO + " Máquina de Turing / ALL")
    print(NEON_AZUL + "[0]" + NEON_BRANCO + " Voltar")
 
    print()
 
    return input(DESTAQUE + "Escolha uma opção: ")

def pedir_nome_arquivo():
    print()
    print(SEPARADOR + "─" * 60)
    print(INFO + "O arquivo deve estar na mesma pasta do projeto e conter, ")
    print(INFO + "na primeira linha, o tipo do autômato (ex.: @AF, @AFN, @AP, @MT, @ALL).")
    print(SEPARADOR + "─" * 60)
 
    return input(DESTAQUE + "Digite o nome do arquivo (ex.: entrada.txt): ").strip()



def menu_principal():

    exibir_titulo()

    print(DESTAQUE + "MENU PRINCIPAL")
    print(SEPARADOR + "─" * 30)

    print(NEON_AMARELO + "[1]" + NEON_BRANCO + " Simular AFD")
    print(NEON_AMARELO + "[2]" + NEON_BRANCO + " Extras")
    print(NEON_AMARELO + "[0]" + NEON_BRANCO + " Sair")

    print()

    return input(DESTAQUE + "Escolha uma opção: ")


def menu_extras():

    print()

    print(SEPARADOR + "╔" + "═" * 58 + "╗")
    print(TITULO + "║                          EXTRAS                          ║")
    print(SEPARADOR + "╚" + "═" * 58 + "╝")

    print()

    print(NEON_AZUL + "[1]" + NEON_BRANCO+ " AFN (Autômato Finito Não Determinístico)")
    print(NEON_AZUL + "[2]" + NEON_BRANCO + " Autômato de Pilha")
    print(NEON_AZUL + "[3]" + NEON_BRANCO + " Máquina de Turing")
    print(NEON_AZUL + "[0]" + NEON_BRANCO + " Voltar")

    print()

    return input(DESTAQUE + "Escolha uma opção: ")