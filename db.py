import sqlite3

DB_PATH = 'construccion.db'

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def guardar_casa(nombre, fecha_creacion=None, observaciones=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO casa (nombre, fecha_creacion, observaciones) VALUES (?, ?, ?)",
        (nombre, fecha_creacion, observaciones)
    )
    casa_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return casa_id

def guardar_habitacion(nombre, ancho, largo, altura, id_casa):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO habitacion (nombre, ancho, largo, altura, id_casa) VALUES (?, ?, ?, ?, ?)",
        (nombre, ancho, largo, altura, id_casa)
    )
    habitacion_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return habitacion_id

def obtener_habitaciones_por_casa(id_casa):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre, ancho, largo, altura FROM habitacion WHERE id_casa = ?",
        (id_casa,)
    )
    habitaciones = cursor.fetchall()
    conn.close()
    return habitaciones

def guardar_material(nombre, precio_m2, tipo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO material (nombre, precio_m2, tipo) VALUES (?, ?, ?)",
        (nombre, precio_m2, tipo)
    )
    material_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return material_id

def obtener_materiales():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio_m2, tipo FROM material")
    materiales = cursor.fetchall()
    conn.close()
    return materiales

def guardar_sistema_construccion(nombre, factor_costo, descripcion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sistema_construccion (nombre, factor_costo, descripcion) VALUES (?, ?, ?)",
        (nombre, factor_costo, descripcion)
    )
    sistema_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return sistema_id

def obtener_sistemas_construccion():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, factor_costo, descripcion FROM sistema_construccion")
    sistemas = cursor.fetchall()
    conn.close()
    return sistemas

def guardar_habitacion_material(id_habitacion, id_material_piso, id_material_paredes, id_sistema_construccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO habitacion_material (id_habitacion, id_material_piso, id_material_paredes, id_sistema_construccion) VALUES (?, ?, ?, ?)",
        (id_habitacion, id_material_piso, id_material_paredes, id_sistema_construccion)
    )
    rel_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return rel_id

def obtener_materiales_habitacion(id_habitacion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_material_piso, id_material_paredes, id_sistema_construccion FROM habitacion_material WHERE id_habitacion = ?",
        (id_habitacion,)
    )
    datos = cursor.fetchone()
    conn.close()
    return datos
