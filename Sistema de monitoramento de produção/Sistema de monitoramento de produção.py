import mysql.connector
from prettytable import PrettyTable
from time import strftime, localtime
from datetime import datetime


def criar_Tabala(base_conectado):
        try:
            cursor= base_conectado.cursor()
            bd= """CREATE TABLE `PROJETO_INDIVIDUAL` (
            `Ordem` varchar(225) NOT NULL,
            `Estacao_1` varchar(50) NOT NULL,
            `Data_entrada_estacao_1` varchar(50) NOT NULL,
            `Data_saida_estacao_1` varchar(50) NULL,
            `Estacao_2` varchar(50) NULL,
            `Data_entrada_estacao_2` varchar(50) NULL,
            `Data_saida_estacao_2` varchar(50) NULL
            )"""
            
            cursor.execute(bd)
            cursor.close()
            base_conectado.commit()
        except:
            pass


def inserir_Ordem (base_conectado):
    while True:
        ordem= input("Por Favor, Falar qual é a ordem.\nCaso queira sair escreva FIM\n").upper()
        if ordem != "FIM":
            cursor= base_conectado.cursor()
            sql= "INSERT INTO `PROJETO_INDIVIDUAL` (`Ordem`, `Estacao_1`, `Data_entrada_estacao_1`) VALUES (\"{}\",\"{}\",\"{}\");".format(ordem, "CONFIRMADO", strftime("%d-%m-%Y %H:%M:%S", localtime()))
            cursor.execute(sql)
            cursor.close()
            base_conectado.commit()
            print("CONCLUIDO\n")
        else:
            break

def saida_1(base_conectado):
    while True:
        produto_saiu_1= input("Qual ordem que saiu da fabrica 1?\nCaso queira sair escreva FIM\n").upper()
        
        cursor= base_conectado.cursor()

        cursor.execute("SELECT * FROM PROJETO_INDIVIDUAL WHERE estacao_1 = \"CONFIRMADO\"")

        resultado = cursor.fetchall()

        ordem_ID= []

        for nome in range(len(resultado)):
            ordem_ID.append(resultado[nome][0])

        cursor.close()

        if produto_saiu_1 in ordem_ID:
            cursor= base_conectado.cursor()
            sql= "UPDATE PROJETO_INDIVIDUAL SET Data_saida_estacao_1= \"{}\" WHERE Ordem = \"{}\";".format(strftime("%d-%m-%Y %H:%M:%S", localtime()), produto_saiu_1)

            cursor.execute(sql)
            cursor.close()
            base_conectado.commit()
            
            print("CONCLUIDO\n",)
            
        elif produto_saiu_1 == "FIM":
            return(print("\nCONCLUIDO\n", "#######"*15))

        else:
            print("Produto Nao existe\n")


def entrada_2(base_conectado):
    while True:
        produto_entrada_2= input("Qual ordem que entrou na fabrica 2?\nCaso queira sair escreva FIM\n").upper()
        
        cursor= base_conectado.cursor()

        cursor.execute("SELECT * FROM PROJETO_INDIVIDUAL WHERE estacao_1 = \"CONFIRMADO\"")

        resultado = cursor.fetchall()

        ordem_ID= []

        for nome in range(len(resultado)):
            ordem_ID.append(resultado[nome][0])

        cursor.close()

        if produto_entrada_2 in ordem_ID:
            cursor= base_conectado.cursor()
            sql= "UPDATE PROJETO_INDIVIDUAL SET Estacao_2= \"{}\" WHERE Ordem = \"{}\";".format("CONFIRMADO", produto_entrada_2)

            cursor.execute(sql)

            cursor.execute("UPDATE PROJETO_INDIVIDUAL SET Data_entrada_estacao_2= \"{}\" WHERE Ordem = \"{}\";".format(strftime("%d-%m-%Y %H:%M:%S", localtime()), produto_entrada_2))
            
            sql= "UPDATE PROJETO_INDIVIDUAL SET Estacao_1= \"{}\" WHERE Ordem = \"{}\";".format("FINALIZADO", produto_entrada_2 )

            cursor.execute(sql)
            cursor.close()
            base_conectado.commit()

            print("CONCLUIDO\n",)
            
        elif produto_entrada_2 == "FIM":
            return(print("\nCONCLUIDO\n", "#######"*15))

        else:
            print("Produto Nao existe\n")


