from cores import *


def exibir_titulo():

    print()

    print(SEPARADOR + "╔" + "═" * 58 + "╗")
    print(TITULO + "║                       TP-FTC FINAL                       ║")
    print(SEPARADOR + "╚" + "═" * 58 + "╝")

    print(INFO + " Simulador de Autômatos - FTC")
    print()


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