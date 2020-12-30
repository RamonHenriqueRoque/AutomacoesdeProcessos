import mysql.connector

def selecionar_cliente(base_conectado, selecionar_colocado):

    # Caixa
    if selecionar_colocado == 0:
        # Acessando a base de dados
        cursor= base_conectado.cursor()
        sql= "SELECT * from `pedidos_clientes` where `colocado` = 0"
        cursor.execute(sql)

        #Pegando o resultado da pesquisa
        resultado = cursor.fetchall()
        cursor.close()                                                                                  # Fechando o programa

        resultado= arrumando_lista(resultado, selecionar_colocado)
        return (resultado)

    # GERENTE
    elif selecionar_colocado == 1:
        # Acessando a base de dados
        cursor= base_conectado.cursor()
        sql= "SELECT * from `andamento` where `processos` = 1"
        cursor.execute(sql)

        #Pegando o resultado da pesquisa
        resultado = cursor.fetchall()
        cursor.close()                                                                                  # Fechando o programa

        resultado= arrumando_lista(resultado, selecionar_colocado)
        return(resultado)

    
    
def arrumando_lista(lista, selecionar_colocado):
    # Caixa
    if selecionar_colocado == 0:
        dic_arrumado= {}
        # Criando a Key do Dicionario
        for unidade_lista in lista:
            dic_arrumado[unidade_lista[0]] = []

        # Adicionando os produtos
        for produto_lista in lista:
            dic_arrumado[produto_lista[0]].append(produto_lista[1])
        return (dic_arrumado)

    # GERENTE
    elif selecionar_colocado == 1:
        lista_Cliente= []
        for id_Cliente in lista:
            lista_Cliente.append(id_Cliente[0])
        return (lista_Cliente)


def main(selecionar_colocado):
    base_conectado= mysql.connector.connect(host= "localhost", user= "root", password= "", database= "projetofinalai")

    # Saber se é Caixa ou Gerente
    resultado= selecionar_cliente(base_conectado, selecionar_colocado = selecionar_colocado)
    return(resultado)





def id_produtos (lista):
    base_conectado= mysql.connector.connect(host= "localhost", user= "root", password= "", database= "projetofinalai")
    cursor= base_conectado.cursor()
    sql= "SELECT * from produtos;"
    cursor.execute(sql)

    #Pegando o resultado da pesquisa
    resultado= cursor.fetchall()
    cursor.close()                                                                                  # Fechando o programa
    lista_ID_final= []

    for result_prod in resultado:
      if result_prod[1] in lista:
        lista_ID_final.append([result_prod[0], result_prod[1]])

    return (dict(lista_ID_final))


def mudando_coluna_colocado(id_cliente, produto):
    base_conectado= mysql.connector.connect(host= "localhost", user= "root", password= "", database= "projetofinalai")

    cursor= base_conectado.cursor()
    sql= "UPDATE `pedidos_clientes` SET `COLOCADO`= 1 WHERE `ID_CLIENTE` = {} and `PRODUTO` = \"{}\";".format(id_cliente, produto)
    cursor.execute(sql)
    cursor.close()
    base_conectado.commit()
    base_conectado.close()

def mudando_coluna_processos(id_cliente):
    base_conectado= mysql.connector.connect(host= "localhost", user= "root", password= "", database= "projetofinalai")

    cursor= base_conectado.cursor()
    sql= "UPDATE `andamento` SET `PROCESSOS`= 1 WHERE `ID_CLIENTE` = {};".format(id_cliente)
    cursor.execute(sql)
    cursor.close()
    base_conectado.commit()
    base_conectado.close()















