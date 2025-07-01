import numpy as np
import backend.funcoes as func

def metodo_tabular(vetor_z, matriz_esquerda, vetor_direito):
    iteracao = 0
    quantidade_negativos = np.sum(vetor_z < 0)

    while (quantidade_negativos > 0):

        # índice da coluna pivô é encontrado pegando o valor mais negativo da nova_linha_z e pegando o seu índice
        indice_coluna_pivo = np.argmin(vetor_z)

        # coluna pivô é encontrada chamando a função coluna_pivo(), que recebe como argumentos:
            # a matriz que representa o lado esquerdo da restrição
            # o índice da coluna pivô
        coluna_pivo = func.coluna_pivo(matriz_esquerda, indice_coluna=indice_coluna_pivo)
        #print("Coluna pivô:\n", coluna_pivo, "\n")

        # após encontrarmos a coluna pivô, dividimos a matriz que representa o lado direito da restrição pela coluna pivô
        if iteracao == 0:
            divisao_colunas = vetor_direito / coluna_pivo
        else:
            novo_vetor_direito = vetor_direito[1:]
            divisao_colunas = novo_vetor_direito / coluna_pivo

        indices_nao_negativos = np.where(divisao_colunas >= 0)[0]

        indice_linha_pivo = indices_nao_negativos[np.argmin(divisao_colunas[indices_nao_negativos])]

        # o algarismo pivô é encontrado chamando a função item_pivo(), que recebe como argumentos:
            # a matriz que representa o lado esquerdo da restrição
            # o índice da linha pivô
            # o índice da coluna pivô
        pivo = func.item_pivo(matriz_esquerda, indice_linha_pivo, indice_coluna_pivo)
        #print("Número pivô:\n", pivo, "\n")

        # com o algarismo pivô tendo sido encontrado, o próximo passo é dividir a linha pivô por ele mesmo, de modo que agora o elemento pivô seja 1.
        # a divisão é feita pela função dividir_linha_pivo(), que recebe como argumentos:
            # a matriz que representa o lado esquerdo da restrição
            # o índice da linha pivô
            # o divisor
        matriz_esquerda, vetor_direito = func.dividir_linha_pivo(matriz_esquerda, vetor_direito=vetor_direito, indice_linha=indice_linha_pivo, divisor=pivo, iteracao=iteracao)
        #print("Matriz do lado Esquerdo das Restrições com a Linha Pivô Dividida pelo Algarismo Pivô:\n", matriz_esquerda, "\n")

        if iteracao == 0:
            vetor_direito = np.insert(vetor_direito, 0, 0)

        # por fim, devemos somar a linha pivô com as outras linhas da matriz, de modo que os elementos da coluna pivô das outras linhas fique igual a 0.
        # isso é feito pela função anular_coluna_pivo(), que recebe como argumentos():
            # a matriz que representa o lado esquerdo da restrição, com a linha pivô modificada
            # o índice da linha pivô
            # o índice da coluna pivô
        vetor_z, matriz_esquerda, vetor_direito = func.anular_coluna_pivo(vetor_z, matriz_esquerda=matriz_esquerda, vetor_direito=vetor_direito, indice_linha=indice_linha_pivo, indice_coluna=indice_coluna_pivo)
        print("Vetor Z com os Elementos da Coluna Pivô Nulos:\n", vetor_z, "\n")
        print("Matriz do lado Esquerdo das Restrições com os Elementos da Coluna Pivô Nulos (Exceto o da Linha Pivô):\n", matriz_esquerda, "\n")
        print("Vetor Direito Com Valores Atualizados:\n", vetor_direito, "\n")

        iteracao += 1
        quantidade_negativos = np.sum(vetor_z < 0)