import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Function to create the database and tables
def crear_base_datos():
    conexion = sqlite3.connect("empleados.db")
    cursor = conexion.cursor()

    # Create empleados table
    cursor.execute("""CREATE TABLE IF NOT EXISTS empleados (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        cargo TEXT,
                        salario TEXT,
                        cuenta_bancaria TEXT,
                        lugar_trabajo TEXT,
                        bonificaciones TEXT,
                        deducciones TEXT,
                        fecha_inicio TEXT,
                        igss TEXT)""")

    # Create facturas table
    cursor.execute("""CREATE TABLE IF NOT EXISTS facturas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        orden_compra TEXT,
                        serie_factura TEXT,
                        dte_no TEXT,
                        valor_factura REAL,
                        cliente TEXT,
                        fecha_facturacion TEXT,
                        fecha_pago TEXT,
                        contacto TEXT,
                        correo TEXT)""")

    conexion.commit()
    conexion.close()


# Function to start the application
def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    usuarios_validos = {
        "admin": "admin",
        "william": "william",
        "user": "user"
    }

    if usuarios_validos.get(usuario) == contrasena:
        ventana_login.destroy()
        abrir_sistema(usuario)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")


# Function to open the employee management system
def abrir_sistema(usuario):
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión de Empleados y Facturas")
    ventana.geometry("1200x800")
    ventana.resizable(True, True)

    style = ttk.Style()
    style.theme_use("clam")

    # Create notebook for tabs
    notebook = ttk.Notebook(ventana)
    notebook.pack(pady=10, expand=True, fill='both')

    # Create frames for tabs
    frame_empleados = ttk.Frame(notebook)
    frame_facturas = ttk.Frame(notebook)
    notebook.add(frame_empleados, text="Empleados")
    notebook.add(frame_facturas, text="Facturas")

    # ---- Pestaña CRUD para Empleados ----
    frame_formulario = ttk.Frame(frame_empleados, padding=(10, 10))
    frame_formulario.pack(pady=10)

    labels_texts = [
        "Nombre", "Cargo", "Salario", "Cuenta Bancaria",
        "Lugar de Trabajo", "Bonificaciones", "Deducciones",
        "Fecha Inicio de Labores", "Número de IGSS"
    ]
    entries = {}

    for i, text in enumerate(labels_texts):
        ttk.Label(frame_formulario, text=f"{text}:").grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
        entry = ttk.Entry(frame_formulario)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[text] = entry

    frame_botones = ttk.Frame(frame_empleados)
    frame_botones.pack(pady=10)

    tree = ttk.Treeview(frame_empleados,
                        columns=("ID", "Nombre", "Cargo", "Salario", "Cuenta", "Lugar", "Bonificaciones", "Deducciones",
                                 "Fecha Inicio", "IGSS"),
                        show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Cargo", text="Cargo")
    tree.heading("Salario", text="Salario")
    tree.heading("Cuenta", text="Cuenta Bancaria")
    tree.heading("Lugar", text="Lugar de Trabajo")
    tree.heading("Bonificaciones", text="Bonificaciones")
    tree.heading("Deducciones", text="Deducciones")
    tree.heading("Fecha Inicio", text="Fecha Inicio de Labores")
    tree.heading("IGSS", text="Número de IGSS")

    columns_config = {
        "ID": 50, "Nombre": 150, "Cargo": 100, "Salario": 100,
        "Cuenta": 150, "Lugar": 150, "Bonificaciones": 100,
        "Deducciones": 100, "Fecha Inicio": 150, "IGSS": 120
    }
    for col, width in columns_config.items():
        tree.column(col, width=width)

    tree.pack(pady=20, fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_empleados, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    ttk.Button(frame_botones, text="Agregar", command=lambda: crear_empleado(entries, tree)).grid(row=0, column=0,
                                                                                                  padx=10)
    ttk.Button(frame_botones, text="Actualizar", command=lambda: actualizar_empleado(entries, tree)).grid(row=0,
                                                                                                          column=1,
                                                                                                          padx=10)
    ttk.Button(frame_botones, text="Eliminar", command=lambda: eliminar_empleado(tree)).grid(row=0, column=2, padx=10)
    ttk.Button(frame_botones, text="Limpiar", command=lambda: limpiar_formulario(entries)).grid(row=0, column=3,
                                                                                                padx=10)

    tree.bind("<Double-1>", lambda event: cargar_empleado(tree, entries))
    listar_empleados(tree)

    # ---- Pestaña Facturas ----
    frame_facturas_formulario = ttk.Frame(frame_facturas, padding=(10, 10))
    frame_facturas_formulario.pack(pady=10)

    factura_labels = [
        "Orden de Compra", "Serie Factura", "DTE No.", "Valor de Factura",
        "Cliente", "Fecha de Facturación", "Fecha de Pago", "Contacto", "Correo"
    ]
    factura_entries = {}

    for i, text in enumerate(factura_labels):
        ttk.Label(frame_facturas_formulario, text=f"{text}:").grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
        entry = ttk.Entry(frame_facturas_formulario)
        entry.grid(row=i, column=1, padx=10, pady=5)
        factura_entries[text] = entry

    frame_facturas_botones = ttk.Frame(frame_facturas)
    frame_facturas_botones.pack(pady=10)

    factura_tree = ttk.Treeview(frame_facturas,
                                columns=("ID", "Orden de Compra", "Serie Factura", "DTE No.", "Valor de Factura",
                                         "Cliente", "Fecha de Facturación", "Fecha de Pago", "Contacto", "Correo"),
                                show="headings")
    factura_tree.heading("ID", text="ID")
    factura_tree.heading("Orden de Compra", text="Orden de Compra")
    factura_tree.heading("Serie Factura", text="Serie Factura")
    factura_tree.heading("DTE No.", text="DTE No.")
    factura_tree.heading("Valor de Factura", text="Valor de Factura")
    factura_tree.heading("Cliente", text="Cliente")
    factura_tree.heading("Fecha de Facturación", text="Fecha de Facturación")
    factura_tree.heading("Fecha de Pago", text="Fecha de Pago")
    factura_tree.heading("Contacto", text="Contacto")
    factura_tree.heading("Correo", text="Correo")

    factura_columns_config = {
        "ID": 50, "Orden de Compra": 150, "Serie Factura": 100, "DTE No.": 100,
        "Valor de Factura": 100, "Cliente": 150, "Fecha de Facturación": 150,
        "Fecha de Pago": 150, "Contacto": 150, "Correo": 150
    }
    for col, width in factura_columns_config.items():
        factura_tree.column(col, width=width)

    factura_tree.pack(pady=20, fill="both", expand=True)

    factura_scrollbar = ttk.Scrollbar(frame_facturas, orient="vertical", command=factura_tree.yview)
    factura_tree.configure(yscroll=factura_scrollbar.set)
    factura_scrollbar.pack(side="right", fill="y")

    ttk.Button(frame_facturas_botones, text="Agregar",
               command=lambda: crear_factura(factura_entries, factura_tree)).grid(row=0, column=0, padx=10)
    ttk.Button(frame_facturas_botones, text="Actualizar",
               command=lambda: actualizar_factura(factura_entries, factura_tree)).grid(row=0, column=1, padx=10)
    ttk.Button(frame_facturas_botones, text="Eliminar", command=lambda: eliminar_factura(factura_tree)).grid(row=0,
                                                                                                             column=2,
                                                                                                             padx=10)
    ttk.Button(frame_facturas_botones, text="Limpiar", command=lambda: limpiar_formulario(factura_entries)).grid(row=0,
                                                                                                                 column=3,
                                                                                                                 padx=10)

    factura_tree.bind("<Double-1>", lambda event: cargar_factura(factura_tree, factura_entries))
    listar_facturas(factura_tree)

    # If the user is not admin, disable some buttons
    if usuario != "admin":
        frame_botones.winfo_children()[0].config(state=tk.DISABLED)  # Agregar
        frame_botones.winfo_children()[2].config(state=tk.DISABLED)  # Eliminar

    ventana.mainloop()


# Functions for Employees CRUD
def crear_empleado(entries, tree):
    datos = {key: entry.get() for key, entry in entries.items()}

    if all(datos.values()):
        conexion = sqlite3.connect("empleados.db")
        cursor = conexion.cursor()
        cursor.execute("""INSERT INTO empleados (nombre, cargo, salario, cuenta_bancaria, 
                          lugar_trabajo, bonificaciones, deducciones, fecha_inicio, igss) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (datos["Nombre"], datos["Cargo"], datos["Salario"], datos["Cuenta Bancaria"],
                        datos["Lugar de Trabajo"], datos["Bonificaciones"], datos["Deducciones"],
                        datos["Fecha Inicio de Labores"], datos["Número de IGSS"]))
        conexion.commit()
        conexion.close()
        listar_empleados(tree)
        limpiar_formulario(entries)
        messagebox.showinfo("Éxito", "Empleado agregado correctamente")
    else:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")


def listar_empleados(tree):
    for row in tree.get_children():
        tree.delete(row)

    conexion = sqlite3.connect("empleados.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    conexion.close()

    for empleado in empleados:
        tree.insert("", "end", values=empleado)


def actualizar_empleado(entries, tree):
    try:
        seleccionado = tree.selection()[0]
        empleado = tree.item(seleccionado, 'values')
        id_empleado = empleado[0]

        datos = {key: entry.get() for key, entry in entries.items()}

        if all(datos.values()):
            conexion = sqlite3.connect("empleados.db")
            cursor = conexion.cursor()
            cursor.execute("""UPDATE empleados SET nombre = ?, cargo = ?, salario = ?, cuenta_bancaria = ?, 
                              lugar_trabajo = ?, bonificaciones = ?, deducciones = ?, fecha_inicio = ?, igss = ? 
                              WHERE id = ?""",
                           (*datos.values(), id_empleado))
            conexion.commit()
            conexion.close()
            listar_empleados(tree)
            limpiar_formulario(entries)
            messagebox.showinfo("Éxito", "Empleado actualizado correctamente")
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, seleccione un empleado")


def eliminar_empleado(tree):
    try:
        seleccionado = tree.selection()[0]
        empleado = tree.item(seleccionado, 'values')
        id_empleado = empleado[0]

        conexion = sqlite3.connect("empleados.db")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM empleados WHERE id = ?", (id_empleado,))
        conexion.commit()
        conexion.close()
        listar_empleados(tree)
        messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, seleccione un empleado")


def limpiar_formulario(entries):
    for entry in entries.values():
        entry.delete(0, tk.END)


def cargar_empleado(tree, entries):
    try:
        seleccionado = tree.selection()[0]
        empleado = tree.item(seleccionado, 'values')
        keys_list = list(entries.keys())
        for i, key in enumerate(keys_list):
            entries[key].delete(0, tk.END)
            entries[key].insert(0, empleado[i + 1])  # Skip the first column (ID)
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, seleccione un empleado")


# Functions for Invoices CRUD
def crear_factura(entries, tree):
    datos = {key: entry.get() for key, entry in entries.items()}

    if all(datos.values()):
        conexion = sqlite3.connect("empleados.db")
        cursor = conexion.cursor()
        cursor.execute("""INSERT INTO facturas (orden_compra, serie_factura, dte_no, valor_factura, cliente,
                          fecha_facturacion, fecha_pago, contacto, correo) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (datos["Orden de Compra"], datos["Serie Factura"], datos["DTE No."],
                        datos["Valor de Factura"], datos["Cliente"], datos["Fecha de Facturación"],
                        datos["Fecha de Pago"], datos["Contacto"], datos["Correo"]))
        conexion.commit()
        conexion.close()
        listar_facturas(tree)
        limpiar_formulario(entries)
        messagebox.showinfo("Éxito", "Factura agregada correctamente")
    else:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")


def listar_facturas(tree):
    for row in tree.get_children():
        tree.delete(row)

    conexion = sqlite3.connect("empleados.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM facturas")
    facturas = cursor.fetchall()
    conexion.close()

    for factura in facturas:
        tree.insert("", "end", values=factura)


def actualizar_factura(entries, tree):
    try:
        seleccionado = tree.selection()[0]
        factura = tree.item(seleccionado, 'values')
        id_factura = factura[0]

        datos = {key: entry.get() for key, entry in entries.items()}

        if all(datos.values()):
            conexion = sqlite3.connect("empleados.db")
            cursor = conexion.cursor()
            cursor.execute("""UPDATE facturas SET orden_compra = ?, serie_factura = ?, dte_no = ?, valor_factura = ?, 
                              cliente = ?, fecha_facturacion = ?, fecha_pago = ?, contacto = ?, correo = ? 
                              WHERE id = ?""",
                           (*datos.values(), id_factura))
            conexion.commit()
            conexion.close()
            listar_facturas(tree)
            limpiar_formulario(entries)
            messagebox.showinfo("Éxito", "Factura actualizada correctamente")
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, seleccione una factura")


def eliminar_factura(tree):
    try:
        seleccionado = tree.selection()[0]
        factura = tree.item(seleccionado, 'values')
        id_factura = factura[0]

        conexion = sqlite3.connect("empleados.db")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM facturas WHERE id = ?", (id_factura,))
        conexion.commit()
        conexion.close()
        listar_facturas(tree)
        messagebox.showinfo("Éxito", "Factura eliminada correctamente")
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, seleccione una factura")


def cargar_factura(tree, entries):
    try:
        seleccionado = tree.selection()[0]
        factura = tree.item(seleccionado, 'values')
        keys_list = list(entries.keys())
        for i, key in enumerate(keys_list):
            entries[key].delete(0, tk.END)
            entries[key].insert(0, factura[i + 1])  # Skip the first column (ID)
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, seleccione una factura")

# Main execution
if __name__ == "__main__":
    crear_base_datos()

    # Create login window
    ventana_login = tk.Tk()
    ventana_login.title("Login")
    ventana_login.geometry("300x200")

    ttk.Label(ventana_login, text="Usuario:").pack(pady=10)
    entry_usuario = ttk.Entry(ventana_login)
    entry_usuario.pack(pady=5)

    ttk.Label(ventana_login, text="Contraseña:").pack(pady=10)
    entry_contrasena = ttk.Entry(ventana_login, show="*")
    entry_contrasena.pack(pady=5)

    ttk.Button(ventana_login, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=20)

    ventana_login.mainloop()