def saida_2(base_conectado):
    while True:
        produto_saida_2= input("Qual ordem que entrou na fabrica 2?\nCaso queira sair escreva FIM\n").upper()
        
        cursor= base_conectado.cursor()
        cursor.execute("SELECT * FROM PROJETO_INDIVIDUAL WHERE estacao_2 = \"CONFIRMADO\";")
        resultado = cursor.fetchall()

        ordem_ID= []

        for nome in range(len(resultado)):
            ordem_ID.append(resultado[nome][0])

        cursor.close()

        if produto_saida_2 in ordem_ID:
            cursor= base_conectado.cursor()
            sql= "UPDATE PROJETO_INDIVIDUAL SET Estacao_2= \"{}\", Data_saida_estacao_2= \"{}\" WHERE Ordem = \"{}\";".format("FINALIZADO", strftime("%d-%m-%Y %H:%M:%S", localtime()), produto_saida_2)

            cursor.execute(sql)
            cursor.close()
            base_conectado.commit()

            print("CONCLUIDO\n",)
            
        elif produto_saida_2 == "FIM":
            return(print("\nCONCLUIDO\n", "#######"*15))

        else:
            print("Produto Nao existe\n")


def quais_foram_produzidos(base_conectado):
    estrutura_tabela= PrettyTable()
    estrutura_tabela.field_names= ["Ordem", "ESTAÇÃO_1", "DATA_ENTRADA_ESTAÇÃO_1", "DATA_SAIDA_ESTAÇÃO_1", "ESTAÇÃO_2", "DATA_ENTRADA_ESTAÇÃO_2",
                                   "DATA_SAIDA_ESTAÇÃO_2"]

    cursor= base_conectado.cursor()
    
    cursor.execute("SELECT * FROM PROJETO_INDIVIDUAL WHERE estacao_2 = \"FINALIZADO\";")
    resultado = cursor.fetchall()
    cursor.close()
    
    for i in range(len(resultado)):
        estrutura_tabela.add_row([resultado[i][0],resultado[i][1],resultado[i][2],resultado[i][3],resultado[i][4],resultado[i][5],resultado[i][6]])
    return(print(estrutura_tabela), "\n","#######"*15)


def quem_esta_sendo_produzidos(base_conectado):
    
    estrutura_tabela= PrettyTable()
    estrutura_tabela.field_names= ["Ordem", "ESTAÇÃO_1", "DATA_ENTRADA_ESTAÇÃO_1", "DATA_SAIDA_ESTAÇÃO_1", "ESTAÇÃO_2", "DATA_ENTRADA_ESTAÇÃO_2",
                                   "DATA_SAIDA_ESTAÇÃO_2"]

    cursor= base_conectado.cursor()

    cursor.execute("SELECT * FROM PROJETO_INDIVIDUAL WHERE estacao_1 = \"CONFIRMADO\" or  estacao_2 = \"CONFIRMADO\";")
    resultado = cursor.fetchall()
    cursor.close()
    
    for i in range(len(resultado)):
        estrutura_tabela.add_row([resultado[i][0],resultado[i][1],resultado[i][2],resultado[i][3],resultado[i][4],resultado[i][5],resultado[i][6]])
    return(print(estrutura_tabela), "\n","#######"*15)


def quem_esta_na_fabrica1(base_conectado):
    estrutura_tabela= PrettyTable()
    estrutura_tabela.field_names= ["Ordem", "ESTAÇÃO_1", "DATA_ENTRADA_ESTAÇÃO_1", "DATA_SAIDA_ESTAÇÃO_1", "ESTAÇÃO_2", "DATA_ENTRADA_ESTAÇÃO_2",
                                   "DATA_SAIDA_ESTAÇÃO_2"]

    cursor= base_conectado.cursor()

    cursor.execute("SELECT * FROM PROJETO_INDIVIDUAL WHERE estacao_1 = \"CONFIRMADO\";")
    resultado = cursor.fetchall()
    cursor.close()
    
    for i in range(len(resultado)):
        estrutura_tabela.add_row([resultado[i][0],resultado[i][1],resultado[i][2],resultado[i][3],resultado[i][4],resultado[i][5],resultado[i][6]])
    return(print(estrutura_tabela), "\n","#######"*15)


