from prettytable import PrettyTable
import mysql.connector

def criar_Tabala(base_conectado):
    try:
        cursor= base_conectado.cursor()
        bd= """CREATE TABLE `mini_Projeto` (
            `NOME` varchar(225) NOT NULL,
            `PRECO` varchar(50) NOT NULL,
            `QUANTIDADE` int(20) NOT NULL
        )
        """
        cursor.execute(bd)
        cursor.close()
        base_conectado.commit()
    except:
        pass


    
def incluir_produtos(base_conectado):
    while True:
        produto= input("Por Favor, Falar qual é o produto, preço e sua quantidade.\nPrimeiro nome depois o preço (COM O PONTO) e por ultimo a quantidade, separar por espaço os tres.\nCaso queira sair escreva FIM\n").split(" ")
        if len(produto) == 3:
            try:
                str(produto[0])
                float(produto[1])
                int(produto[2])
                if int(produto[2]) >= 0 and float(produto[1]) >= 0:
                    cursor= base_conectado.cursor()
                    sql= "INSERT INTO `mini_Projeto` (`NOME`, `PRECO`, `QUANTIDADE`) VALUES (\"{}\",\"{}\",{});".format(produto[0].upper(),float(produto[1]), int(produto[2]))

                    cursor.execute(sql)
                    cursor.close()
                    base_conectado.commit()
                    print("CONCLUIDO\n")

                else:
                    print("DIGITOU ALGUMA COISA ERRADA")
            except:
                print("DIGITOU ALGUMA COISA ERRADA")

        elif produto[0].upper() == "FIM":
            return(print("\nCONCLUIDO\n", "#######"*15))
        else:
            print("DIGITOU ALGUMA COISA ERRADA")
        
def atualizar_estoque(base_conectado):
    while True:
        produto_atualizar= input("Qual Produto voce queira atualizar?\nCaso queira sair escreva FIM\n").upper()
        cursor= base_conectado.cursor()

        cursor.execute("SELECT * FROM mini_Projeto")

        resultado = cursor.fetchall()

        coluna_ID= []
        quant_ID=[]

        for nome in range(len(resultado)):
            coluna_ID.append(resultado[nome][0])
            quant_ID.append(resultado[nome][2])
        cursor.close()

        if produto_atualizar in coluna_ID:
            try:
                quant_atualizar= int(input("Quantidade. Numero negativo vai tirar, positivo acrescentar\n"))

                if (quant_ID[coluna_ID.index(produto_atualizar)] + quant_atualizar) < 0:
                    print("VALOR DO ESTOQUE MENOR QUE 0, Valor nao computado\n")

                else:
                    cursor= base_conectado.cursor()
                    sql= "UPDATE mini_Projeto SET QUANTIDADE= {} WHERE NOME = \"{}\";".format((quant_ID[coluna_ID.index(produto_atualizar)] + quant_atualizar), produto_atualizar)

                    cursor.execute(sql)
                    cursor.close()
                    base_conectado.commit()

                    print("CONCLUIDO\n")
            except:
                print("Valor invalido\n")
                
        elif produto_atualizar == "FIM":
            return(print("\nCONCLUIDO\n", "#######"*15))
        else:
            print("Produto Nao existe\n")

def listagem_produtos(base_conectado):
    estrutura_tabela= PrettyTable()
    estrutura_tabela.field_names= ["PRODUTOS", "PREÇO", "QUANTIDADES"]

    cursor= base_conectado.cursor()
    cursor.execute("SELECT * FROM mini_Projeto")
    resultado = cursor.fetchall()

    cursor.close()
    
    for i in range(len(resultado)):
        estrutura_tabela.add_row([resultado[i][0], "R$" + str(resultado[i][1]), resultado[i][2]])
    return(print(estrutura_tabela), "\n","#######"*15)

def atualizar_preco(base_conectado):
    while True:
        produto_atualizar= input("Digitar o novo preço\n").upper()
        cursor= base_conectado.cursor()

        cursor.execute("SELECT * FROM mini_Projeto")

        resultado = cursor.fetchall()

        coluna_ID= []
        preco_ID=[]

        for nome in range(len(resultado)):
            coluna_ID.append(resultado[nome][0])
            preco_ID.append(resultado[nome][1])
        cursor.close()

        if produto_atualizar in coluna_ID:
            try:
                preco_atualizar= float(input("Quantidade. Numero negativo vai tirar, positivo acrescentar\n"))

                if preco_atualizar < 0:
                    print("VALOR DO PREÇO MENOR QUE 0, Valor nao computado\n")

                else:
                    cursor= base_conectado.cursor()
                    sql= "UPDATE mini_Projeto SET PRECO= \"{}\" WHERE NOME = \"{}\";".format(str(preco_atualizar), produto_atualizar)

                    cursor.execute(sql)
                    cursor.close()
                    base_conectado.commit()

                    print("CONCLUIDO\n",)
            except:
                print("Valor invalido")
                
        elif produto_atualizar == "FIM":
            return(print("\nCONCLUIDO\n", "#######"*15))
        else:
            print("Produto Nao existe\n")
 
def selecionar_atributos(base_conectado):
    while True:
        while True:
            desejos= input("Voce deseja fazer o que:\n0(Incluir novos produtos)\n1(Atualizar estoque)\n2(Atualizar preço)\n3(Listagem de todos os produtos)\n4(FIM)\n")
            if desejos == "0" or desejos == "1" or desejos == "2" or desejos == "3" or desejos == "4":
                break    
        if desejos == "0":
            incluir_produtos(base_conectado)
        elif desejos == "1":
            atualizar_estoque(base_conectado)
        elif desejos == "2":
            atualizar_preco(base_conectado)
        elif desejos == "3":
            listagem_produtos(base_conectado)
        elif desejos == "4":
            break

def main():
    base_conectado= mysql.connector.connect(host= "localhost", user= "root", password= "", database= "mini_projeto2")          # ENTRO NA BANCO DE DADOS
    criar_Tabala(base_conectado)
    selecionar_atributos(base_conectado)

main()



