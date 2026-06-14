from leituraArq import ler_arquivo
from interface import menu_principal, menu_extras

from automatofd import executar_afd



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

                    #fazer afn
                     print("afn")
                elif opcao_extra == "2":

                    #fazer ap
                     print("ap")
                    
                elif opcao_extra == "3":

                    #fazer mt
                     print("mt")
                   
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