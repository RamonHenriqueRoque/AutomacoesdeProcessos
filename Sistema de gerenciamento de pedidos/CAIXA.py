import BD_SQL
from prettytable import PrettyTable
import sys

def arrumando_codigo_barra(barra):
    try:
        return(int(barra))
    except:
        print("CODIGO DO CLIENTE INVALIDO")
        main()

def pegar_lista_produtos(barra):
    lista= BD_SQL.main(selecionar_colocado= 0)
    imprimindo_produtos(lista, barra)

def visualizar_produtos(produto_cliente):
    estrutura_tabela= PrettyTable()
    estrutura_tabela.field_names= ["PRODUTO"]

    for produto in produto_cliente:
        estrutura_tabela.add_row([produto])
    print(estrutura_tabela)

def imprimindo_produtos(lista_produtos, codigo_barra_cliente):
    # Visualizando os pedidos do cliente
    try:
        produto_cliente= lista_produtos[codigo_barra_cliente]
    except:
        arrumando_codigo_barra("ERRO")
        imprimindo_produtos(lista_produtos, codigo_barra_cliente)
        
    visualizar_produtos(produto_cliente)
    
    # Codigo de Barra do produto
    pegando_ID_produto= BD_SQL.id_produtos(produto_cliente)                                 #RETORNA UM DICIONARIO (key = ID, Value= Produto)

    lista_keys= list(pegando_ID_produto.keys())

    while lista_keys != []:
        try:
            id_produto= int(input("POR FAVOR, COLOQUE O CODIGO DE BARRA DO PRODUTO\n"))

            if id_produto in lista_keys:
                BD_SQL.mudando_coluna_colocado(codigo_barra_cliente, pegando_ID_produto[id_produto])
            
                print("OK")
                lista_keys.remove(id_produto)
            else:
                print("ERROR")
        except:
            print("ERROR")
            
    BD_SQL.mudando_coluna_processos(codigo_barra_cliente)
    print("PODE FECHAR A CAIXA")

    
    
def main():
    while True:
        teclado_menu= input("Para fechar o programa digita 0, caso contrario 1\n")
        if teclado_menu == "0":
            sys.exit()
        elif teclado_menu == "1":
            pegar_lista_produtos(arrumando_codigo_barra(input("COLOCAR O CODIGO DE BARRA DO CLIENTE\n")))
        else:
            print("Valor invalido")
main()
















