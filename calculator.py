import customtkinter as ctk
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Calculadora LV")
app.geometry("360x720")
app.resizable(False, False)

entrada = ctk.StringVar()
historico = []
taxa = ctk.StringVar(value="5.00")
modo_escuro = True
modo_cientifico_ativo = False

# === Funções ===

def adicionar(valor):
    entrada.set(entrada.get() + str(valor))

def limpar():
    entrada.set("")

def calcular():
    try:
        resultado = eval(entrada.get())
        historico.append(f"{entrada.get()} = {resultado}")
        entrada.set(str(resultado))
    except:
        entrada.set("Erro")

def mostrar_historico():
    janela = ctk.CTkToplevel(app)
    janela.title("Histórico")
    janela.geometry("300x300")
    texto = "\n".join(historico[-10:])
    ctk.CTkLabel(janela, text=texto).pack(padx=10, pady=10)

def converter_usd_brl():
    try:
        valor = float(entrada.get())
        taxa_valor = float(taxa.get())
        convertido = valor * taxa_valor
        entrada.set(f"{convertido:.2f} R$")
    except:
        entrada.set("Erro")

def converter_brl_usd():
    try:
        valor = float(entrada.get())
        taxa_valor = float(taxa.get())
        convertido = valor / taxa_valor
        entrada.set(f"{convertido:.2f} USD")
    except:
        entrada.set("Erro")

def alternar_tema():
    global modo_escuro
    modo_escuro = not modo_escuro
    if modo_escuro:
        ctk.set_appearance_mode("dark")
        tema_botao.configure(text="☀ Modo Claro")
    else:
        ctk.set_appearance_mode("light")
        tema_botao.configure(text="🌙 Modo Escuro")

# === Científico ===

def aplicar_funcao(func):
    try:
        valor = float(entrada.get())
        if func == "sqrt":
            resultado = math.sqrt(valor)
        elif func == "square":
            resultado = valor ** 2
        elif func == "sin":
            resultado = math.sin(math.radians(valor))
        elif func == "cos":
            resultado = math.cos(math.radians(valor))
        elif func == "log":
            resultado = math.log10(valor)
        entrada.set(str(round(resultado, 5)))
    except:
        entrada.set("Erro")

def toggle_modo_cientifico():
    global modo_cientifico_ativo
    modo_cientifico_ativo = not modo_cientifico_ativo
    if modo_cientifico_ativo:
        cientifico_frame.pack(pady=5, padx=10, fill="x")
        btn_cientifico.configure(text="− Modo Científico")
    else:
        cientifico_frame.pack_forget()
        btn_cientifico.configure(text="+ Modo Científico")

# === Interface ===

display = ctk.CTkEntry(app, textvariable=entrada, font=("Arial", 26), justify="right")
display.pack(padx=20, pady=20, fill="x")

ctk.CTkLabel(app, text="Taxa de câmbio (1 USD = ? BRL):").pack()
ctk.CTkEntry(app, textvariable=taxa).pack(pady=(0, 10), padx=20, fill="x")

botoes = [
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"]
]
operadores = {"÷": "/", "×": "*"}

for linha in botoes:
    linha_frame = ctk.CTkFrame(app)
    linha_frame.pack(pady=5, padx=10, fill="x")
    for item in linha:
        comando = (
            calcular if item == "=" else
            lambda x=item: adicionar(operadores.get(x, x))
        )
        ctk.CTkButton(
            linha_frame,
            text=item,
            command=comando,
            height=60,
            width=70
        ).pack(side="left", expand=True, padx=5)

# Extras
funcoes_frame = ctk.CTkFrame(app)
funcoes_frame.pack(pady=5, padx=10, fill="x")

ctk.CTkButton(funcoes_frame, text="Limpar", command=limpar, height=45).pack(side="left", expand=True, padx=5)
ctk.CTkButton(funcoes_frame, text="Histórico", command=mostrar_historico, height=45).pack(side="left", expand=True, padx=5)

conversor_frame = ctk.CTkFrame(app)
conversor_frame.pack(pady=5, padx=10, fill="x")

ctk.CTkButton(conversor_frame, text="US → R$", command=converter_usd_brl, height=45).pack(side="left", expand=True, padx=5)
ctk.CTkButton(conversor_frame, text="R$ → US", command=converter_brl_usd, height=45).pack(side="left", expand=True, padx=5)

tema_botao = ctk.CTkButton(app, text="☀ Modo Claro", command=alternar_tema)
tema_botao.pack(pady=5, padx=20, fill="x")

btn_cientifico = ctk.CTkButton(app, text="+ Modo Científico", command=toggle_modo_cientifico)
btn_cientifico.pack(pady=5, padx=20, fill="x")

# Modo Científico (inicialmente oculto)
cientifico_frame = ctk.CTkFrame(app)
funcoes = [("√", "sqrt"), ("x²", "square"), ("sin", "sin"), ("cos", "cos"), ("log", "log")]
for nome, func in funcoes:
    ctk.CTkButton(
        cientifico_frame,
        text=nome,
        command=lambda f=func: aplicar_funcao(f),
        height=45
    ).pack(side="left", expand=True, padx=5)

# Rodapé
ctk.CTkLabel(app, text="Desenvolvida por Lucas Vasques", font=("Arial", 10)).pack(pady=10)

# Teclado
def tecla_pressionada(event):
    key = event.keysym
    if key in "0123456789":
        adicionar(key)
        return "break"
    elif key == "Return":
        calcular()
        return "break"
    elif key in ("plus", "minus", "slash", "asterisk", "period"):
        map_keys = {"plus": "+", "minus": "-", "slash": "/", "asterisk": "*", "period": "."}
        adicionar(map_keys[key])
        return "break"
    elif key == "c":
        limpar()
        return "break"

app.bind("<Key>", tecla_pressionada)

app.mainloop()
