import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def mostrar():
    for item in tree.get_children():
        tree.delete(item)
    cone = sqlite3.connect('tareas.db')
    cur = cone.cursor()
    cur.execute('SELECT id_tareas, titulo, descripcion, prioridad, estado, fecha_inicio FROM tareas')
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row + ("Borrar",))


def enviar():
    cone = sqlite3.connect('tareas.db')
    cur = cone.cursor()
    titulotx=titulo.get()
    textareatx=textarea.get("1.0",tk.END).strip()
    prioridadtx= prioridad.get()
    cur.execute('INSERT INTO tareas (titulo, descripcion, prioridad) VALUES (?, ?, ?)',(titulotx,textareatx, prioridadtx))
    cone.commit()
    messagebox.showinfo('exito','el mensaje se a guardado con exito')
    mostrar()

def borrar(id_tareas):
    cone = sqlite3.connect('tareas.db')
    cur = cone.cursor()
    cur.execute('DELETE FROM TAREAS WHERE id_tareas = ?'(id_tareas,))
    cone.commit()

def onclik(event):
    item= tree.identify_row(event.y)
    if item:
        col = tree.identify_row(event.x)
        if col == '#7':
            values = tree.item(item,'values')
            id_tareas = values[0]
            borrar(id_tareas)
            
ventana = tk.Tk()
ventana.geometry('800x900')
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

prioridadlabel = tk.Label(frame, text='prioridad:')
prioridadlabel.grid(row=2, column=0, padx=5)

prioridad = ttk.Combobox(frame, state="readonly", values=["Importante","No muy importante","Puede esperar"])
prioridad.grid(row=2, column=1, padx=5, pady=5)

boton = tk.Button(frame, text='enviar', command=enviar)
boton.grid(row=3, column=1, padx=5)

tree = ttk.Treeview(ventana, columns=('id', 'titulo', 'descripcion', 'prioridad', 'estado', 'fecha_inicio','borrar'), show='headings', height=80)
tree.heading("id", text="id")
tree.heading("titulo", text="titulo")
tree.heading("descripcion", text="descripcion")
tree.heading("prioridad", text="prioridad")
tree.heading("estado", text="estado")
tree.heading("fecha_inicio", text="fecha_inicio")
tree.heading("borrar",text="borrar")

tree.column("id",width=50)
tree.column('titulo', width=80)
tree.column('descripcion', width=90)
tree.column('prioridad', width=80)
tree.column('estado', width=80)
tree.column('fecha_inicio', width=100)
tree.column('borrar', width=80)

tree.bind('<ButtonRelease-1>', onclik)

tree.grid(row=1, column=1, padx=5, pady=5, columnspan=2)


mostrar()
ventana.mainloop()