from colorama import Fore, Style, init

init(autoreset=True)

# ==========================
# CORES PRINCIPAIS
# ==========================

TITULO = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
SEPARADOR = Fore.LIGHTCYAN_EX + Style.BRIGHT

OK = Fore.LIGHTGREEN_EX + Style.BRIGHT
ERRO = Fore.LIGHTRED_EX + Style.BRIGHT

CAMINHO = Fore.LIGHTBLUE_EX + Style.BRIGHT
PALAVRA = Fore.LIGHTYELLOW_EX + Style.BRIGHT

ESTATISTICA = Fore.LIGHTMAGENTA_EX + Style.BRIGHT

INFO = Fore.LIGHTCYAN_EX + Style.BRIGHT
DESTAQUE = Fore.LIGHTYELLOW_EX + Style.BRIGHT

# ==========================
# CORES INDIVIDUAIS
# ==========================

PRETO = Fore.BLACK
VERMELHO = Fore.RED
VERDE = Fore.GREEN
AMARELO = Fore.YELLOW
AZUL = Fore.BLUE
MAGENTA = Fore.MAGENTA
CIANO = Fore.CYAN
BRANCO = Fore.WHITE

# ==========================
# CORES NEON
# ==========================

NEON_VERMELHO = Fore.LIGHTRED_EX + Style.BRIGHT
NEON_VERDE = Fore.LIGHTGREEN_EX + Style.BRIGHT
NEON_AMARELO = Fore.LIGHTYELLOW_EX + Style.BRIGHT
NEON_AZUL = Fore.LIGHTBLUE_EX + Style.BRIGHT
NEON_MAGENTA = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
NEON_CIANO = Fore.LIGHTCYAN_EX + Style.BRIGHT
NEON_BRANCO = Fore.LIGHTWHITE_EX + Style.BRIGHT

RESET = Style.RESET_ALL