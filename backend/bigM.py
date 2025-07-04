import numpy as np
import backend.funcoes as func

import customtkinter as ctk

def metodo_bigM(vetor_z, matriz_esquerda, vetor_direito, z_inicial, tipo_operacao, plotar):
    if plotar == 0:
        global scrollable_frame, visualizador
        visualizador = ctk.CTk()
        visualizador.title("Resultados")
        visualizador.geometry("1280x720")

        scrollable_frame = ctk.CTkScrollableFrame(visualizador, width=1920, height=1080)
        scrollable_frame.pack(pady=20)

        # Garante que a janela carregue antes de começar o loop
        visualizador.after(100, lambda: calcular(vetor_z, matriz_esquerda, vetor_direito, z_inicial, tipo_operacao, plotar))
        visualizador.mainloop()
    else:
        vetor_direito, idx_x1, idx_x2 = calcular(vetor_z, matriz_esquerda, vetor_direito, z_inicial, tipo_operacao, plotar)

        return vetor_direito, idx_x1, idx_x2

def exibir_tabela_resultado(vetor_z, matriz_esquerda, vetor_direito):
    tabela = ctk.CTkFrame(scrollable_frame)
    tabela.pack(pady=15)

    for i in range(vetor_z.shape[0]):
        label_var = ctk.CTkLabel(tabela, text="Variáveis", width=70, height=30, corner_radius=4)
        label_var.grid(row=0, column=0, padx=5, pady=5)

        label_z = ctk.CTkLabel(tabela, text="Z", width=50, height=30, corner_radius=4)
        label_z.grid(row=1, column=0, padx=5, pady=5)

        for j in range(vetor_z.shape[1]):
            cell = ctk.CTkLabel(tabela, text=str(vetor_z[i, j]), width=50, height=30, corner_radius=4)
            cell.grid(row=i, column=j + 1, padx=5, pady=5)

    linha_offset = matriz_esquerda.shape[0]

    for i in range(matriz_esquerda.shape[0]):
        for j in range(matriz_esquerda.shape[1]):
            cell = ctk.CTkLabel(tabela, text=str(matriz_esquerda[i, j]), width=50, height=30, corner_radius=4)
            cell.grid(row=linha_offset + i, column=j, padx=5, pady=5)

    resultados = matriz_esquerda.shape[1] 

    label_resultados = ctk.CTkLabel(tabela, text="Resultados", width=80, height=30, corner_radius=4)
    label_resultados.grid(row=0, column=resultados, padx=5, pady=5)

    cell = ctk.CTkLabel(tabela, text=str(vetor_direito[0]), width=80, height=30, corner_radius=4)
    cell.grid(row=1, column=resultados, padx=5, pady=5)

    for i in range(len(matriz_esquerda)):
        cell = ctk.CTkLabel(tabela, text=str(vetor_direito[i + 1]), width=80, height=30, corner_radius=4)
        cell.grid(row=linha_offset + i, column=resultados, padx=5, pady=5)

def calcular(vetor_z, matriz_esquerda, vetor_direito, z_inicial, tipo_operacao, plotar):
    iteracao = 0
    quantidade_negativos = np.sum(vetor_z < 0)

    variaveis_h = np.array([])
    variaveis_v = np.array([])

    for i in range(vetor_z.size):
        variaveis_h = np.append(variaveis_h, f"x{i+1}")

    qtd_linhas = matriz_esquerda.shape[0]
    for i in range(qtd_linhas):
        variaveis_v = np.append(variaveis_v, f"x{vetor_z.size - ((qtd_linhas - 1) - i)}")

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

        matriz_esquerda, vetor_direito = func.dividir_linha_pivo(matriz_esquerda=matriz_esquerda, vetor_direito=vetor_direito, indice_linha=indice_linha_pivo, divisor=pivo, iteracao=iteracao)

        if iteracao == 0:
            vetor_direito = np.insert(vetor_direito, 0, z_inicial)

        vetor_z, matriz_esquerda, vetor_direito = func.anular_coluna_pivo(vetor_z=vetor_z, matriz_esquerda=matriz_esquerda, vetor_direito=vetor_direito, indice_linha=indice_linha_pivo, indice_coluna=indice_coluna_pivo)

        iteracao += 1
        quantidade_negativos = np.sum(vetor_z < 0)

        if quantidade_negativos == 0:
            if tipo_operacao == 1:
                vetor_z = vetor_z * -1
                vetor_direito[0] = vetor_direito[0] * -1

        z_expandido = np.vstack((variaveis_h, vetor_z))

        variaveis_v[indice_linha_pivo] = variaveis_h[indice_coluna_pivo]

        esquerda_expandida = np.hstack((variaveis_v[:, np.newaxis], matriz_esquerda))

        if plotar == 0:
            exibir_tabela_resultado(vetor_z=z_expandido, matriz_esquerda=esquerda_expandida, vetor_direito=vetor_direito)
            visualizador.update()

    if plotar == 1:
        idx_x1 = np.where(esquerda_expandida == 'x1')[0][0]
        idx_x2 = np.where(esquerda_expandida == 'x2')[0][0]

        return vetor_direito, idx_x1 + 1, idx_x2 + 1