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
        tree.insert("", tk.END, values=row + ("Actualizar", "Borrar"))
    cone.close()

def enviar():
    cone = sqlite3.connect('tareas.db')
    cur = cone.cursor()
    titulotx = titulo.get()
    textareatx = textarea.get("1.0", tk.END).strip()
    prioridadtx = prioridad.get()
    cur.execute('INSERT INTO tareas (titulo, descripcion, prioridad) VALUES (?, ?, ?)', (titulotx, textareatx, prioridadtx))
    cone.commit()
    messagebox.showinfo('Éxito', 'El mensaje se ha guardado con éxito')
    cone.close()
    mostrar()

def borrar(id_tareas):
    cone = sqlite3.connect('tareas.db')
    cur = cone.cursor()
    cur.execute('DELETE FROM tareas WHERE id_tareas = ?', (id_tareas,))
    cone.commit()
    mostrar()
    cone.close()

def actualizar(id_tareas):
    actu = tk.Toplevel(ventana)
    actu.title("actualizar")
    cone = sqlite3.connect('tareas.db')
    cur = cone.cursor()
    cur.execute('SELECT titulo, descripcion, prioridad, estado FROM tareas WHERE id_tareas = ?', (id_tareas,))
    tarea = cur.fetchone()
    if not tarea:
        messagebox.showerror("Error", "No se encontró la tarea.")
        return
        
    titulotx, textareatx, prioridadtx, estadotx = tarea

    # Campos para actualizar la tarea
    titulolabel = tk.Label(actu, text='Título:')
    titulolabel.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

    titulo_entry = tk.Entry(actu, font=('Arial', 12))
    titulo_entry.grid(row=0, column=1, padx=10, pady=5)
    titulo_entry.insert(0, titulotx)

    textarealabel = tk.Label(actu, text='Descripción:')
    textarealabel.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

    textarea_entry = tk.Text(actu, height=5, width=30)
    textarea_entry.grid(row=1, column=1, padx=10, pady=5)
    textarea_entry.insert("1.0", textareatx)

    prioridadlabel = tk.Label(actu, text='Prioridad:')
    prioridadlabel.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

    prioridad_entry = ttk.Combobox(actu, state="readonly", values=["Importante", "No muy importante", "Puede esperar"], font=('Arial', 12))
    prioridad_entry.grid(row=2, column=1, padx=10, pady=5)
    prioridad_entry.set(prioridadtx)

    estadolabel = tk.Label(actu, text='estado:')
    estadolabel.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

    estado= ttk.Combobox(actu, state="readonly", values=["pendiente", "completado"], font=('Arial', 12))
    estado.grid(row=3, column=1, padx=10, pady=5)
    estado.set(estadotx)

    def guardar_cambios():
        nuevo_titulo = titulo_entry.get()
        nueva_descripcion = textarea_entry.get("1.0", tk.END).strip()
        nueva_prioridad = prioridad_entry.get()
        estadon = estado.get()

        cone = sqlite3.connect('tareas.db')
        cur = cone.cursor()
        cur.execute('UPDATE tareas SET titulo = ?, descripcion = ?, prioridad = ?, estado = ? WHERE id_tareas = ?',
                    (nuevo_titulo, nueva_descripcion, nueva_prioridad, estadon, id_tareas))
        cone.commit()
        cone.close()
        mostrar()
        actu.destroy()

    boton_guardar = tk.Button(actu, text='Guardar', command=guardar_cambios)
    boton_guardar.grid(row=4, column=0, padx=10, pady=10, sticky=tk.E)

def onclik(event):
    item = tree.identify_row(event.y)
    if item:
        col = tree.identify_column(event.x)
        if col == '#8':
            values = tree.item(item, 'values')
            id_tareas = values[0]
            borrar(id_tareas)
            messagebox.showinfo('Éxito', 'El mensaje se ha Borrardo con éxito')
        elif col == '#7':
            values = tree.item(item, 'values')
            id_tareas = values[0]
            actualizar(id_tareas)




ventana = tk.Tk()
ventana.geometry('1300x500')
ventana.title("Aplicación de Tareas")

main_frame = tk.Frame(ventana)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

left_frame = tk.Frame(main_frame, padx=20, pady=20)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

titulolabel = tk.Label(left_frame, text='Título:')
titulolabel.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

titulo = tk.Entry(left_frame, font=('Arial', 12))
titulo.grid(row=0, column=1, padx=10, pady=5)

textarealabel = tk.Label(left_frame, text='Descripción:')
textarealabel.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

textarea = tk.Text(left_frame, height=5, width=30)
textarea.grid(row=1, column=1, padx=10, pady=5)

prioridadlabel = tk.Label(left_frame, text='Prioridad:')
prioridadlabel.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

prioridad = ttk.Combobox(left_frame, state="readonly", values=["Importante", "No muy importante", "Puede esperar"], font=('Arial', 12))
prioridad.grid(row=2, column=1, padx=10, pady=5)

boton = tk.Button(left_frame, text='Enviar', command=enviar)
boton.grid(row=3, column=1, padx=10, pady=10, sticky=tk.E)

tree_scroll = tk.Scrollbar(right_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(right_frame, columns=('id', 'titulo', 'descripcion', 'prioridad', 'estado', 'fecha_inicio', 'actualizar', 'borrar'), show='headings', height=20, yscrollcommand=tree_scroll.set)
tree.heading("id", text="ID")
tree.heading("titulo", text="Título")
tree.heading("descripcion", text="Descripción")
tree.heading("prioridad", text="Prioridad")
tree.heading("estado", text="Estado")
tree.heading("fecha_inicio", text="Fecha de Inicio")
tree.heading("actualizar", text="Actualizar")
tree.heading("borrar", text="Borrar")

tree.column("id", width=30)
tree.column('titulo', width=80)
tree.column('descripcion', width=120)
tree.column('prioridad', width=100)
tree.column('estado', width=80)
tree.column('fecha_inicio', width=100)
tree.column('actualizar', width=80)
tree.column('borrar', width=80)

tree.bind('<ButtonRelease-1>', onclik)

tree.pack(fill=tk.BOTH, expand=True)
tree_scroll.config(command=tree.yview)

mostrar()
ventana.mainloop()