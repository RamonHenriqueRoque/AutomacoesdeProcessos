"""
RAMON HENRIQUE ROQUE 758958
"""

import pandas as pd
import numpy as np
import math
from prettytable import PrettyTable
import typing
import warnings
warnings.filterwarnings("ignore")

def exportar_separar() -> pd.DataFrame:
    
    """
    Nessa função tem o objetivo de importar os dados de um arquivo json e 
    retorna seus resultados em um DataFrame.

    Returns
    -------
    DataFrame
        Importando_dados: Retorna os dados no arquivo.
    """
    base= pd.read_json("Dados do algoritmo Programa mestre.txt")
    base= base.reset_index().rename({"index": "Periodo"}, axis= 1) 
    return(base)


def maximo(linha: pd.DataFrame) -> pd.Series:
    """
    Nessa função compara duas colunas e retorna o maior numero da linha.

    Parameters
    ----------
    linha : pd.DataFrame
        Base que vamos analisar.

    Returns
    -------
    pd.Series
        Nova coluna dos comparativos dos maiores valores.
    """

    return(max(linha["Prev de dem Ind"], linha["Pedidos em carteira"]))

def demanda_total(df: pd.DataFrame) -> pd.DataFrame:
    """
    Criando a coluna demanda_total.

    Parameters
    ----------
    df : pd.DataFrame
        Base de dados.

    Returns
    -------
    pd.DataFrame
        Retorna a base + a coluna da demanda total.
    """

    df["Demanda Total"]= df.apply(maximo, axis= 1)
    return(df)

def estrategia_l4l(base: pd.DataFrame, estoque_seg: int) -> pd.DataFrame:
    """
    Temos a estrategia lote para lote.

    Parameters
    ----------
    base : pd.DataFrame
        base de dados.
    estoque_seg : int
        Se o sistema requer um estoque de segurança.

    Returns
    -------
    Retorna a coluna estoque, MSP e disponivel para promessa em relação ao tempo.

    """
    base["MPS"]= 0
    
    for id in base.index[1:]:
        
        # Caso o estoque seja superior à demanda e o estoque segurança
        if base["Estoque"][id - 1] >= base["Demanda Total"][id] + estoque_seg:
            base["MPS"][id]= 0
            base["Estoque"][id]= base["Estoque"][id - 1] - base["Demanda Total"][id] + estoque_seg
        
        # Caso o estoque seja inferior 
        else:
            base["MPS"][id]= base["Demanda Total"][id] - base["Estoque"][id - 1] + estoque_seg
            base["Estoque"][id]= base["MPS"][id] + base["Estoque"][id - 1] - base["Demanda Total"][id]
            
    return(disponivel_para_promessa(base))

def estrategia_lote_fixo(base: pd.DataFrame, multiplo: int, estoque_seg: int) -> pd.DataFrame:
    """
    Temos a estrategia lote fixo.

    Parameters
    ----------
    base : pd.DataFrame
        Base de dados.
    multiplo:
        Se a produção tem um lote fixo que sera definido aqui o seu tamanho.
    estoque_seg : int
        Se o sistema requer um estoque de segurança.

    Returns
    -------
    Retorna a coluna estoque, MSP e disponivel para promessa em relação ao tempo.
    """
    base["MPS"]= 0
    
    for id in base.index[1:]:
        # Caso o estoque seja superior à demanda e o estoque segurança
        if base["Estoque"][id - 1] >= base["Demanda Total"][id] + estoque_seg:
            base["MPS"][id]= 0
            base["Estoque"][id]= base["Estoque"][id - 1] - base["Demanda Total"][id]
        
        # Caso o estoque seja inferior 
        else:
            quant_falta= base["Demanda Total"][id] - base["Estoque"][id - 1]
            cts= math.ceil((estoque_seg + quant_falta)/multiplo)
            
            base["MPS"][id]= cts*multiplo
            base["Estoque"][id]= base["MPS"][id] + base["Estoque"][id - 1] - base["Demanda Total"][id]
    return(disponivel_para_promessa(base))


