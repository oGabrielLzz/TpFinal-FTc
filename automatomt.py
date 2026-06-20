import os
from grafico import gerar_imagem_mt

try:
    from cores import *
except Exception:
    SEPARADOR = TITULO = INFO = DESTAQUE = NEON_AMARELO = NEON_BRANCO = NEON_AZUL = ""
    NEON_VERDE = NEON_VERMELHO = NEON_CIANO = PALAVRA = CAMINHO = OK = ERRO = ESTATISTICA = ""

BRANCO = "_"
LIM_ESQ = "<"
LIM_DIR = ">"
DIRECOES = {"E": -1, "D": 1}


def _caminho_arquivo(nome_arquivo):
    pasta = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pasta, nome_arquivo)


def _linha_alfabeto(linha):
    conteudo = linha[2:]
    if conteudo.startswith(" "):
        conteudo = conteudo[1:]
    return list(conteudo)


def ler_arquivo_mt(nome_arquivo="entrada_mt.txt"):
    with open(_caminho_arquivo(nome_arquivo), "r", encoding="utf-8") as arq:
        linhas = [linha.rstrip("\n") for linha in arq]

    modo = "MT"
    pos = 0
    if linhas and linhas[0].startswith("@"):
        modo = linhas[0][1:].strip().upper()
        pos = 1
        if modo not in {"MT", "ALL"}:
            raise ValueError("Tipo inválido para máquina de Turing. Use @MT ou @ALL.")

    estados = []
    alfabeto_entrada = ["0", "1"]
    alfabeto_fita_extra = []
    estado_inicial = ""
    estados_finais = []
    transicoes = {}
    palavras_teste = []
    lendo_palavras = False

    for linha in linhas[pos:]:
        if linha.startswith("Q:"):
            estados = linha[2:].strip().split()
        elif linha.startswith("S:"):
            alfabeto_entrada = _linha_alfabeto(linha)
        elif linha.startswith("G:"):
            alfabeto_fita_extra = _linha_alfabeto(linha)
        elif linha.startswith("I:"):
            estado_inicial = linha[2:].strip().split()[0]
        elif linha.startswith("F:"):
            estados_finais = linha[2:].strip().split()
        elif linha == "---":
            lendo_palavras = True
        elif not lendo_palavras:
            if not linha.strip():
                continue
            if "->" not in linha or "|" not in linha:
                continue

            esquerda, direita = linha.split("|", 1)
            origem_destino = esquerda.split("->", 1)
            origem = origem_destino[0].strip()
            destino = origem_destino[1].strip()

            transicoes.setdefault(origem, {})
            for regra in direita.strip().split():
                try:
                    lido, acao = regra.split("/", 1)
                    escrito = acao[:-1]
                    direcao = acao[-1]
                except ValueError as exc:
                    raise ValueError(f"Transição inválida: {regra}") from exc

                if len(lido) != 1 or len(escrito) != 1 or direcao not in DIRECOES:
                    raise ValueError(f"Transição inválida: {regra}. Use formato a/bD ou a/bE.")

                transicoes[origem][lido] = (destino, escrito, direcao)
        else:
            palavras_teste.append(linha)

    simbolos_proibidos = {BRANCO, LIM_ESQ, LIM_DIR}
    for simbolo in alfabeto_entrada + alfabeto_fita_extra:
        if simbolo in simbolos_proibidos:
            raise ValueError("Os símbolos _, < e > são reservados e não podem aparecer em S: ou G:.")

    return {
        "tipo": modo,
        "estados": estados,
        "alfabeto_entrada": alfabeto_entrada,
        "alfabeto_fita_extra": alfabeto_fita_extra,
        "estado_inicial": estado_inicial,
        "estados_finais": estados_finais,
        "transicoes": transicoes,
        "palavras_teste": palavras_teste,
    }


def _criar_fita(palavra, modo):
    if modo == "ALL":
        return list(LIM_ESQ + palavra + LIM_DIR), 1

    fita = {0: LIM_ESQ}
    for i, simbolo in enumerate(palavra, start=1):
        fita[i] = simbolo
    return fita, 1


