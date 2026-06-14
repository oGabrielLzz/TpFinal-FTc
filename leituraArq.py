def ler_arquivo(nome_arquivo):

    with open(nome_arquivo, "r", encoding="utf-8") as arq:
        linhas = [linha.rstrip("\n") for linha in arq]

    estados = []
    estado_inicial = ""
    estados_finais = []
    transicoes = {}
    palavras_teste = []

    lendo_palavras = False

    for linha in linhas:

        if linha.startswith("Q:"):
            estados = linha[2:].strip().split()

        elif linha.startswith("I:"):
            estado_inicial = linha[2:].strip()

        elif linha.startswith("F:"):
            estados_finais = linha[2:].strip().split()

        elif linha == "---":
            lendo_palavras = True

        elif not lendo_palavras:

            if "->" in linha and "|" in linha:

                esquerda, direita = linha.split("|")

                origem_destino = esquerda.split("->")

                origem = origem_destino[0].strip()
                destino = origem_destino[1].strip()

                simbolos = direita.strip().split()

                if origem not in transicoes:
                    transicoes[origem] = {}

                for simbolo in simbolos:
                    transicoes[origem][simbolo] = destino

        else:
           
            palavras_teste.append(linha) #guardando linha vazia pra palavra vazia

    return {
        "estados": estados,
        "estado_inicial": estado_inicial,
        "estados_finais": estados_finais,
        "transicoes": transicoes,
        "palavras_teste": palavras_teste
    }