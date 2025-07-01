import numpy as np
import matplotlib.pyplot as plt

def plot(vetor_z, matriz_restricoes, z_otimo, x1, x2):
    matriz = np.delete(matriz_restricoes, -2, axis=1).astype(float)
    sinais = matriz_restricoes[:,-2]

    x = np.linspace(0, 100, 400)

    plt.figure(figsize=(10, 10))

    for i, (a, b, c) in enumerate(matriz):
        if b != 0:
            y = (c - a * x) / b
            plt.plot(x, y, label=f'Restrição {i+1}: {a}x + {b}y {sinais[i]} {c}')

            if sinais[i] == '<=': 
                plt.fill_between(x, y, plt.ylim()[0], color='blue', alpha=0.5)
            if sinais[i] == '>=':
                plt.fill_between(x, y, plt.ylim()[1], color='red', alpha=0.5)
        else:
            x_vertical = np.full_like(x, c / a)
            plt.plot(x_vertical, x, label=f'Restrição {i+1}:{a}x + {b}y {sinais[i]} {c}')

            if sinais[i] == '<=': 
                plt.fill_between(x, y, plt.ylim()[0], color='blue', alpha=0.5)
            if sinais[i] == '>=':
                plt.fill_between(x, y, plt.ylim()[1], color='red', alpha=0.5)

    

    for i in range(10):
        if i == 0:
            if vetor_z[1] != 0:
                y = (z_otimo - vetor_z[0] * x) / vetor_z[1]
                plt.plot(x, y, label=f'Z: {vetor_z[0]}x + {vetor_z[1]}y = {z_otimo}', color='black')
            else:
                x_vertical = np.full_like(x, z_otimo / vetor_z[0])
                plt.plot(x_vertical, x, label=f'Curva de Nível: {vetor_z[0]}x + {vetor_z[1]}y = {z_otimo}', color='black')
        else:
            fracao_z_otimo = (z_otimo / 10)

            if vetor_z[1] != 0:
                y = ((fracao_z_otimo * i) - vetor_z[0] * x) / vetor_z[1]
                plt.plot(x, y, label=f'Curva de Nível: {vetor_z[0]}x + {vetor_z[1]}y = {fracao_z_otimo * i}', color='black')
            else:
                x_vertical = np.full_like(x, (fracao_z_otimo * i) / vetor_z[0])
                plt.plot(x_vertical, x, label=f'Curva de Nível: {vetor_z[0]}x + {vetor_z[1]}y = {fracao_z_otimo * i}', color='black')

    plt.scatter(x1, x2, color='white', edgecolors='black', label=f'Z Ótimo = {z_otimo}', zorder=5)

    plt.axhspan(0, plt.ylim()[1], facecolor='black', alpha=0.5)
    plt.axvspan(0, plt.xlim()[1], facecolor='black', alpha=0.5)

    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title('Solução Gráfica')
    plt.grid(True)
    plt.legend()
    plt.xlim(0, 50)
    plt.ylim(0, 50)
    plt.show()