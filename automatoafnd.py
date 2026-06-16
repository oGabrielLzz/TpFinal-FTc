from cores import *
from grafico import gerar_imagem


def fechamento_lambda(estados, transicoes):
    """Calcula o fechamento-λ (epsilon-closure) de um conjunto de estados."""

    fechamento = set(estados)
    pilha = list(estados)

    while pilha:

        estado = pilha.pop()

        destinos = transicoes.get(estado, {}).get("\\", [])

        for destino in destinos:

            if destino not in fechamento:
                fechamento.add(destino)
                pilha.append(destino)

    return fechamento


def aceita_palavra(palavra, dados):

    estados_iniciais = dados["estados_iniciais"]
    transicoes = dados["transicoes"]
    estados_finais = dados["estados_finais"]

    estados_atuais = fechamento_lambda(estados_iniciais, transicoes)

    caminho = ["{" + ", ".join(sorted(estados_atuais)) + "}"]

    for simbolo in palavra:

        proximos_estados = set()

        for estado in estados_atuais:

            destinos = transicoes.get(estado, {}).get(simbolo, [])

            for destino in destinos:
                proximos_estados.add(destino)

        estados_atuais = fechamento_lambda(proximos_estados, transicoes)

        caminho.append("{" + ", ".join(sorted(estados_atuais)) + "}")

    aceita = any(estado in estados_finais for estado in estados_atuais)

    return aceita, caminho


def executar_afnd(dados):

    print()

    print(SEPARADOR + "╔" + "═" * 58 + "╗")
    print(TITULO + "║                     SIMULAÇÃO DO AFND                    ║")
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

        gerar_imagem(dados, nome_arquivo="automato_afnd", tipo="AFND")

     elif opcao == "0":

        break

     else:

        print(ERRO + "\nOpção inválida!\n")