def estrategia_lote_minimo(base: pd.DataFrame, lmin: int, estoque_seg: int) -> pd.DataFrame:
    """
    Temos a estrategia lote minimo.

    Parameters
    ----------
    base : pd.DataFrame
        Base de dados.
    lmin : TYPE, optional
        Valor minimo que o lote permite.
    estoque_seg : TYPE, optional
        Se o sistema requer um estoque de segurança.

    Returns
    -------
    Retorna a coluna estoque, MSP e disponivel para promessa em relação ao tempo.

    """    
    base["MPS"]= 0
    
    for id in base.index[1:]:
        # Caso o estoque seja superior à demanda e o estoque segurança
        if base["Estoque"][id - 1] >= base["Demanda Total"][id] + estoque_seg:
            base["MPS"][id]= 0
            base["Estoque"][id]= base["Estoque"][id - 1] - base["Demanda Total"][id]
        
        # Caso o estoque seja inferior 
        else:
            quant_falta= base["Demanda Total"][id] - base["Estoque"][id - 1]
            
            if quant_falta <= lmin:
                base["MPS"][id]= lmin
                base["Estoque"][id]= base["MPS"][id] + base["Estoque"][id - 1] - base["Demanda Total"][id]
            else:
                base["MPS"][id]= quant_falta
                base["Estoque"][id]= base["MPS"][id] + base["Estoque"][id - 1] - base["Demanda Total"][id]
    return(disponivel_para_promessa(base))

def estrategia_lote_maximo(base: pd.DataFrame, lmax: int, estoque_seg: int) -> pd.DataFrame:
    """
    Temos a estrategia lote maximo.

    Parameters
    ----------
    base : pd.DataFrame
        Base de dados.
    lmax : TYPE, optional
        Limite que a produção consiga produzir.
    estoque_seg : TYPE, optional
        Se o sistema requer um estoque de segurança.

    Returns
    -------
    Retorna a coluna estoque, MSP e disponivel para promessa em relação ao tempo.

    """
    base["MPS"]= 0
    
    for id in base.index[1:]:
        # Caso o estoque seja superior à demanda e o estoque segurança
        if base["Estoque"][id - 1] >= base["Demanda Total"][id] + estoque_seg:
            base["MPS"][id]= 0
            base["Estoque"][id]= base["Estoque"][id - 1] - base["Demanda Total"][id]
        
        # Caso o estoque seja inferior 
        else:
            quant_falta= base["Demanda Total"][id] - base["Estoque"][id - 1] + estoque_seg
            
            if quant_falta > lmax:
                base["MPS"][id]= lmax
                base["Estoque"][id]= estoque_seg
            else:
                base["MPS"][id]= quant_falta
                base["Estoque"][id]= base["MPS"][id] + base["Estoque"][id - 1] - base["Demanda Total"][id]
    return(disponivel_para_promessa(base))

def estrategia_cobertura_periodo(base: pd.DataFrame, quant_periodo: int, estoque_seg: int) -> pd.DataFrame:
    """
    Temos a estrategia lote maximo.

    Parameters
    ----------
    base : pd.DataFrame
        Base de dados..
    quant_periodo : TYPE, optional
        A janela de periodos que vamos produzir no tempo i.
    estoque_seg : TYPE, optional
        Se o sistema requer um estoque de segurança.

    Returns
    -------
    Retorna a coluna estoque, MSP e disponivel para promessa em relação ao tempo.

    """
    base["MPS"]= 0
    
    # Separar e somar a demanda dos periodos
    demanda= base["Demanda Total"].to_list()[2:]
    soma_demanda= [sum(demanda[i:quant_periodo+i]) for i in range(len(demanda)) if i % quant_periodo == 0]
    
    producao_periodo= [id for id in range(2, base.shape[0], quant_periodo)]
    cont= 0
    
    for id in base.index[1:]:
        
        if id == 1:
            # Caso o estoque seja superior à demanda e o estoque segurança
            if base["Estoque"][0] >= base["Demanda Total"][1] + estoque_seg:
                base["MPS"][1]= 0
                base["Estoque"][1]= base["Estoque"][0] - base["Demanda Total"][1]
            
            # Caso o estoque seja inferior 
            else:
                base["MPS"][1]= base["Demanda Total"][1] - base["Estoque"][0] + estoque_seg
                base["Estoque"][1]= base["MPS"][1] + base["Estoque"][0] - base["Demanda Total"][id]      
       
        elif id in producao_periodo:
            estoque_minimo= [estoque_seg - base["Estoque"][id - 1] if estoque_seg >= base["Estoque"][id - 1] else 0][0]
            base["MPS"][id]= soma_demanda[cont] + estoque_minimo
            base["Estoque"][id]= base["MPS"][id] + base["Estoque"][id - 1] - base["Demanda Total"][id]
            
            cont += 1
        
        else:
            base["MPS"][id]= 0
            base["Estoque"][id]= base["Estoque"][id - 1] - base["Demanda Total"][id]
   
        
    return(disponivel_para_promessa(base))

