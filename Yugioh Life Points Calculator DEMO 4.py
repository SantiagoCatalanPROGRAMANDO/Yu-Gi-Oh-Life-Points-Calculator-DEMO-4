import random
import os
import sys
from tkinter import messagebox
import winsound
import tkinter as tk
from PIL import Image, ImageTk # type: ignore
from playsound import playsound
import threading

#---------------------------
# RUTA DE ARCHIVO
def ruta_archivo(nombre):

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, nombre)

    return os.path.join(os.path.abspath("."), nombre)


#---------------------------
# SONIDO DE FONDO
def musica_fondo():

    while True:

        playsound(
            ruta_archivo("bgsound.mp3")
        )
#---------------------------

#---------------------------
# SONIDOS DE GANAR/PERDER LP
def sonido_boton ():
    print("SONIDO")

    winsound.PlaySound(
        ruta_archivo("puntosvida.wav"),
        winsound.SND_ASYNC | winsound.SND_FILENAME
    )
#---------------------------

#---------------------------
# SONIDOS BOTONES PUNTOS DE VIDA
def sonido_botonlp():

    print("SONIDO")

    winsound.PlaySound(
        ruta_archivo("puntosvida.wav"),
        winsound.SND_ASYNC | winsound.SND_FILENAME
    )
#---------------------------

#---------------------------
# SONIDOS LANZAR MONEDA Y LANZAR DADO
def sonido_moneda():

    print("SONIDO")

    winsound.PlaySound(
        ruta_archivo("moneda.wav"),
        winsound.SND_ASYNC | winsound.SND_FILENAME
    )
def sonido_dado():

    print("SONIDO")

    winsound.PlaySound(
        ruta_archivo("dado.wav"),
        winsound.SND_ASYNC | winsound.SND_FILENAME
    )
#---------------------------

#---------------------------
# HISTORIAL DE PUNTOS DE VIDA
def agregar_historial(texto):

    historial.config(state="normal")

    historial.insert(tk.END, texto + "\n")

    historial.see(tk.END)

    historial.config(state="disabled")
#----------------------------

#----------------------------
# LANZAR UNA MONEDA y LANZAR DADO
def lanzar_moneda():
    sonido_moneda()
    resultado = random.choice(["CARA","CRUZ"])
    messagebox.showinfo("Moneda", f"Resultado: {resultado}")

#---------------------------
def lanzar_dado():
    sonido_dado()
    resultado = random.randint(1,6)
    messagebox.showinfo("Dado", f"Salió: {resultado}")
#--------------------------

#--------------------------
# VENTANA PRINCIPAL

ventana = tk.Tk()
historial = tk.Text(
    ventana,
    height=10,
    width=35,
    bg="black",
    fg="white",
    font=("Arial", 10)
)
historial.place(x=10, y=500)
threading.Thread(target=musica_fondo, daemon=True).start()
ventana.title("Yu-Gi-Oh Life Points Calculator DEMO 1.0")
ventana.geometry("1000x800")
ventana.configure(bg="black")
ventana.resizable(False, False)
tk.Button(
    ventana,
    text="LANZAR MONEDA",
    font=("Arial", 14, "bold"),
    bg="gold",
    fg="black",
    command=lanzar_moneda
).grid(row=2, column=0, sticky="ew")

tk.Button(
    ventana,
    text="LANZAR DADO",
    font=("Arial", 14, "bold"),
    bg="silver",
    fg="black",
    command=lanzar_dado
).grid(row=2, column=1, sticky="ew")
#--------------------------

#--------------------------
# DIVIDIR LA VENTANA EN 2 COLUMNAS IGUALES
ventana.grid_columnconfigure(0, weight=2)
ventana.grid_columnconfigure(1, weight=2)
ventana.grid_rowconfigure(0, weight=2)
#-------------------------

#-------------------------
# VARIABLES

vida1 = tk.IntVar(value=8000)
vida2 = tk.IntVar(value=8000)

duelo_terminado = False
#--------------------------

