import flask_login
from flask import Flask, url_for, redirect, request, render_template, session, jsonify, flash
import mysql.connector
from mysql.connector import Error
import hashlib
from contextlib import contextmanager

@contextmanager
def conexion_db():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        database='indenetwork'
    )
    try:
        yield connection
    finally:
        connection.close()

def get_current_user_id():
    return session.get('miembroLogueado')

def obtener_lista_miembros():
    with conexion_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id_estudiante, nombre_estudiante, apellido_estudiante FROM estudiantes")
        return cursor.fetchall()

def obtener_amigo_por_defecto(miembros):
    return miembros[0][0] if miembros else None

def obtener_nombre_amigo(amigo_id):
    if amigo_id:
        with conexion_db() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT nombre_estudiante, apellido_estudiante FROM estudiantes WHERE id_estudiante = %s", (amigo_id,))
            amigo = cursor.fetchone()
            return amigo[0], amigo[1] if amigo else ("", "")
    return "", ""

def obtener_mensajes(miembro_actual, amigo_id, page=1, per_page=20):
    offset = (page - 1) * per_page
    with conexion_db() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT fk_miembro1, contenido_mensaje, fechaHora_mensaje 
            FROM MENSAJES 
            WHERE (fk_miembro1 = %s AND fk_miembro2 = %s)
                OR (fk_miembro1 = %s AND fk_miembro2 = %s)
            ORDER BY fechaHora_mensaje DESC
            LIMIT %s OFFSET %s
        """, (miembro_actual, amigo_id, amigo_id, miembro_actual, per_page, offset))
        return cursor.fetchall()[::-1]  

def insertar_mensaje(fk_miembro1, amigo_id, contenido_mensaje):
    with conexion_db() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO MENSAJES (fk_miembro1, fk_miembro2, contenido_mensaje) VALUES (%s, %s, %s)',
                (fk_miembro1, amigo_id, contenido_mensaje)
            )
            connection.commit()
        except Error as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()

def amigos_chat():
    miembro_actual = get_current_user_id()
    if not miembro_actual:
        return redirect(url_for('login_route'))

    miembros = obtener_lista_miembros()
    amigo_id = request.args.get('amigo_id', type=int) or obtener_amigo_por_defecto(miembros)
    amigo_nombre, amigo_apellido = obtener_nombre_amigo(amigo_id)
    mensajes = obtener_mensajes(miembro_actual, amigo_id) if amigo_id else []

    # Formatear los mensajes para el frontend
    mensajes_formateados = []
    for mensaje in mensajes:
        tipo = 'sent' if mensaje[0] == miembro_actual else 'received'
        mensajes_formateados.append({
            'tipo': tipo,
            'contenido': mensaje[1],
            'fecha': mensaje[2].strftime("%Y-%m-%d %H:%M:%S")
        })

    return render_template('amigos_chat.html', miembros=miembros, mensajes=mensajes_formateados, 
                            amigo_nombre=amigo_nombre, amigo_apellido=amigo_apellido, 
                            amigo_actual=amigo_id, miembro_actual=miembro_actual)

def enviar_mensaje(amigo_id):
    if request.method == 'POST':
        fk_miembro1 = get_current_user_id()
        if not fk_miembro1:
            return jsonify({"success": False, "message": "No se ha iniciado sesión"}), 401
        
        contenido_mensaje = request.form['Enter_mensaje']
        
        if not amigo_id or not contenido_mensaje:
            return jsonify({"success": False, "message": "Datos incompletos"}), 400

        try:
            insertar_mensaje(fk_miembro1, amigo_id, contenido_mensaje)
            return jsonify({"success": True, "message": "Mensaje enviado correctamente."})
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return jsonify({"success": False, "message": f"Error al enviar el mensaje: {err}"}), 500
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({"success": False, "message": f"Error inesperado: {str(e)}"}), 500

def obtener_nuevos_mensajes(amigo_id):
    miembro_actual = get_current_user_id()
    if not miembro_actual:
        return jsonify({"success": False, "message": "No se ha iniciado sesión"}), 401

    ultimo_timestamp = request.args.get('ultimo_timestamp')

    with conexion_db() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT fk_miembro1, contenido_mensaje, fechaHora_mensaje 
            FROM MENSAJES 
            WHERE ((fk_miembro1 = %s AND fk_miembro2 = %s) OR (fk_miembro1 = %s AND fk_miembro2 = %s))
            AND fechaHora_mensaje > %s
            ORDER BY fechaHora_mensaje ASC
        """, (miembro_actual, amigo_id, amigo_id, miembro_actual, ultimo_timestamp))
        
        nuevos_mensajes = cursor.fetchall()
    return jsonify({"success": True, "messages": nuevos_mensajes})