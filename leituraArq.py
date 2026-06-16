import os

def ler_arquivo(nome_arquivo):

    # Resolve o caminho relativo à pasta deste arquivo, não ao diretório do terminal
    pasta = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta, nome_arquivo)

    with open(caminho, "r", encoding="utf-8") as arq:
        linhas = [linha.rstrip("\n") for linha in arq]

    estados = []
    estado_inicial = ""
    estados_iniciais = []
    estados_finais = []
    transicoes = {}
    palavras_teste = []

    lendo_palavras = False

    for linha in linhas:

        if linha.startswith("Q:"):
            estados = linha[2:].strip().split()

        elif linha.startswith("I:"):
            # Suporte a múltiplos estados iniciais (AFND)
            estados_iniciais = linha[2:].strip().split()
            estado_inicial = estados_iniciais[0] if len(estados_iniciais) == 1 else estados_iniciais[0]

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

                    # AFD: destino é string; AFND: destino é lista
                    if simbolo not in transicoes[origem]:
                        transicoes[origem][simbolo] = [destino]
                    else:
                        if isinstance(transicoes[origem][simbolo], list):
                            if destino not in transicoes[origem][simbolo]:
                                transicoes[origem][simbolo].append(destino)
                        else:
                            transicoes[origem][simbolo] = [transicoes[origem][simbolo], destino]

        else:
           
            palavras_teste.append(linha) #guardando linha vazia pra palavra vazia

    return {
        "estados": estados,
        "estado_inicial": estado_inicial,
        "estados_iniciais": estados_iniciais,
        "estados_finais": estados_finais,
        "transicoes": transicoes,
        "palavras_teste": palavras_teste
    }