#--------------------------
# MITAD DE LP
def mitad1():
    if not duelo_terminado:
        vida1.set(vida1.get() // 2)
        agregar_historial(f"Duelista 1 dividió sus LP a la mitad.")
        print("SONIDO")
        winsound.PlaySound(
        ruta_archivo("puntosvida.wav"),
        winsound.SND_ASYNC | winsound.SND_FILENAME
        )  
        revisar_ganador()

def mitad2():
    if not duelo_terminado:
        vida2.set(vida2.get() // 2)
        agregar_historial(f"Duelista 2 dividió sus LP a la mitad")
        print("SONIDO")
        winsound.PlaySound(
        ruta_archivo("puntosvida.wav"),
        winsound.SND_ASYNC | winsound.SND_FILENAME
        )  
        revisar_ganador()
#-------------------------
# FUNCION DEL GANADOR
#-------------------------
def revisar_ganador():
    global duelo_terminado

    if duelo_terminado:
        return

    if vida1.get() <= 0:
        vida1.set(0)
        duelo_terminado = True
        messagebox.showinfo("DUELO TERMINADO", "GANADOR JUGADOR 2")

    elif vida2.get() <= 0:
        vida2.set(0)
        duelo_terminado = True
        messagebox.showinfo("DUELO TERMINADO", "GANADOR JUGADOR 1")

#-------------------------

#-------------------------
# JUGADOR 1
def sumar1(valor):
    if not duelo_terminado:
        sonido_boton()
        vida1.set(vida1.get() + valor)
        
        agregar_historial(f"Duelista 1 ganó {valor} LP")

def restar1(valor):
    if not duelo_terminado:
        sonido_boton()
        vida1.set(vida1.get() - valor)

        agregar_historial(f"Duelista 1 perdió {valor} LP")
        revisar_ganador()

#--------------------------

#--------------------------
# JUGADOR 2
def sumar2(valor):
    if not duelo_terminado:
        sonido_boton()
        vida2.set(vida2.get() + valor)

        agregar_historial(f"Duelista 2 ganó {valor} LP")

def restar2(valor):
    if not duelo_terminado:
        sonido_boton()
        vida2.set(vida2.get() - valor)

        agregar_historial(f"Duelista 2 perdió {valor} LP")
        revisar_ganador()

#-------------------------

#-------------------------
# REINICIAR EL DUELO
def reiniciar():
    global duelo_terminado
    historial.config(state="normal")
    historial.delete(1.0, tk.END)
    historial.config(state="disabled")
    vida1.set(8000)
    vida2.set(8000)
    duelo_terminado = False
#-------------------------

#--------------------------
# FRAMES
frame1 = tk.Frame(ventana, bg="red")
# FONDO PANEL ROJO
img_rojo = Image.open(ruta_archivo("1.png"))
img_rojo = img_rojo.resize((600, 700))   # ajustá según tamaño panel
foto_rojo = ImageTk.PhotoImage(img_rojo)

fondo_rojo = tk.Label(frame1, image=foto_rojo, bd=0)
fondo_rojo.place(x=0, y=0, relwidth=1, relheight=1)
frame2 = tk.Frame(ventana, bg="blue")
# FONDO PANEL AZUL
img_azul = Image.open(ruta_archivo("2.png"))
img_azul = img_azul.resize((600, 700))
foto_azul = ImageTk.PhotoImage(img_azul)

fondo_azul = tk.Label(frame2, image=foto_azul, bd=0)
fondo_azul.place(x=0, y=0, relwidth=1, relheight=1)

frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=1, sticky="nsew")
#-------------------------

#-------------------------
# JUGADOR 1
tk.Label(
    frame1,
    text="DUELISTA 1",
    bg="red",
    fg="white",
    font=("Impact", 22, "bold")
).pack(pady=10)

tk.Label(
    frame1,
    textvariable=vida1,
    bg="red",
    fg="white",
    font=("Impact", 30, "bold")
).pack(pady=15)

botones1 = tk.Frame(frame1, bg="red")
botones1.pack(pady=10)

tk.Button(botones1, text="+1000", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: sumar1(1000)).grid(row=0, column=0, padx=5, pady=5)

tk.Button(botones1, text="-1000", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: restar1(1000)).grid(row=0, column=1, padx=5, pady=5)

tk.Button(botones1, text="+500", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: sumar1(500)).grid(row=1, column=0, padx=5, pady=5)

tk.Button(botones1, text="-500", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: restar1(500)).grid(row=1, column=1, padx=5, pady=5)

tk.Button(botones1, text="+100", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: sumar1(100)).grid(row=2, column=0, padx=5, pady=5)

tk.Button(botones1, text="-100", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: restar1(100)).grid(row=2, column=1, padx=5, pady=5)

tk.Button(botones1, text="+50", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: sumar1(50)).grid(row=3, column=0, padx=5, pady=5)

tk.Button(botones1, text="-50", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: restar1(50)).grid(row=3, column=1, padx=5, pady=5)

tk.Button(botones1, text="HALF LP", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=mitad1).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

#-------------------------

#-------------------------
# JUGADOR 2
tk.Label(
    frame2,
    text="DUELISTA 2",
    bg="orange",
    fg="white",
    font=("Impact", 22, "bold")
).pack(pady=10)

tk.Label(
    frame2,
    textvariable=vida2,
    bg="orange",
    fg="white",
    font=("Impact", 30, "bold")
).pack(pady=15)

botones2 = tk.Frame(frame2, bg="orange")
botones2.pack(pady=10)

tk.Button(botones2, text="+1000", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: sumar2(1000)).grid(row=0, column=0, padx=5, pady=5)

tk.Button(botones2, text="-1000", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: restar2(1000)).grid(row=0, column=1, padx=5, pady=5)

tk.Button(botones2, text="+500", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: sumar2(500)).grid(row=1, column=0, padx=5, pady=5)

tk.Button(botones2, text="-500", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: restar2(500)).grid(row=1, column=1, padx=5, pady=5)

tk.Button(botones2, text="+100", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: sumar2(100)).grid(row=2, column=0, padx=5, pady=5)

tk.Button(botones2, text="-100", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: restar2(100)).grid(row=2, column=1, padx=5, pady=5)

tk.Button(botones2, text="+50", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: sumar2(50)).grid(row=3, column=0, padx=5, pady=5)

tk.Button(botones2, text="-50", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=lambda: restar2(50)).grid(row=3, column=1, padx=5, pady=5)

tk.Button(botones2, text="HALF LP", width=10, height=2,
          font=("Calibri", 13, "bold"),
          command=mitad2).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

#-------------------------

#-------------------------
# BOTON PARA REINICIAR EL DUELO
tk.Button(
    ventana,
    text="REINICIAR EL DUELO",
    font=("Arial", 14, "bold"),
    bg="black",
    fg="white",
    command=reiniciar
).grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

historial = tk.Text(
    ventana,
    height=8,
    width=40,
    bg="black",
    fg="cyan",
    font=("Consolas", 10, "bold"),
    state="disabled"
)

historial.place(x=350, y=574)

#-------------------------
#-------------------------
# EJECUTAR APLICACION
#-------------------------
ventana.mainloop()