def disponivel_para_promessa(base: pd.DataFrame) -> pd.DataFrame:
    """
    Cria uma coluna disponivel para promessa e faz a conta.

    Parameters
    ----------
    base : pd.DataFrame
        Base de dados.

    Returns
    -------
    Base de dados com a coluna disponivel para a promesso preenchida.

    """
    base["Disponivel para a promessa"] = 0
    
    for id in base.index[1:]:
        if id == 1:       
            dpp= base["MPS"][1] + base['Estoque'][0] - base["Pedidos em carteira"][1]
            if dpp < 0:
                base["Disponivel para a promessa"][1]= 0
            else:
                base["Disponivel para a promessa"][1]= dpp
            
        else:
            dpp=  base["MPS"][id]-base["Pedidos em carteira"][id]
            # Caso o valor ser negativo
            if dpp < 0:
                cont= 1
                while True:
                    atri= ["Cont" if base["Disponivel para a promessa"][id - cont] + dpp < 0 else  base["Disponivel para a promessa"][id - cont] + dpp][0]
                    if atri == "Cont":
                        base["Disponivel para a promessa"][id - cont]= 0
                        dpp= base["Disponivel para a promessa"][id - cont] + dpp
                        cont += 1
                    else:
                        base["Disponivel para a promessa"][id - 1]= atri
                        break
            else:
                base["Disponivel para a promessa"][id]= dpp
    
    
    return(base)

def arrumando_respostas(exercicio: pd.DataFrame) -> str:
    """
    Transforma uma tabela em string.

    Parameters
    ----------
    exercicio : pd.DataFrame
        base de dados.

    Returns
    -------
    str
        Texto em tabela.

    """
    
    # exercicio
    estrutura_tabela= PrettyTable()
    estrutura_tabela.field_names= ['Periodo', 
                                   'Prev de dem Ind', 
                                   'Pedidos em carteira', 
                                   'Estoque', 
                                   'Demanda Total',
                                   "Disponivel para a promessa",
                                   'MPS']
    
    for id in exercicio.index:
        estrutura_tabela.add_row([exercicio["Periodo"][id], 
                                  exercicio["Prev de dem Ind"][id], 
                                  exercicio["Pedidos em carteira"][id], 
                                  exercicio["Estoque"][id],
                                  exercicio["Demanda Total"][id],
                                  exercicio["Disponivel para a promessa"][id],
                                  exercicio["MPS"][id]])
        
    return(estrutura_tabela.get_string())


def importando_resultado(lista_ex: list):
    """
    Criamos um documento com as respostas dos exercicios.

    Parameters
    ----------
    lista_ex : list
        [Nome do exercicio, DataFrame do exercicio].
    """
    with open('Resultados do algoritmo de Programacao Mestre.txt','w') as f:
        f.write("Abaixo apresenta os resultados do algoritmo da lista passado em aula. \n\n\n")
        
        for exercicio in lista_ex:
            f.write(exercicio[0])
            f.write("\n")
            f.write(arrumando_respostas(exercicio[1]))
            f.write("\n"*2)
       
if __name__ == "__main__":
    base= exportar_separar()
    base= demanda_total(base)
    
    ex_a= estrategia_l4l(base.copy(), estoque_seg= 50)
    ex_b= estrategia_lote_fixo(base.copy(), multiplo= 120, estoque_seg= 50)
    ex_c= estrategia_l4l(base.copy(), estoque_seg= 80)
    ex_d= estrategia_lote_fixo(base.copy(), multiplo= 70, estoque_seg= 20)
    ex_e= estrategia_lote_minimo(base.copy(), lmin= 100, estoque_seg= 0)
    ex_f= estrategia_cobertura_periodo(base.copy(), quant_periodo= 2, estoque_seg= 20)
    ex_g= estrategia_cobertura_periodo(base.copy(), quant_periodo= 3, estoque_seg= 20)
    bonus= estrategia_lote_maximo(base.copy(), lmax= 100, estoque_seg= 50)
    
    lists_ex= [["ex_a - Estrategia L4L com estoque de segurança de 50", ex_a],
               ["ex_b - Estrategia lote fixo com estoque de segurança de 50 e multiplo de 120", ex_b],
               ["ex_c - Estrategia L4L com estoque de segurança de 80", ex_c],
               ["ex_d - Estrategia lote fixo com estoque de segurança de 70 e multiplo de 20", ex_d],
               ["ex_e - Estrategia lote minimo de 100", ex_e],
               ["ex_f - Estrategia cobertura com 2 periodos e estoque de segurança de 20", ex_f],
               ["ex_g - Estrategia cobertura com 2 periodos e estoque de segurança de 20", ex_g],
               ["bonus - Estrategia lote maximo com estoque de segurança de 50", bonus]]
    importando_resultado(lists_ex)