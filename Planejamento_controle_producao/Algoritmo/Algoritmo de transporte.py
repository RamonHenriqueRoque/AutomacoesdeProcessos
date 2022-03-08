"""
RAMON HENRIQUE ROQUE
"""

import pandas as pd
import numpy as np
from prettytable import PrettyTable
from typing import List, Tuple

def importar_separar() -> Tuple[list, list, list, list, list]:
  """
    Nessa função tem o objetivo de importar os dados de um arquivo json,
    e após importar ele dividir nas suas categorias.

    Returns
    -------
    Tuple[list, list, list, list, list]
        capacidade: Retorna a capacidade do processo.
        demanda: Retorna a demanda do mercado.
        custo_produção: Custo de produção.
        estoque: Estoque inicial e final.
        custo_estoque: Custo de estoque.
   """
  importando_dados = pd.read_json("Dados Algoritmo de transporte.txt")
  capacidade= importando_dados["Capacidade"].dropna().to_list()
  demanda= importando_dados["Demanda"].dropna().to_list()
  custo_producao= importando_dados["Custo de produção Normal"].dropna().to_list()
  estoque= importando_dados["Estoque"].dropna().to_list()
  custo_estoque= importando_dados["Custo de estoque"].dropna().to_list()
  custo_estoque.insert(0,0)

  return(capacidade, demanda, custo_producao, estoque, custo_estoque)

def arrumar_estoque(custo_no_periodo: list) -> List:
    """
    Combino o custo de estoque em relação aos periodos

    Parameters
    ----------
    custo_no_periodo : list
        Custo de estoque no periodo.

    Returns
    -------
    List
        Custo do estoque combinado no periodo.

    """
    return([sum(custo_no_periodo[0:id+1]) for id in range(len((custo_no_periodo)))])

def criar_matriz_custo(custo_estoque_periodo: list, custo_producao_periodo: list) -> np.ndarray:
    """
    Matriz de custo, que é a combinação do preço de estoque + preço de produção. Com isso,
    conseguimos o preço total no periodo que será produzido.

    Parameters
    ----------
    custo_estoque_periodo : list
        Custo do estoque combinado no periodo.
    custo_producao_periodo : list
        Custo do produção no periodo.

    Returns
    -------
    np.ndarray
        Retorna a matriz de custo total do periodo.

    """
    matriz_custo_por_periodo= []
    
    for cont, custo_producao in enumerate(custo_producao_periodo):
      periodo= []
      
      # Soma dos custos estoque e produção
      for custo_estoque in custo_estoque_periodo:
        periodo.append(custo_estoque+custo_producao)
      
      # Quando não haver sentido no de produção, EX: prod no periodo 3 para a demanda no periodo 1
      # O 9999999999 tem o sentido do BIG_M
      for _ in range(cont):
        periodo.insert(0, 9999999999)
        periodo.pop(-1)
        
      matriz_custo_por_periodo.append(periodo)
    
    return(np.array(matriz_custo_por_periodo))

def metodo_transporte(matriz_custo: np.ndarray, estoque: list, capacidade: list, demanda: list) -> Tuple[list, list]:
    """
    Aqui utilizamos o método de transporte tambem conhecido como método canto noroeste

    Parameters
    ----------
    matriz_custo : np.ndarray
        matriz de custo total do periodo.
    estoque : list
        Estoque inicial e final.
    capacidade : list
        Retorna a capacidade do processo.
    demanda : list
        Retorna a demanda do mercado.

    Returns
    -------
    Tuple[list, list]
        retorno: solução do algoritmo.
        capacidade: se ainda pode ser fabricado no periodo

    """
    estoque_inicial= estoque[0]
    estoque_final= estoque[1]
    matriz_custo_periodo= matriz_custo.T
    
    producao_periodo= {}
    retorno= []
    
    for periodo in range(matriz_custo_periodo.shape[0]):
      custo_periodo= matriz_custo_periodo[periodo]
      periodo_menor_custo= np.where(custo_periodo == min(custo_periodo))[0][0]
      demanda_p = demanda[periodo_menor_custo]
      
      while True:
        
        if capacidade[periodo_menor_custo] > 0:
          
          # Primeiro periodo onde temos estoque inicial
          if periodo == 0:
            quant_prod= demanda[periodo_menor_custo] - estoque_inicial
            producao= [capacidade[periodo_menor_custo] if quant_prod > capacidade[periodo_menor_custo] else quant_prod][0]
            custo= producao * min(custo_periodo)
    
            capacidade[periodo_menor_custo] = capacidade[periodo_menor_custo] - producao                              # Atualizando Capacidade
            demanda_p -= producao + estoque_inicial
            retorno.append([periodo+1, periodo_menor_custo+1, producao, custo])
          
          # Ultimo periodo onde temos estoque Final
          elif periodo == matriz_custo_periodo.shape[0]-1:
            producao= [capacidade[periodo_menor_custo] if estoque_final > capacidade[periodo_menor_custo] else estoque_final][0]
            custo= producao * min(custo_periodo)
    
            capacidade[periodo_menor_custo] = capacidade[periodo_menor_custo] - producao                                # Atualizando Capacidade
            demanda_p -= producao
            retorno.append(["Estoque Final", periodo_menor_custo+1, producao, custo])
            break
           
          # Periodo do meio
          else:
            producao= [capacidade[periodo_menor_custo] if demanda_p > capacidade[periodo_menor_custo] else demanda_p][0]
            custo= producao * min(custo_periodo)
    
            capacidade[periodo_menor_custo] = capacidade[periodo_menor_custo] - producao                                # Atualizando Capacidade
            demanda_p -= producao
            retorno.append([periodo+1, periodo_menor_custo+1, producao, custo])
          
          if demanda_p == 0:
              break
        
        # Caso que nenhum dos periodos tenha capacidade para a produção
        elif np.array_equiv(custo_periodo, np.array([9999999999]*custo_periodo.shape[0])):
          break
        
        # sentido do BIG_M
        else:
          custo_periodo[periodo_menor_custo]= 9999999999
      
        periodo_menor_custo= np.where(custo_periodo == min(custo_periodo))[0][0]
    return(retorno, capacidade)

