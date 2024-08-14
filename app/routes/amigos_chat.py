import flask_login
from flask import Flask, url_for, redirect, request, render_template, session, jsonify, flash
import mysql.connector, hashlib

# Configuración de la base de datos
def conexion_db():
    global mydb, cursor
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        database='indenetwork'
    )
    cursor = mydb.cursor()


# Funciones auxiliares
def obtener_lista_miembros():
    cursor.execute(
        "SELECT id_estudiante, nombre_estudiante, apellido_estudiante FROM estudiantes")
    return cursor.fetchall()


def obtener_amigo_por_defecto(miembros):
    return miembros[0][0] if miembros else None


def obtener_nombre_amigo(amigo_id):
    if amigo_id:
        cursor.execute(
            "SELECT nombre_estudiante, apellido_estudiante FROM estudiantes WHERE id_estudiante = %s", (amigo_id,))
        amigo = cursor.fetchone()
        return amigo[0], amigo[1] if amigo else ("", "")
    return "", ""


def obtener_mensajes(miembro_actual, amigo_id):
    cursor.execute("""
        SELECT fk_miembro1, contenido_mensaje, fechaHora_mensaje 
        FROM MENSAJES 
        WHERE (fk_miembro1 = %s AND fk_miembro2 = %s)
            OR (fk_miembro1 = %s AND fk_miembro2 = %s)
        ORDER BY fechaHora_mensaje ASC
    """, (miembro_actual, amigo_id, amigo_id, miembro_actual))
    return cursor.fetchall()

# Ruta para mostrar la lista de amigos y los mensajes

def amigos_chat(amigo_id=None):
    conexion_db()

    # Obtener la lista de miembros para mostrar en el panel de amigos
    miembros = obtener_lista_miembros()
    
    # Si no se ha seleccionado un amigo, establece un amigo por defecto o maneja el caso.
    amigo_id = amigo_id if amigo_id else obtener_amigo_por_defecto(miembros)

    # Obtener el nombre del amigo seleccionado
    amigo_nombre, amigo_apellido = obtener_nombre_amigo(amigo_id)

    # Obtener el ID del miembro actual (debería obtenerse de la sesión)
    miembro_actual = 1  # Cambiar esto por el código para obtener el ID de la persona que inició sesión 

    # Obtener los mensajes entre el miembro actual y el amigo seleccionado
    mensajes = obtener_mensajes(miembro_actual, amigo_id) if amigo_id else []

    # Renderiza la plantilla HTML con la información de los amigos y mensajes
    return render_template('amigos_chat.html', miembros=miembros, mensajes=mensajes, 
                            amigo_nombre=amigo_nombre, amigo_apellido=amigo_apellido, 
                            amigo_actual=amigo_id)

# Ruta para enviar un mensaje
def enviar_mensaje(amigo_id):
    conexion_db()

    if request.method == 'POST':
        # Obtener el ID del miembro actual desde la sesión
        fk_miembro1 = 1  # Cambiar por la ID del miembro actual desde la sesión
        
        # Captura del mensaje desde el formulario
        contenido_mensaje = request.form['Enter_mensaje']
        
        # Validación de datos antes de la inserción
        if not amigo_id or not contenido_mensaje:
            return jsonify({"success": False, "message": "Datos incompletos"}), 400

        try:
            # Inserción del nuevo mensaje en la base de datos
            insertar_mensaje(fk_miembro1, amigo_id, contenido_mensaje)
            mydb.commit()  # Confirmación de la transacción
            return jsonify({"success": True, "message": "Mensaje enviado correctamente."})
        except mysql.connector.Error as err:
            mydb.rollback()  # Reversión de la transacción en caso de error
            return jsonify({"success": False, "message": f"Error al enviar el mensaje: {err}"}), 500
        except Exception as e:
            mydb.rollback()  # Reversión de la transacción en caso de error
            return jsonify({"success": False, "message": f"Error inesperado: {e}"}), 500



def insertar_mensaje(fk_miembro1, amigo_id, contenido_mensaje):
    cursor.execute(
        'INSERT INTO MENSAJES (fk_miembro1, fk_miembro2, contenido_mensaje) VALUES (%s, %s, %s)',
        (fk_miembro1, amigo_id, contenido_mensaje)
    )