def quem_esta_na_fabrica2(base_conectado):
    estrutura_tabela= PrettyTable()
    estrutura_tabela.field_names= ["Ordem", "ESTAÇÃO_ESTRADA", "DATA_ENTRADA_ESTAÇÃO_1", "DATA_SAIDA_ESTAÇÃO_1", "ESTAÇÃO_ESTAÇÃO_2", "DATA_ENTRADA_ESTAÇÃO_2",
                                   "DATA_SAIDA_ESTAÇÃO_2"]

    cursor= base_conectado.cursor()

    cursor.execute("SELECT * FROM PROJETO_INDIVIDUAL WHERE estacao_2 = \"CONFIRMADO\";")
    resultado = cursor.fetchall()
    cursor.close()
    
    for i in range(len(resultado)):
        estrutura_tabela.add_row([resultado[i][0],resultado[i][1],resultado[i][2],resultado[i][3],resultado[i][4],resultado[i][5],resultado[i][6]])
    return(print(estrutura_tabela), "\n","#######"*15)

def diferenca_tempo(d1, d2):
    d1 = datetime.strptime(d1, "%d-%m-%Y %H:%M:%S")
    d2 = datetime.strptime(d2, "%d-%m-%Y %H:%M:%S")
    return str(abs((d2 - d1)))

def media_tempo(lista):
    separa_tempo=[]
    segundo=0
    minuto=0
    horas=0
    
    for sep in lista:
        separa_tempo.append(sep.split(":"))

    for tempo in separa_tempo:
        segundo += int(tempo[2])
        minuto += int(tempo[1])
        horas += int(tempo[0])

    soma_total_tempo= horas*3600 + minuto*60 + segundo
    
    media_tempo= soma_total_tempo/len(lista)
    
    segundo=0
    minuto=0
    horas=0
    while media_tempo != 0:
        if media_tempo >= 3600:
            horas = media_tempo//3600
            media_tempo = media_tempo - horas*3600
        elif media_tempo >= 60:
            minuto= media_tempo//60
            media_tempo = media_tempo - minuto*60
        else:
            segundo= int(media_tempo)
            media_tempo= 0
    return (print("O Tempo medio foi de %i:%i:%s.\n"%(horas, minuto, segundo)))


def tempo_medio(base_conectado):
    cursor= base_conectado.cursor()

    cursor.execute("SELECT Data_entrada_estacao_1, Data_saida_estacao_2 FROM PROJETO_INDIVIDUAL WHERE Estacao_2 = \"FINALIZADO\";")

    resultado = cursor.fetchall()

    cursor.close()

    diferenca=[]
    for i in range(len(resultado)):
        diferenca.append(diferenca_tempo(resultado[i][0], resultado[i][1]))
    media_tempo(diferenca)
    

def selecionar_atributos(base_conectado):
    while True:
        while True:
            lista_desejos=["Voce deseja fazer o que:", "0(Incluir nova ordem)",
                           "1(Saida de Ordem na fabrica)","2(Entrada de Ordem na fabrica)",
                           "3(Saida de Ordem na fabrica)","4(Quais ordem foram Produzidos)",
                           "5(Quem estão sendo produziddos)","6(Quem esta na fabrica)",
                           "7(Quem esta na fabrica)", "8(Tempo Medio de produção)", "9(Caso queira SAIR)"]
            for i in lista_desejos: print(i)
            
            desejos= input()
            if desejos in [str(i) for i in range(0,10)]:
                break    
        if desejos == "0":
            inserir_Ordem(base_conectado)
        elif desejos == "1":
            saida_1(base_conectado)
        elif desejos == "2":
            entrada_2(base_conectado)
        elif desejos == "3":
            saida_2(base_conectado)
        elif desejos == "4":
            quais_foram_produzidos(base_conectado)
        elif desejos == "5":
            quem_esta_sendo_produzidos(base_conectado)
        elif desejos == "6":
            quem_esta_na_fabrica1(base_conectado)
        elif desejos == "7":
            quem_esta_na_fabrica2(base_conectado)
        elif desejos == "8":
            tempo_medio(base_conectado)
        elif desejos =="9":
            base_conectado.close()
            break
        
def main():
    base_conectado= mysql.connector.connect(host= "localhost", user= "root", password= "", database= "mini_projeto2")          # ENTRO NA BANCO DE DADOS
    criar_Tabala(base_conectado)
    selecionar_atributos(base_conectado)

main()
