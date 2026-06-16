from cores import *
from grafico import gerar_imagem

def aceita_palavra(palavra, dados):

    estado_atual = dados["estado_inicial"]

    caminho = [estado_atual]

    for simbolo in palavra:

        destino = dados["transicoes"][estado_atual][simbolo]

        # Suporte ao novo formato de leitura: destino pode ser lista (AFND) ou string (legado)
        if isinstance(destino, list):
            estado_atual = destino[0]
        else:
            estado_atual = destino

        caminho.append(estado_atual)

    aceita = estado_atual in dados["estados_finais"]

    return aceita, caminho


def executar_afd(dados):

    print()

    print(SEPARADOR + "╔" + "═" * 58 + "╗")
    print(TITULO + "║                     SIMULAÇÃO DO AFD                     ║")
    print(SEPARADOR + "╚" + "═" * 58 + "╝")

    print()

    aceitas = 0
    rejeitadas = 0

    for palavra in dados["palavras_teste"]:

        aceita, caminho = aceita_palavra(palavra, dados)

        print(SEPARADOR + "─" * 60)

        if palavra == "":
            print(PALAVRA + "Palavra: λ (vazia)")
        else:
            print(PALAVRA + f"Palavra: {palavra}")

        print(CAMINHO + "Caminho: " + " -> ".join(caminho))

        if aceita:
            print(OK + "Resultado: OK")
            aceitas += 1
        else:
            print(ERRO + "Resultado: X")
            rejeitadas += 1

        print()

    print(SEPARADOR + "═" * 60)

    print(ESTATISTICA + "ESTATÍSTICAS")

    print(SEPARADOR + "═" * 60)

    print(NEON_VERDE + f"Aceitas: {aceitas}")
    print(NEON_VERMELHO + f"Rejeitadas: {rejeitadas}")
    print(NEON_CIANO + f"Total: {aceitas + rejeitadas}")

    if (aceitas + rejeitadas) > 0:

        taxa = (aceitas / (aceitas + rejeitadas)) * 100

        print(
            NEON_AMARELO +
            f"Taxa de aceitação: {taxa:.2f}%"
        )

    print()

    while True:

     print(SEPARADOR + "═" * 60)
     print(DESTAQUE + "[1] Gerar imagem do autômato")
     print(DESTAQUE + "[0] Voltar ao menu principal")
     print(SEPARADOR + "═" * 60)

     opcao = input(INFO + "Escolha uma opção: ")

     if opcao == "1":

        gerar_imagem(dados, nome_arquivo="automato_afd", tipo="AFD")

     elif opcao == "0":

        break

     else:

        print(ERRO + "\nOpção inválida!\n")