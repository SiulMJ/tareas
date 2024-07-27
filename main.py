import tkinter as tk
from tkinter import messagebox
import sqlite3

def enviar():
    cone = sqlite3.connect('tareas.db')
    cur = cone.cursor()
    titulotx=titulo.get()
    textareatx=textarea.get("1.0",tk.END).strip()
    cur.execute('INSERT INTO tareas (titulo, descripcion) VALUES (?, ?)',(titulotx,textareatx))
    cone.commit()
    messagebox.showinfo('exito','el mensaje se a guardado con exito')


ventana = tk.Tk()
ventana.geometry('400x300')
ventana.title("Aplicación de Tareas")

frame = tk.Frame()
frame.grid(pady=20)

titulolabel = tk.Label(frame, text='Titulo:')
titulolabel.grid(row=0, column=0 ,padx=5)

titulo = tk.Entry(frame)
titulo.grid(row=0, column=1, padx=5, pady=5)

textarealabel = tk.Label(frame, text='decripcion:')
textarealabel.grid(row=1, column=0, padx=5)

textarea = tk.Text(frame, height=5, width=30)
textarea.grid(row=1, column=1, padx=5, pady=5)

boton = tk.Button(frame, text='enviar', command=enviar)
boton.grid(row=2, column=1, padx=5)

ventana.mainloop()