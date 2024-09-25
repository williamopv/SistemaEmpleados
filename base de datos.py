def crear_base_datos():
    conexion = sqlite3.connect("empleados.db")
    cursor = conexion.cursor()
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
