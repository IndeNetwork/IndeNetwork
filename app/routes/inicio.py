import flask_login
from flask import Flask, url_for, redirect, request, render_template, session, jsonify, flash
import mysql.connector, hashlib

def conexion_db():
    global mydb, cursor
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        database='indenetwork'
    )
    cursor = mydb.cursor()

def inicio():
    # Si hay una sesion en curso se podrá accerder al inicio.
    if 'miembroLogueado' in session:
        #Se llama la conexion con la db.
        conexion_db()
        # En la siguiente variable se guarda el valor de "miembroLogueado" de la session.
        miembroLogueado = session['miembroLogueado']
        # Se ejecuta una busqueda basada en el "miembroLogueado" para obtener su nombre y apellido. Se tiene en cuenta si el miembro que quiere ingresar es profesor o estudiante.
        if 'isTeacher' in session:
            cursor.execute(
                "SELECT nombre_profesor, apellido_profesor FROM profesores WHERE id_profesor = %s", (miembroLogueado,))
        else:
            cursor.execute(
                "SELECT nombre_estudiante, apellido_estudiante FROM estudiantes WHERE id_estudiante = %s", (miembroLogueado,))
        # Como tupla se guarda el nombre y apellido del miembro en "datos_miembro".
        datos_miembro = cursor.fetchone()
        # Solo quedaría cargar o renderizar el html con la información obtenida en la busqueda sql.
        if datos_miembro:
            return render_template('inicio.html', nombre=datos_miembro[0], apellido=datos_miembro[1])
        else: # Si no hay resultados se redirigira a la pagina de logueo.
            return redirect(url_for('login_interface'))
    else:  # Si no hay una sesion en curso se redirigira a la pagina de logueo.
        return redirect(url_for('login_interface'))
    
''' ******SIN TERMINAR*******
def inicio_search():
    if 'miembroLogueado' in session:
        conexion_db()
        if request.method == 'POST':
            valor_aBuscar = request.form['valor_aBuscar']
            if valor_aBuscar:
                cursor.execute(
                    "SELECT nombre_profesor, apellido_profesor FROM profesores WHERE (nombre_profesor = %s AND apellido_profesor = %s)  UNION SELECT nombre_estudiante, apellido_estudiante FROM estudiantes WHERE (nombre_estudiante = %s AND apellido_estudiante = %s)", (valor_aBuscar, valor_aBuscar, valor_aBuscar, valor_aBuscar))
                miembros_encontrados = cursor.fetchall()
                    
    else:
        return redirect(url_for('login'))
'''
