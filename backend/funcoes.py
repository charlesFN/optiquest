import numpy as np

# a função coluna_pivo() recebe a matriz e o índice da coluna
# através da função np.take, que possui os argumentos:
    # axis: indica de qual eixo nós iremos retirar os valores (0: eixo x, 1: eixo y)
    # indices: indica qual índice da linha ou coluna será removido
# com isso, conseguimos retornar a nossa coluna pivô
def coluna_pivo(matriz, indice_coluna):
    return np.take(matriz, indices=indice_coluna, axis=1)

#encontra o item pivô do array esquerdo das restrições
def item_pivo(matriz, indice_linha, indice_coluna):
    # criamos um objeto com as mesmas dimensões da matriz
    indexadores = [slice(None)] * matriz.ndim

    # preenche o objeto com o índice da linha e coluna onde se encontra o elemento pivô
    indexadores[0] = indice_linha
    indexadores[1] = indice_coluna

    #retorna o elemento da matriz que se encontra no índice informado pelo objeto indexador
    return matriz[tuple(indexadores)]

# a função dividir_linha_pivo() recebe a matriz, o índice da linha pivô, e o divisor
def dividir_linha_pivo(matriz_esquerda, vetor_direito, indice_linha, divisor, iteracao):
    matriz_esquerda[indice_linha] = matriz_esquerda[indice_linha] / divisor

    if iteracao == 0:
        vetor_direito[indice_linha] = vetor_direito[indice_linha] / divisor
    else:
        vetor_direito[indice_linha+1] = vetor_direito[indice_linha+1] / divisor

    return matriz_esquerda, vetor_direito

# a função anular_coluna_pivo() recebe a matriz, o índice da linha pivô, e o índice da coluna pivô
def anular_coluna_pivo(vetor_z, matriz_esquerda, vetor_direito, indice_linha, indice_coluna):
    # pega a quantidade total de linhas da matriz
    linhas_totais = matriz_esquerda.shape[0]

    # pega a linha pivô
    linha_pivo = np.take(matriz_esquerda, indices=indice_linha, axis=0)


    valor_atual_vetor_z = np.take(vetor_z, indices=indice_coluna)
    # pega o valor da coluna pivô da linha pivô
    pivo = np.take(linha_pivo, indices=indice_coluna, axis=1 if linha_pivo.ndim > 1 else 0)

    multiplicador_vetor_z = -valor_atual_vetor_z / pivo

    vetor_z = vetor_z + (linha_pivo * multiplicador_vetor_z)

    pivo_vetor_direito_z = np.take(vetor_direito, indices=indice_linha+1)
    vetor_direito[0] = vetor_direito[0] + (pivo_vetor_direito_z * multiplicador_vetor_z)

    # inicia um loop com n iterações, baseada na quantidade de linhas da matriz
    for i in range(linhas_totais):
        # se a iteração for igual ao índice da linha pivô, nada será feito
        if i == indice_linha:
            continue

        # pega a linha equivalente a iteração atual
        linha_atual = np.take(matriz_esquerda, indices=i, axis=0)

        # pega o valor da coluna pivô na linha da iteração atual
        valor_atual = np.take(linha_atual, indices=indice_coluna, axis=1 if linha_atual.ndim > 1 else 0)
        # pega o valor da coluna pivô da linha pivô
        pivo = np.take(linha_pivo, indices=indice_coluna, axis=1 if linha_pivo.ndim > 1 else 0)

        # não faz nada caso o número que irá servir como divisor seja igual a zero
        if np.allclose(pivo, 0):
            continue

        # transforma o valor da coluna pivô na linha da iteração atual em um número negativo, e o divide pelo valor da coluna pivô da linha pivô
        # assim, teremos um multiplicador negativo que ao multiplicar pela linha pivô e somar com a linha da iteração atual
        # fará com que o número da coluna pivô da linha da iteração atual fique igual a zero
        multiplicador = -valor_atual / pivo

        valor_atual_vetor_direito = np.take(vetor_direito, indices=i+1)
        pivo_vetor_direito = np.take(vetor_direito, indices=indice_linha+1)

        vetor_direito[i+1] = valor_atual_vetor_direito + (pivo_vetor_direito * multiplicador)

        # multiplica a linha pivô pelo multiplicador negativo
        linha_pivo_modificada = linha_pivo * multiplicador

        # soma a linha pivô modificada com a linha da iteração atual
        linha_atual_modificada = linha_atual + linha_pivo_modificada

        # cria um objeto com as dimensões da matriz
        # armazena o índice da linha atual dentro do objeto
        # substitui a linha atual na matriz, pela sua versão modificada
        indexadores = [slice(None)] * matriz_esquerda.ndim
        indexadores[0] = i
        matriz_esquerda[tuple(indexadores)] = linha_atual_modificada

    return vetor_z, matriz_esquerda, vetor_direito