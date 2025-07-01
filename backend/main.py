import numpy as np
import backend.maximizacao as max
import backend.minimizacao as min
import backend.grafico as grafico

def resolucao(tipo, funcao_obj, restricoes, plotar):
    if tipo == 'Maximizar':
        tipo_operacao = 0
    else:
        tipo_operacao = 1

    vetor_z = funcao_obj

    restricoes_desempacotadas = [(*tupla[0], *tupla[1:]) for tupla in restricoes]

    lista_restricoes = [list(tupla) for tupla in restricoes_desempacotadas]

    matriz_restricoes = np.array(lista_restricoes)

    plotar_grafico = plotar

    if tipo_operacao == 0:
        max.maximizacao(vetor_z=vetor_z, matriz_restricoes=matriz_restricoes, plotar=plotar_grafico)
    elif tipo_operacao == 1:
        min.minimizacao(vetor_z=vetor_z, matriz_restricoes=matriz_restricoes, plotar=plotar_grafico)