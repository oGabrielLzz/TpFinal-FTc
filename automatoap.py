import os
from collections import deque
from grafico import gerar_imagem_ap

try:
    from cores import *
except Exception:
    SEPARADOR = TITULO = INFO = DESTAQUE = NEON_AMARELO = NEON_BRANCO = NEON_AZUL = ""
    NEON_VERDE = NEON_VERMELHO = NEON_CIANO = PALAVRA = CAMINHO = OK = ERRO = ESTATISTICA = ""


def _caminho_arquivo(nome_arquivo):
    pasta = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pasta, nome_arquivo)


def ler_arquivo_ap(nome_arquivo="entrada_ap.txt"):
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
        "estados": estados,
        "alfabeto_pilha": alfabeto_pilha,
        "estado_inicial": estado_inicial,
        "estados_finais": estados_finais,
        "transicoes": transicoes,
        "palavras_teste": palavras_teste
    }


def simular_palavra_apn(palavra, dados, limite_passos=10000):
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


def executar_apn(dados):
    print()
    print(SEPARADOR + "╔" + "═" * 58 + "╗")
    print(TITULO + "║                    SIMULAÇÃO DO APN                      ║")
    print(SEPARADOR + "╚" + "═" * 58 + "╝")
    print()

    aceitas = 0
    rejeitadas = 0

    for palavra in dados["palavras_teste"]:
        aceita, caminho = simular_palavra_apn(palavra, dados)
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
            gerar_imagem_ap(dados, nome_arquivo="automato_apn", tipo="APN")
        elif opcao == "0":
            break
        else:
            print(ERRO + "\nOpção inválida!\n")


def simular_palavra_apd(palavra, dados, limite_passos=10000):
    estado_inicial = dados["estado_inicial"]
    transicoes = dados["transicoes"]
    estados_finais = dados["estados_finais"]

    estado_atual = estado_inicial
    pilha = ()
    index = 0
    caminho = [(estado_atual, list(pilha))]
    visitados = set()

    passos = 0
    while passos < limite_passos:
        passos += 1

        # reconhecimento: palavra lida completamente e pilha vazia
        if index == len(palavra) and len(pilha) == 0:
            return True, caminho, None

        # evitar loops infinitos de transições lambda
        config = (estado_atual, pilha, index)
        if config in visitados:
            return False, caminho, "Loop infinito de transições lambda detectado."
        visitados.add(config)

        char = palavra[index] if index < len(palavra) else None
        top = pilha[0] if len(pilha) > 0 else None

        transicoes_estado = transicoes.get(estado_atual, [])
        aplicaveis = []

        for t in transicoes_estado:
            # 1. entrada cond
            if t["a"] == "\\":
                cond_a = True
            else:
                cond_a = (char is not None and t["a"] == char)

            # 2. pilha cond
            if t["b"] == "\\":
                cond_b = True
            else:
                cond_b = (top is not None and t["b"] == top)

            if cond_a and cond_b:
                aplicaveis.append(t)

        if not aplicaveis:
            break

        # se houver mais de uma transição possivel, ha um conflito de nao-determinismo
        if len(aplicaveis) > 1:
            detalhe = ", ".join([f"({t['a']},{t['b']}/{t['z']} -> {t['destino']})" for t in aplicaveis])
            return False, caminho, f"Conflito de não-determinismo (múltiplas transições aplicáveis): {detalhe}"

        escolhida = aplicaveis[0]
        destino = escolhida["destino"]
        a = escolhida["a"]
        b = escolhida["b"]
        z = escolhida["z"]

        # consome entrada se não for lambda
        if a != "\\":
            index += 1

        # desempilha se não for lambda
        if b != "\\":
            pilha = pilha[1:]

        # empilha se não for lambda
        if z != "\\":
            pilha = tuple(z) + pilha

        estado_atual = destino
        caminho.append((estado_atual, list(pilha)))

    # verificao de aceitacao final
    aceita = (index == len(palavra) and len(pilha) == 0)
    return aceita, caminho, None


def executar_apd(dados):
    print()
    print(SEPARADOR + "╔" + "═" * 58 + "╗")
    print(TITULO + "║                     SIMULAÇÃO DO APD                     ║")
    print(SEPARADOR + "╚" + "═" * 58 + "╝")
    print()

    aceitas = 0
    rejeitadas = 0

    for palavra in dados["palavras_teste"]:
        aceita, caminho, erro_conflito = simular_palavra_apd(palavra, dados)
        print(SEPARADOR + "─" * 60)
        if palavra == "":
            print(PALAVRA + "Palavra: λ (vazia)")
        else:
            print(PALAVRA + f"Palavra: {palavra}")

        path_str = " -> ".join([f"{state}{stack}" for state, stack in caminho])
        print(CAMINHO + "Caminho: " + path_str)

        if erro_conflito:
            print(ERRO + f"Resultado: X (Erro: {erro_conflito})")
            rejeitadas += 1
        elif aceita:
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
            gerar_imagem_ap(dados, nome_arquivo="automato_apd", tipo="APD")
        elif opcao == "0":
            break
        else:
            print(ERRO + "\nOpção inválida!\n")
