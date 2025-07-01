import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

import backend.main as back

# Configurações
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def criar_campos():
    global entradas_objetivo, entradas_restricoes

    # Limpar campos antigos
    for widget in frame_objetivo.winfo_children():
        widget.destroy()
    for widget in frame_restricoes.winfo_children():
        widget.destroy()

    entradas_objetivo = []
    entradas_restricoes = []

    try:
        num_var = int(entrada_num_var.get())
        num_rest = int(entrada_num_rest.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira números válidos.")
        return

    # Função objetivo
    for i in range(num_var):
        label = ctk.CTkLabel(frame_objetivo, text=f"x{i+1}:", font=ctk.CTkFont(size=16))
        label.grid(row=0, column=i*2, padx=5, pady=5)
        entry = ctk.CTkEntry(frame_objetivo, width=60)
        entry.grid(row=0, column=i*2+1, padx=5, pady=5)
        entradas_objetivo.append(entry)

    # Restrições
    for j in range(num_rest):
        linha = []
        for i in range(num_var):
            entry = ctk.CTkEntry(frame_restricoes, width=60)
            entry.grid(row=j, column=i*2, padx=5, pady=5)
            linha.append(entry)
            label = ctk.CTkLabel(frame_restricoes, text=f"x{i+1}", font=ctk.CTkFont(size=14))
            label.grid(row=j, column=i*2+1, padx=2, pady=5)
        entrada_sinal = ctk.CTkOptionMenu(frame_restricoes, values=["<=", ">=", "="])
        entrada_sinal.grid(row=j, column=num_var*2, padx=5, pady=5)
        entrada_valor = ctk.CTkEntry(frame_restricoes, width=60)
        entrada_valor.grid(row=j, column=num_var*2+1, padx=5, pady=5)
        linha.append(entrada_sinal)
        linha.append(entrada_valor)
        entradas_restricoes.append(linha)

def coletar_dados():
    try:
        tipo = tipo_var.get()
        funcao_obj = [float(entry.get()) for entry in entradas_objetivo]
        restricoes = []
        for linha in entradas_restricoes:
            coeficientes = [float(entry.get()) for entry in linha[:-2]]
            sinal = linha[-2].get()
            valor = float(linha[-1].get())
            restricoes.append((coeficientes, sinal, valor))
        return tipo, funcao_obj, restricoes
    except Exception as e:
        messagebox.showerror("Erro", f"Verifique os campos preenchidos! {e}")
        return None

def resolver_simplex():
    dados = coletar_dados()
    if dados:
        tipo, funcao_obj, restricoes = dados
        back.resolucao(tipo=tipo, funcao_obj=funcao_obj, restricoes=restricoes, plotar=0)

def resolver_simplex_inteiro():
    dados = coletar_dados()
    if dados:
        tipo, funcao_obj, restricoes = dados
        messagebox.showinfo("Simplex Inteiro", f"Tipo: {tipo}\nFunção: {funcao_obj}\nRestrições: {restricoes}")

def resolver_simplex_dual():
    dados = coletar_dados()
    if dados:
        tipo, funcao_obj, restricoes = dados
        messagebox.showinfo("Simplex Dual", f"Tipo: {tipo}\nFunção: {funcao_obj}\nRestrições: {restricoes}")

def plotar_regiao():
    dados = coletar_dados()
    if dados:
        tipo, funcao_obj, restricoes = dados
        back.resolucao(tipo=tipo, funcao_obj=funcao_obj, restricoes=restricoes, plotar=1)

# Criar janela principal
janela = ctk.CTk()
janela.title("Método Simplex")
janela.geometry("1200x850")
janela.resizable(False, False)

# Imagem de fundo
bg_image = ctk.CTkImage(light_image=Image.open("ca.png"), size=(1200, 850))
label_fundo = ctk.CTkLabel(janela, image=bg_image, text="")
label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

# Título
titulo = ctk.CTkLabel(janela, text="Método Simplex", text_color="green", font=ctk.CTkFont(size=30, weight="bold"))
titulo.pack(pady=20)

# Frame de configurações
frame_setup = ctk.CTkFrame(janela, fg_color="transparent")
frame_setup.pack(pady=10)

label_num_var = ctk.CTkLabel(frame_setup, text="Número de Variáveis:", font=ctk.CTkFont(size=16))
label_num_var.grid(row=0, column=0, padx=5)
entrada_num_var = ctk.CTkEntry(frame_setup, width=50)
entrada_num_var.grid(row=0, column=1, padx=5)

label_num_rest = ctk.CTkLabel(frame_setup, text="Número de Restrições:", font=ctk.CTkFont(size=16))
label_num_rest.grid(row=0, column=2, padx=5)
entrada_num_rest = ctk.CTkEntry(frame_setup, width=50)
entrada_num_rest.grid(row=0, column=3, padx=5)

btn_criar = ctk.CTkButton(frame_setup, text="Criar Campos", command=criar_campos)
btn_criar.grid(row=0, column=4, padx=10)

# Tipo de problema
tipo_var = ctk.StringVar(value="Maximizar")
label_tipo = ctk.CTkLabel(janela, text="Tipo de Problema:", font=ctk.CTkFont(size=18))
label_tipo.pack(pady=10)
tipo_menu = ctk.CTkOptionMenu(janela, variable=tipo_var, values=["Maximizar", "Minimizar"])
tipo_menu.pack()

# Frames para função objetivo e restrições
frame_objetivo = ctk.CTkFrame(janela, fg_color="transparent")
frame_objetivo.pack(pady=20)

frame_restricoes = ctk.CTkFrame(janela, fg_color="transparent")
frame_restricoes.pack(pady=20)

# Botões de ações
frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
frame_botoes.pack(pady=30)

btn_resolver_normal = ctk.CTkButton(frame_botoes, text="Resolver Simplex Normal", command=resolver_simplex, width=250)
btn_resolver_normal.grid(row=0, column=0, padx=10, pady=5)

btn_resolver_inteiro = ctk.CTkButton(frame_botoes, text="Resolver Simplex Inteiro", command=resolver_simplex_inteiro, width=250)
btn_resolver_inteiro.grid(row=0, column=1, padx=10, pady=5)

btn_resolver_dual = ctk.CTkButton(frame_botoes, text="Resolver Simplex Dual", command=resolver_simplex_dual, width=250)
btn_resolver_dual.grid(row=1, column=0, padx=10, pady=5)

btn_plotar = ctk.CTkButton(frame_botoes, text="Plotar Região de Viabilidade", command=plotar_regiao, width=250)
btn_plotar.grid(row=1, column=1, padx=10, pady=5)

# Rodar a janela
janela.mainloop()
