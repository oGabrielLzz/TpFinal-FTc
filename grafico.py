import os
from graphviz import Digraph
from cores import *


def gerar_imagem(dados, nome_arquivo="automato", tipo="AFD"):

    dot = Digraph(name=tipo)

    dot.attr(rankdir="LR")                        # esquerda para direita
    dot.attr("graph", bgcolor="white")
    dot.attr("node", fontname="Helvetica")
    dot.attr("edge", fontname="Helvetica")

    estados_finais = set(dados["estados_finais"])
    transicoes     = dados["transicoes"]

    # Nó invisível para a seta de estado inicial
    dot.node("__inicio__", shape="none", label="")

    for estado in dados["estados"]:

        if estado in estados_finais:
            dot.node(estado, shape="doublecircle", style="filled",
                     fillcolor="#d0f0c0", color="#2e7d32")
        else:
            dot.node(estado, shape="circle", style="filled",
                     fillcolor="#e3f2fd", color="#1565c0")

    # Seta de entrada para o(s) estado(s) inicial(is)
    for estado_inicial in dados["estados_iniciais"]:
        dot.edge("__inicio__", estado_inicial, label="")

    # Agrupa rótulos de transições com mesmo par origem->destino
    # { (origem, destino): [simbolo1, simbolo2, ...] }
    arestas = {}

    for origem, simbolos_destinos in transicoes.items():
        for simbolo, destinos in simbolos_destinos.items():

            # destinos é sempre lista (formato novo do leituraArq)
            rotulo = "λ" if simbolo == "\\" else simbolo

            for destino in destinos:
                chave = (origem, destino)
                if chave not in arestas:
                    arestas[chave] = []
                arestas[chave].append(rotulo)

    for (origem, destino), rotulos in arestas.items():
        label = ", ".join(rotulos)
        dot.edge(origem, destino, label=label, color="#1565c0")

    # Salva na mesma pasta do script
    pasta = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta, nome_arquivo)

    dot.render(caminho, format="png", cleanup=True, view=True)

    print(INFO + f"\nImagem salva em: {caminho}.png\n")

def gerar_imagem_mt(dados, nome_arquivo="maquina_turing", tipo="MT"):
    dot = Digraph(name=tipo)

    dot.attr(rankdir="LR")
    dot.attr("graph", bgcolor="white")
    dot.attr("node", fontname="Helvetica")
    dot.attr("edge", fontname="Helvetica")

    estados_finais = set(dados["estados_finais"])
    transicoes = dados["transicoes"]

    dot.node("__inicio__", shape="none", label="")

    for estado in dados["estados"]:
        if estado in estados_finais:
            dot.node(
                estado,
                shape="doublecircle",
                style="filled",
                fillcolor="#d0f0c0",
                color="#2e7d32"
            )
        else:
            dot.node(
                estado,
                shape="circle",
                style="filled",
                fillcolor="#e3f2fd",
                color="#1565c0"
            )

    # Seta para o estado inicial da MT
    dot.edge("__inicio__", dados["estado_inicial"], label="")

    # Agrupa transições com mesmo par origem -> destino
    arestas = {}

    for origem, regras in transicoes.items():
        for simbolo_lido, acao in regras.items():
            destino, simbolo_escrito, direcao = acao

            lido = "□" if simbolo_lido == "_" else simbolo_lido
            escrito = "□" if simbolo_escrito == "_" else simbolo_escrito
            rotulo = f"{lido}/{escrito}{direcao}"

            chave = (origem, destino)

            if chave not in arestas:
                arestas[chave] = []

            arestas[chave].append(rotulo)

    for (origem, destino), rotulos in arestas.items():
        label = "\\n".join(rotulos)
        dot.edge(origem, destino, label=label, color="#1565c0")

    pasta = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta, nome_arquivo)

    dot.render(caminho, format="png", cleanup=True, view=True)

    print(INFO + f"\nImagem da {tipo} salva em: {caminho}.png\n")