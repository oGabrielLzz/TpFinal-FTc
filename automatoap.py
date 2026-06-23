import os
from collections import deque
from grafico import gerar_imagem_ap
from leituraArq import identificar_tipo

try:
    from cores import *
except Exception:
    SEPARADOR = TITULO = INFO = DESTAQUE = NEON_AMARELO = NEON_BRANCO = NEON_AZUL = ""
    NEON_VERDE = NEON_VERMELHO = NEON_CIANO = PALAVRA = CAMINHO = OK = ERRO = ESTATISTICA = ""


def _caminho_arquivo(nome_arquivo):
    pasta = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pasta, nome_arquivo)


def ler_arquivo_ap(nome_arquivo):
    tipo_automato = identificar_tipo(nome_arquivo)

    with open(_caminho_arquivo(nome_arquivo), "r", encoding="utf-8") as arq:
        linhas = [linha.rstrip("\n") for linha in arq]

    estados = []
    alfabeto_pilha = []
    estado_inicial = ""
    estados_finais = []
    transicoes = {}
    palavras_teste = []
    lendo_palavras = False

    for linha in linhas:
        linha_strip = linha.strip()
        if not linha_strip:
            continue
        if linha_strip == "---":
            lendo_palavras = True
            continue

        if not lendo_palavras:
            if linha_strip.startswith("Q:"):
                estados = linha_strip[2:].strip().split()
            elif linha_strip.startswith("G:"):
                conteudo = linha_strip[2:].strip()
                if " " in conteudo:
                    alfabeto_pilha = [c for c in conteudo.split() if c]
                else:
                    alfabeto_pilha = list(conteudo)
            elif linha_strip.startswith("I:"):
                estado_inicial = linha_strip[2:].strip().split()[0]
            elif linha_strip.startswith("F:"):
                estados_finais = linha_strip[2:].strip().split()
            elif "->" in linha_strip and "|" in linha_strip:
                esquerda, direita = linha_strip.split("|", 1)
                origem_destino = esquerda.split("->", 1)
                origem = origem_destino[0].strip()
                destino = origem_destino[1].strip()

                transicoes.setdefault(origem, [])
                regras = direita.strip().split()
                for regra in regras:
                    if "/" not in regra or "," not in regra:
                        continue
                    parte_lida, z = regra.split("/", 1)
                    a, b = parte_lida.split(",", 1)
                    transicoes[origem].append({
                        "destino": destino,
                        "a": a,
                        "b": b,
                        "z": z
                    })
        else:
            palavras_teste.append(linha_strip)

    return {
        "tipo_automato": tipo_automato,
        "estados": estados,
        "alfabeto_pilha": alfabeto_pilha,
        "estado_inicial": estado_inicial,
        "estados_finais": estados_finais,
        "transicoes": transicoes,
        "palavras_teste": palavras_teste
    }


def simular_palavra(palavra, dados, limite_passos=10000):
    estado_inicial = dados["estado_inicial"]
    transicoes = dados["transicoes"]

    # fila BFS: (estado atual, tupla da pilha, indice leitura, caminho percorrido) - testa caminhos
    queue = deque([(estado_inicial, (), 0, [(estado_inicial, [])])])
    visitados = set()

    melhor_caminho = [(estado_inicial, [])]
    max_index = 0

    passos = 0
    while queue and passos < limite_passos:
        passos += 1
        estado, pilha, index, caminho = queue.popleft()

        # reconhecimento: palavra lida completamente e pilha vazia
        if index == len(palavra) and len(pilha) == 0:
            return True, caminho

        # salva ate onde conseguiu ir pra mostrar na tela caso de erro
        if index > max_index:
            max_index = index
            melhor_caminho = caminho
        elif index == max_index and len(caminho) > len(melhor_caminho):
            melhor_caminho = caminho

        config = (estado, pilha, index)
        if config in visitados:
            continue
        visitados.add(config)

        # se nao tiver transicao pra esse estado, retorna vazio
        transicoes_estado = transicoes.get(estado, [])

        for t in transicoes_estado:
            a = t["a"]
            b = t["b"]
            z = t["z"]
            destino = t["destino"]

            # 1. leitura do simbolo de entrada
            if a == "\\":
                proximo_index = index
            else:
                if index < len(palavra) and palavra[index] == a:
                    proximo_index = index + 1
                else:
                    continue

            # 2. o que desempilha
            if b == "\\":
                pilha_apos_desempilhar = pilha
            else:
                if len(pilha) > 0 and pilha[0] == b:
                    pilha_apos_desempilhar = pilha[1:]
                else:
                    continue

            # 3. o que empilha (z)
            if z == "\\":
                nova_pilha = pilha_apos_desempilhar
            else:
                nova_pilha = tuple(z) + pilha_apos_desempilhar

            novo_caminho = caminho + [(destino, list(nova_pilha))]
            queue.append((destino, nova_pilha, proximo_index, novo_caminho))

    return False, melhor_caminho


def executar_ap(dados):
    print()
    print(SEPARADOR + "╔" + "═" * 58 + "╗")
    print(TITULO + "║                     SIMULAÇÃO DO AP                      ║")
    print(SEPARADOR + "╚" + "═" * 58 + "╝")
    print()

    aceitas = 0
    rejeitadas = 0

    for palavra in dados["palavras_teste"]:
        aceita, caminho = simular_palavra(palavra, dados)
        print(SEPARADOR + "─" * 60)
        if palavra == "":
            print(PALAVRA + "Palavra: λ (vazia)")
        else:
            print(PALAVRA + f"Palavra: {palavra}")

        path_str = " -> ".join([f"{state}{stack}" for state, stack in caminho])
        print(CAMINHO + "Caminho: " + path_str)

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
        print(NEON_AMARELO + f"Taxa de aceitação: {taxa:.2f}%")
    print()

    while True:
        print(SEPARADOR + "═" * 60)
        print(DESTAQUE + "[1] Gerar imagem do autômato")
        print(DESTAQUE + "[0] Voltar ao menu de extras")
        print(SEPARADOR + "═" * 60)

        opcao = input(INFO + "Escolha uma opção: ").strip()

        if opcao == "1":
            gerar_imagem_ap(dados, nome_arquivo="automato_ap", tipo="AP")
        elif opcao == "0":
            break
        else:
            print(ERRO + "\nOpção inválida!\n")
