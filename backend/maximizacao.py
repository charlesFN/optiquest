import numpy as np
import backend.tabular as tabular
import backend.bigM as bigM
import backend.grafico as grafico

def maximizacao(vetor_z, matriz_restricoes, plotar):
    vetor_z_inicial = vetor_z
    matriz_restricoes_inicial = matriz_restricoes

    linhas_totais = matriz_restricoes.shape[0]

    qtd_restricoes_igual = np.sum(matriz_restricoes == '=')
    qtd_restricoes_maior = np.sum(matriz_restricoes == '>=')

    if (qtd_restricoes_igual + qtd_restricoes_maior ) == 0:
        for i in range(linhas_totais):
            vetor_z = np.append(vetor_z,0)

        vetor_z = vetor_z * -1

        matriz = matriz_restricoes[:,:-2]
        matriz_identidade = np.eye(linhas_totais)

        matriz_esquerda = np.hstack([matriz,matriz_identidade]).astype(float)

        vetor_direito = np.take(matriz_restricoes, -1, axis=1).astype(float)

        if plotar == 0:
            tabular.metodo_tabular(vetor_z=vetor_z.astype(float),matriz_esquerda=matriz_esquerda,vetor_direito=vetor_direito,plotar=plotar)
        else:
            vetor_direito_final, idx_x1, idx_x2 = tabular.metodo_tabular(vetor_z=vetor_z.astype(float), matriz_esquerda=matriz_esquerda, vetor_direito=vetor_direito, plotar=plotar)
            grafico.plot(vetor_z=vetor_z_inicial, matriz_restricoes=matriz_restricoes_inicial, z_otimo=vetor_direito_final[0], x1=vetor_direito_final[idx_x1], x2=vetor_direito_final[idx_x2])
    else:
        vetor_vazio = np.empty((linhas_totais))

        matriz = matriz_restricoes[:,:-2]
        matriz_vazia = np.empty((linhas_totais,linhas_totais))

        for i in range(linhas_totais):
            tipo_restricao = matriz_restricoes[i,-2]

            if tipo_restricao == '<=':
                vetor_vazio[i] = 0

                for j in range(linhas_totais):
                    if i == j:
                        matriz_vazia[i,j] = 1
                    else:
                        matriz_vazia[i,j] = 0
            elif tipo_restricao == '=':
                vetor_vazio[i] = -100

                for j in range(linhas_totais):
                    if i == j:
                        matriz_vazia[i,j] = 1
                    else:
                        matriz_vazia[i,j] = 0
            elif tipo_restricao == '>=':
                vetor_vazio[i] = 0

                for j in range(linhas_totais):
                    if i == j:
                        matriz_vazia[i,j] = -1
                    else:
                        matriz_vazia[i,j] = 0

        # função Z multiplicada por -1
        # novo_vetor_z = np.hstack([vetor_z,vetor_vazio])
        novo_vetor_z = vetor_z
        # novo_vetor_z = novo_vetor_z * -1

        matriz_esquerda = np.hstack([matriz,matriz_vazia]).astype(float)
        
        vetor_direito = np.take(matriz_restricoes, -1, axis=1).astype(float)

        vetor_z_final = novo_vetor_z
        z_inicial = 0

        for i in range(linhas_totais):
            tipo_restricao = matriz_restricoes[i,-2]

            if tipo_restricao == '=':
                linha_igual = matriz_esquerda[i] * -100

                vetor_z_final = vetor_z_final + linha_igual

                z_inicial = z_inicial + (vetor_direito[i] * -100)

        if qtd_restricoes_maior > 0:
            matriz_vazia_ext = np.empty((linhas_totais,qtd_restricoes_maior))

            for i in range(linhas_totais):
                tipo_restricao = matriz_restricoes[i,-2]

                if tipo_restricao == '>=':
                    vetor_z_final = np.append(vetor_z_final,100)

                for j in range(qtd_restricoes_maior):
                    if j == i:
                        if tipo_restricao == '>=':
                            matriz_vazia_ext[i,j] = 1
                        else:
                            matriz_vazia_ext[i,j] = 0
                    else:
                        matriz_vazia_ext[i,j] = 0

            matriz_esquerda = np.hstack([matriz_esquerda,matriz_vazia_ext])

        for i in range(linhas_totais):
            tipo_restricao = matriz_restricoes[i,-2]

            if tipo_restricao == '>=':
                linha_maior_igual = matriz_esquerda[i] * -100

                vetor_z_final = vetor_z_final + linha_maior_igual

                z_inicial = z_inicial + (vetor_direito[i] * -100)

        if plotar == 0:
            bigM.metodo_bigM(vetor_z=vetor_z_final, matriz_esquerda=matriz_esquerda, vetor_direito=vetor_direito, z_inicial=z_inicial,tipo_operacao=0, plotar=plotar)
        else:
            vetor_direito_final, idx_x1, idx_x2 = bigM.metodo_bigM(vetor_z=vetor_z_final, matriz_esquerda=matriz_esquerda, vetor_direito=vetor_direito, z_inicial=z_inicial,tipo_operacao=0, plotar=plotar)
            grafico.plot(vetor_z=vetor_z_inicial, matriz_restricoes=matriz_restricoes_inicial, z_otimo=vetor_direito_final[0], x1=vetor_direito_final[idx_x1], x2=vetor_direito_final[idx_x2])