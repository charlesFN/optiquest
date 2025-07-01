import numpy as np
import backend.funcoes as func

def metodo_bigM(vetor_z, matriz_esquerda, vetor_direito, z_inicial, tipo_operacao, plotar):
    iteracao = 0
    quantidade_negativos = np.sum(vetor_z < 0)

    matrizes = []
    matrizes.append(matriz_esquerda)

    variaveis_h = np.array([])
    variaveis_v = np.array([])

    for i in range(vetor_z.size):
        variaveis_h = np.append(variaveis_h, f"x{i+1}")

    vetor_z_expandido = np.vstack((variaveis_h, vetor_z))

    qtd_linhas = matriz_esquerda.shape[0]
    for i in range(qtd_linhas):
        variaveis_v = np.append(variaveis_v, f"x{vetor_z.size - ((qtd_linhas - 1) - i)}")

    matriz_esquerda_expandida = np.hstack((variaveis_v[:, np.newaxis], matriz_esquerda))

    print("Z Expandido:\n", vetor_z_expandido, "\n")
    print("Matriz Esquerda Expandida:\n", matriz_esquerda_expandida, "\n")

    while (quantidade_negativos > 0):
        indice_coluna_pivo = np.argmin(vetor_z)

        coluna_pivo = func.coluna_pivo(matriz_esquerda, indice_coluna=indice_coluna_pivo)

        if iteracao == 0:
            divisao_colunas = vetor_direito / coluna_pivo
        else:
            novo_vetor_direito = vetor_direito[1:]
            divisao_colunas = novo_vetor_direito / coluna_pivo

        indices_nao_negativos = np.where(divisao_colunas >= 0)[0]

        indice_linha_pivo = indices_nao_negativos[np.argmin(divisao_colunas[indices_nao_negativos])]

        pivo = func.item_pivo(matriz_esquerda, indice_linha_pivo, indice_coluna_pivo)

        matriz_esquerda, vetor_direito = func.dividir_linha_pivo(matriz_esquerda, vetor_direito=vetor_direito, indice_linha=indice_linha_pivo, divisor=pivo, iteracao=iteracao)

        if iteracao == 0:
            vetor_direito = np.insert(vetor_direito, 0, z_inicial)

        vetor_z, matriz_esquerda, vetor_direito = func.anular_coluna_pivo(vetor_z, matriz_esquerda=matriz_esquerda, vetor_direito=vetor_direito, indice_linha=indice_linha_pivo, indice_coluna=indice_coluna_pivo)

        iteracao += 1
        quantidade_negativos = np.sum(vetor_z < 0)

        if quantidade_negativos == 0:
            if tipo_operacao == 1:
                vetor_z = vetor_z * -1
                vetor_direito[0] = vetor_direito[0] * -1

        z_expandido = np.vstack((variaveis_h, vetor_z))

        variaveis_v[indice_linha_pivo] = variaveis_h[indice_coluna_pivo]

        esquerda_expandida = np.hstack((variaveis_v[:, np.newaxis], matriz_esquerda))

        print("Vetor Z com os Elementos da Coluna Pivô Nulos:\n", z_expandido, "\n")
        print("Matriz do lado Esquerdo das Restrições com os Elementos da Coluna Pivô Nulos (Exceto o da Linha Pivô):\n", esquerda_expandida, "\n")
        print("Vetor Direito Com Valores Atualizados:\n", vetor_direito, "\n")

    if plotar == 1:
        idx_x1 = np.where(esquerda_expandida == 'x1')[0][0]
        idx_x2 = np.where(esquerda_expandida == 'x2')[0][0]

        return vetor_direito, idx_x1 + 1, idx_x2 + 1