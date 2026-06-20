from leituraArq import ler_arquivo
from interface import menu_principal, menu_extras

from automatomt import ler_arquivo_mt, executar_mt
from automatofd import executar_afd
from automatoafnd import executar_afnd


def main():

    while True:

        opcao = menu_principal()

        if opcao == "1":
            dados = ler_arquivo("entrada.txt")
            executar_afd(dados)

        elif opcao == "2":
            while True:

                opcao_extra = menu_extras()

                if opcao_extra == "1":
                    dados = ler_arquivo("entrada_afnd.txt")
                    executar_afnd(dados)

                elif opcao_extra == "2":
                    #fazer ap
                     print("ap")
                    
                elif opcao_extra == "3":
                     dados = ler_arquivo_mt("entrada_mt.txt")
                     executar_mt(dados)
                   
                elif opcao_extra == "0":
                    break

                else:
                    print("\nOpção inválida.\n")

        elif opcao == "0":
            print("\nEncerrando programa...")
            break

        else:
            print("\nOpção inválida.\n")

if __name__ == "__main__":
    main()