def _ler_fita(fita, pos, modo):
    if modo == "ALL":
        if pos < 0 or pos >= len(fita):
            return None
        return fita[pos]
    return fita.get(pos, BRANCO)


def _escrever_fita(fita, pos, simbolo, modo):
    if modo == "ALL":
        if pos < 0 or pos >= len(fita):
            return False
        fita[pos] = simbolo
        return True
    fita[pos] = simbolo
    return True


def _conteudo_fita(fita, modo):
    if modo == "ALL":
        return "".join(fita)

    indices_nao_brancos = [i for i, s in fita.items() if s != BRANCO]
    ultimo = max(indices_nao_brancos) if indices_nao_brancos else 0
    return "".join(fita.get(i, BRANCO) for i in range(0, ultimo + 1))


def simular_palavra(palavra, dados, limite_passos=100000, limite_celulas=1000000, registrar_caminho=False):
    modo = dados.get("tipo", "MT")
    estado = dados["estado_inicial"]
    finais = set(dados["estados_finais"])
    transicoes = dados["transicoes"]
    fita, cabeca = _criar_fita(palavra, modo)
    caminho = []

    for passo in range(limite_passos):
        if registrar_caminho:
            caminho.append((passo, estado, cabeca, _conteudo_fita(fita, modo)))

        if estado in finais:
            return True, _conteudo_fita(fita, modo), caminho

        simbolo_lido = _ler_fita(fita, cabeca, modo)
        if simbolo_lido is None:
            return False, _conteudo_fita(fita, modo), caminho

        regra = transicoes.get(estado, {}).get(simbolo_lido)
        if regra is None:
            return False, _conteudo_fita(fita, modo), caminho

        prox_estado, simbolo_escrito, direcao = regra
        if not _escrever_fita(fita, cabeca, simbolo_escrito, modo):
            return False, _conteudo_fita(fita, modo), caminho

        estado = prox_estado
        cabeca += DIRECOES[direcao]

        if modo == "MT":
            if cabeca < 0 or cabeca > limite_celulas:
                return False, _conteudo_fita(fita, modo), caminho
        else:
            if cabeca < 0 or cabeca >= len(fita):
                return False, _conteudo_fita(fita, modo), caminho

    return False, _conteudo_fita(fita, modo), caminho


def executar_mt(dados):
    tipo = dados.get("tipo", "MT")
    print()
    print(SEPARADOR + "╔" + "═" * 58 + "╗")
    print(TITULO + f"║ SIMULAÇÃO DA {tipo} ║")
    print(SEPARADOR + "╚" + "═" * 58 + "╝")
    print()

    aceitas = 0
    rejeitadas = 0

    for palavra in dados["palavras_teste"]:
        aceita, fita_final, _ = simular_palavra(palavra, dados)
        print(SEPARADOR + "─" * 60)
        print(PALAVRA + ("Palavra: λ (vazia)" if palavra == "" else f"Palavra: {palavra}"))
        print(CAMINHO + f"Fita final: {fita_final}")
        if aceita:
            print(OK + f"Resultado: OK {fita_final}")
            aceitas += 1
        else:
            print(ERRO + f"Resultado: X {fita_final}")
            rejeitadas += 1

    print()
    print(SEPARADOR + "═" * 60)
    print(ESTATISTICA + "ESTATÍSTICAS")
    print(SEPARADOR + "═" * 60)
    print(NEON_VERDE + f"Aceitas: {aceitas}")
    print(NEON_VERMELHO + f"Rejeitadas: {rejeitadas}")
    print(NEON_CIANO + f"Total: {aceitas + rejeitadas}")

    if aceitas + rejeitadas > 0:
        taxa = (aceitas / (aceitas + rejeitadas)) * 100
        print(NEON_AMARELO + f"Taxa de aceitação: {taxa:.2f}%")
    print()

    while True:
        print(SEPARADOR + "═" * 60)
        print(DESTAQUE + "[1] Gerar imagem da Máquina de Turing")
        print(DESTAQUE + "[0] Voltar ao menu de extras")
        print(SEPARADOR + "═" * 60)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            gerar_imagem_mt(dados, nome_arquivo="maquina_turing", tipo=tipo)

        elif opcao == "0":
            break

        else:
            print(ERRO + "\nOpção inválida.\n")