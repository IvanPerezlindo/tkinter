import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import psycopg2


root = tk.Tk()
root.title('Gestion')
root.resizable(0,0)

frame = ttk.Frame(root, padding=50)
frame.pack()

marca = StringVar()
modelo = StringVar()
year = StringVar()
precio = StringVar()

def chequear():
    if len(marca.get()) == 0:
        messagebox.showinfo('Advertencia','Complete el campo Marca')
        resetear()
    elif len(modelo.get()) == 0:
        messagebox.showinfo('Advertencia','Complete el campo Modelo')
        resetear()
    elif len(year.get()) == 0 or year.get() == StringVar: #ver que tire error si cargas string en esta casilla
        messagebox.showinfo('Advertencia','Complete el campo Año (Debe ser numerico)')
        resetear()
    elif len(precio.get()) == 0 or precio.get() == StringVar: #ver que tire error si cargas string en esta casilla
        messagebox.showinfo('Advertencia','Complete el campo Precio (Debe ser numerico)')
        resetear()
    else:
        pass

def resetear():
    marca.set('')
    modelo.set('')
    year.set('')
    precio.set('')

def guardar():

    chequear()
    con = psycopg2.connect(database="postgres", user="postgres", password="admin", host="127.0.0.1", port="5432")

    cur = con.cursor()
    insert_query = ('''INSERT INTO motos (marca, modelo, year, precio) VALUES (%s,%s,%s,%s)''')
    datosaGuardar = (marca.get(),modelo.get(),year.get(),precio.get(),)
    cur.execute(insert_query, datosaGuardar)
    con.commit()
    con.close()
    resetear()
    messagebox.showinfo('Gestor','Datos cargados correctamente')
    Mostrar()

def Mostrar():
    refresh()
    con = psycopg2.connect(database="postgres", user="postgres", password="admin", host="127.0.0.1", port="5432") #conexion a base de datos
    cur = con.cursor()
    cur.execute("SELECT * FROM motos")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    con.close()
    boton1.config(state="enabled")

def refresh(): #limpia los registros para que no se dupliquen los resultados. De paso sirve como boton de actualizar pantalla
    for i in tree.get_children():
        tree.delete(i)


tree= ttk.Treeview(frame, column=("column1", "column2", "column3", "column4", "column5"), show='headings')
tree.heading("#1", text="Marca")
tree.heading("#2", text="Modelo")
tree.heading("#3", text="Año")
tree.heading("#4", text="Precio")
tree.heading("#5", text="Id")
tree.pack()

#------------ SELECCIONAR-----------------------------
def seleccionar():
    try:
        global values
        selected = tree.focus()
        values = tree.item(selected, 'values')

        label1.delete(0, END) #limpia(delete) e inserta(insert) el valor seleccionado al label
        label1.insert(0, values[0])
        label2.delete(0, END)
        label2.insert(0, values[1])
        label3.delete(0, END)
        label3.insert(0, values[2])
        label4.delete(0, END)
        label4.insert(0, values[3])
        boton2.config(state="enabled")
        boton3.config(state="enabled")
    except:
        messagebox.showwarning('Advertencia','Seleccione una fila!')

#------------ ACTUALIZAR -----------------------------

def actualizar():
    try:
        con = psycopg2.connect(database="postgres", user="postgres", password="admin", host="127.0.0.1", port="5432")  
        cur = con.cursor()
        update_query = ('''UPDATE motos SET marca = %s, modelo = %s, year = %s, precio = %s WHERE Id = %s''')
        datosaActualizar = (label1.get(), label2.get(),label3.get(),label4.get(), values[4])
        cur.execute(update_query,datosaActualizar)
        con.commit()
        con.close()
        messagebox.showwarning('Actualizacion exitosa','La actualizacion fue exitosa!')
        resetear()
        Mostrar()
    except:
        messagebox.showwarning('Advertencia','Para actualizar debe seleccionar una fila!')

#------------ BORRAR -----------------------------
def borrar():
    resultado = messagebox.askyesno('Advertencia', 'Estas seguro de borrar ese articulo?')
    if resultado == True:
        try:
            con = psycopg2.connect(database="postgres", user="postgres", password="admin", host="127.0.0.1", port="5432")  
            cur = con.cursor()
            delete_query = ('''DELETE from motos WHERE Id = %s''')
            datosaBorrar = (values[4],)
            cur.execute(delete_query,datosaBorrar)
            con.commit()
            con.close()
            messagebox.showwarning('Borrar','Moto borrada!')
            resetear()
            Mostrar()
        except:
            messagebox.showwarning('Advertencia','Para borrar debe seleccionar una fila!')
    else:
        pass




ttk.Label(frame, text='Marca').pack()
label1=ttk.Entry(frame, textvariable=marca)
label1.pack()

ttk.Label(frame, text='Modelo').pack()
label2=ttk.Entry(frame, textvariable=modelo)
label2.pack()

ttk.Label(frame, text='Año').pack()
label3=ttk.Entry(frame, textvariable=year)
label3.pack()

ttk.Label(frame, text='Precio').pack()
label4=ttk.Entry(frame, textvariable=precio)
label4.pack()



ttk.Button(frame, text='Cargar Nueva Moto', command=guardar).pack(side=TOP)
ttk.Button(frame, text='Mostrar Motos', command=Mostrar).pack(side=TOP)
boton1=ttk.Button(frame, text='Seleccionar', state="disabled" , command=seleccionar)
boton1.pack(side=TOP)
boton2=ttk.Button(frame, text='Actualizar', state="disabled" , command=actualizar)
boton2.pack(side=TOP)
boton3=ttk.Button(frame, text='Borrar', state="disabled" , command=borrar)
boton3.pack(side=TOP)
ttk.Button(frame, text='Salir', command=root.destroy).pack(side=RIGHT)

mainloop()