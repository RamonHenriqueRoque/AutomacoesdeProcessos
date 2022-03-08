"""
RAMON HENRIQUE ROQUE RA: 758958
"""
import pandas as pd
import numpy as np
from prettytable import PrettyTable
from typing import List, Tuple

def importar_separar() -> Tuple[float, list, float]:
  """
    Nessa função tem o objetivo de importar os dados de um arquivo json,
    e após importar ele dividir nas suas categorias.

    Returns
    -------
    Tuple[float, list, float]
        custo_setup: Custo para fazer a troca de setup
        demanda: Retorna a demanda do mercado.
        custo_manutencao: Custo de manutenção do produto no mês.
   """
  importando_dados = pd.read_json("Dados Algoritmo SealMeals.txt")
  custo_setup= importando_dados["Custo de Setup"].unique()[0]
  demanda= importando_dados["Demanda"].to_list()
  custo_manutencao= importando_dados["Custo de Manutenção"].unique()[0]

  return(custo_setup, demanda, custo_manutencao)

def calculo_armazenamento(custo_manutencao: int, periodo_demanda: int, demanda: list) -> int:
    """
    Nessa função nos calculamos o custo de armazenamento dos 
    produtos em relação ao tempo.

    Parameters
    ----------
    custo_manutencao : int
        Custo de manutencao no estoque do produto ao mês.
    periodo_demanda : int
        Periodo que estamos analisando.
    demanda : list
        Demanda do produto.

    Returns
    -------
    int
        Custo de armazenamento de X produtos com y meses.

    """
    demanda= demanda[:periodo_demanda]
    valor= sum([quant*custo_manutencao*i for i, quant in enumerate(demanda)])

    return(valor)


def algoritmo_SealMeals(custo_setup: int, demanda: list, custo_manutencao: int) -> Tuple[list, list]:
    """
    Aqui temos o algoritmo seal meals funcionando.
    Parameters
    ----------
    custo_setup : int
        Custo para fazer o setup do produto.
    demanda : list
        Demando do produto.
    custo_manutencao : int
        custo de manutencao no estoque.

    Returns
    -------
    Tuple[list, list]
        A primeira retorna as interações e seus resultados.
        A segunda retorna a solução do problema

    """
    periodo= 1
    criterio_parada= False
    interacao= 1
    resposta_interacao= []
    melhor_momento= []
    
    while(True):
        memoria_menor_custo_unitario= 9999999
        lote = 0
        
        # Calculo das variaveis
        for periodo_demanda, valor_demanda in enumerate(demanda):
            lote += valor_demanda
            custo_armazenamento= [0 if periodo_demanda == 0 else calculo_armazenamento(custo_manutencao, periodo_demanda+1, demanda)][0]
            custo_unitario= round((custo_armazenamento+custo_setup)/lote, 4)
            resposta_interacao.append(["INTERAÇÃO {}".format(interacao), 
                                       periodo,
                                       lote, 
                                       custo_setup, 
                                       custo_armazenamento, 
                                       custo_unitario])
            interacao += 1
            
            # Caso acharmos uma resposta boa no periodo
            if memoria_menor_custo_unitario < custo_unitario:
                demanda= demanda[periodo_demanda:]
                periodo += periodo_demanda 
                
                melhor_momento.append(resposta_interacao[-2])
                break
            memoria_menor_custo_unitario = custo_unitario
         
        # Criterio de parada
        if criterio_parada == True:
            melhor_momento.append(resposta_interacao[-1])
            return(resposta_interacao, melhor_momento)
        if len(demanda) == 1 or len(demanda) == 0:
            criterio_parada= True

def arrumando_respostas(resultado_interacao: list, solucao: list) -> Tuple[str, str]:
    """
    Aqui vamos transformar lista em tabela texto

    Parameters
    ----------
    resultado_interacao : list
        Interação que o algoritmo fez.
    solucao : list
        Solucao do problema.

    Returns
    -------
    Tuple[str, str]
        Teremos duas tabelas.

    """
    # Tratando da solução
    estrutura_tabela_solucao= PrettyTable()
    estrutura_tabela_solucao.field_names= ["Perido de fabricação", "Quant", 
                                           "Custo Total", "Custo Unitario", 
                                           "Espaço Tempo"]
    
    for id, periodo in enumerate(solucao):
        estrutura_tabela_solucao.add_row([periodo[1], 
                                          periodo[2], 
                                          "${}".format(round(periodo[2]*periodo[5],2)), 
                                          "${}".format(round(periodo[5],2)),
                                          "Do {} ao {}".format(periodo[1],
                                                               [solucao[id][1] if (len(solucao)-1) == id else solucao[id+1][1]-1][0])])
    
    # Tratando da interacao
    estrutura_tabela_interacao= PrettyTable()
    estrutura_tabela_interacao.field_names= ["Interacao", 
                                             "Perido de fabricação", 
                                             "Quant", 
                                             "Custo Total", 
                                             "Custo Unitario"]

    for periodo in resultado_interacao:
        estrutura_tabela_interacao.add_row([periodo[0],
                                            periodo[1],
                                            periodo[2],
                                            "${}".format(round(periodo[2]*periodo[5],1)),
                                            "${}".format(round(periodo[5],2))])
        
    return(estrutura_tabela_solucao, estrutura_tabela_interacao)


def exportando_resultado(resultado_interacao: list, solucao: list):
    """
    Escrevendo no arquivo TXT

    Parameters
    ----------
    resultado_interacao : list
        Interação que o algoritmo fez.
    solucao : list
        Solucao do problema.

    Returns
    -------
    Um arquivo TXT

    """
    with open('Resultados do algoritmo de SealMeals.txt','w') as f:
        f.write("Abaixo apresenta os resultados do algoritmo do problema proposto. \n\n\n")
        f.write("A seguir temos as interações\n\n")
        f.write(resultado_interacao.get_string())
        f.write("\n"*2)
        f.write("A seguir os resultados do modelo\n\n")
        f.write(solucao.get_string())
 

if __name__ == "__main__":
    custo_setup, demanda, custo_manutencao= importar_separar()
    resultado_interacao, solucao= algoritmo_SealMeals(custo_setup, demanda, custo_manutencao)
    estrutura_tabela_solucao, estrutura_tabela_interacao= arrumando_respostas(resultado_interacao, solucao)
    exportando_resultado(estrutura_tabela_interacao, estrutura_tabela_solucao)