def arrumando_respostas(respostas: list, capacidade_sobra:list) -> Tuple[str, str]:
    """
    Aqui vamos transformar lista em tabela texto

    Parameters
    ----------
    respostas : list
        solução do algoritmo.
    capacidade_sobra : list
        se ainda pode ser fabricado no periodo.

    Returns
    -------
    Tuple[str, str]
        Teremos duas tabelas.

    """
    # Tratando da solução
    estrutura_tabela_respostas= PrettyTable()
    estrutura_tabela_respostas.field_names= ["Periodo", "Perido de criação", "Quant. Prod", "Custos"]

    for periodo in respostas:
        estrutura_tabela_respostas.add_row([periodo[0], periodo[1], periodo[2], periodo[3]])
    
    # Tratando da capacidade
    estrutura_tabela_cap= PrettyTable()
    estrutura_tabela_cap.field_names= ["Cap. Periodos"]

    for periodo in capacidade_sobra:
        estrutura_tabela_cap.add_row([periodo])
        
    return(estrutura_tabela_respostas, estrutura_tabela_cap)


def exportando_resultado(respostas: list, capacidade_sobra:list, prod_total: int, custo_total: int):
    """
    Escrevendo no arquivo TXT

    Parameters
    ----------
    respostas : list
        solução do algoritmo.
    capacidade_sobra : list
        se ainda pode ser fabricado no period
    prod_total : int
        Soma da produção feita em todos os periodos.
    custo_total : int
        Soma da custo feita em todos os periodos.

    Returns
    -------
    Um arquivo TXT

    """
    with open('Resultados do algoritmo de transporte.txt','w') as f:
        f.write("Abaixo apresenta os resultados do algoritmo do problema proposto. \n\n\n")
        f.write(respostas.get_string())
        f.write("\n"*2)
        f.write("Legenda: \nA coluna Periodo: significa o periodo que se refere a demanda;\n")
        f.write("A coluna Periodo de fabricação: o periodo que vamos fabricar o lote;\n")
        f.write("A coluna Quant. Prod: a quantidade de produção.\n")
        f.write("A coluna Custos: custo do periodo do lote.\n\n")
        f.write("A seguir dados do modelo\n\n")
        f.write("Capacidade restante do modelo\n")
        f.write(capacidade_sobra.get_string())
        f.write("\n\nProdução total: ")
        f.write(str(int(prod_total)))
        f.write("\nCusto Total: ")
        f.write("${}".format(custo_total))


if __name__ == "__main__":
    capacidade, demanda, custo_producao, estoque, custo_estoque= importar_separar()
    custo_estoque= arrumar_estoque(custo_estoque)
    matriz_custo= criar_matriz_custo(custo_estoque, custo_producao)
    resposta, capacidade_sobra= metodo_transporte(matriz_custo, estoque, capacidade, demanda)
    tabela_resposta, tabela_cap= arrumando_respostas(resposta, capacidade_sobra)
    prod_total= sum([prod[2] for prod in resposta])
    custo_total= sum([prod[3] for prod in resposta])
    exportando_resultado(tabela_resposta, tabela_cap, prod_total, custo_total)
