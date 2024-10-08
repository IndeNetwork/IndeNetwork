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
        print(f"\n\nID DEL MIEMBRO LOGUEADO: {miembroLogueado}\n")
        cursor.execute('SELECT * FROM publicaciones LIMIT 5')
        publicaciones = cursor.fetchall()
        cursor.execute('SELECT * FROM amigos WHERE fk_miembro1 = %s or fk_miembro2 = %s', (miembroLogueado,miembroLogueado))
        amigos = cursor.fetchall()

        # Se ejecuta una busqueda basada en el "miembroLogueado" para obtener su nombre y apellido. Se tiene en cuenta si el miembro que quiere ingresar es profesor o estudiante.
        if 'isTeacher' in session:
            cursor.execute(
                "SELECT profesores.nombre_profesor, profesores.apellido_profesor FROM profesores INNER JOIN miembros ON profesores.id_profesor = miembros.fk_profesor WHERE miembros.id_miembro = %s", (miembroLogueado,))
        else:
            cursor.execute(
                "SELECT estudiantes.nombre_estudiante, estudiantes.apellido_estudiante FROM estudiantes INNER JOIN miembros ON estudiantes.id_estudiante = miembros.fk_estudiante WHERE miembros.id_miembro = %s", (miembroLogueado,))
        # Como tupla se guarda el nombre y apellido del miembro en "datos_miembro".
        datos_miembro = cursor.fetchone()
        # Solo quedaría cargar o renderizar el html con la información obtenida en la busqueda sql.
        if datos_miembro:
            return render_template('inicio.html', nombre=datos_miembro[0], apellido=datos_miembro[1], publicaciones= publicaciones, amigos= amigos)
        else: # Si no hay resultados se redirigira a la pagina de logueo.
            return redirect(url_for('login_route'))
        

    else:  # Si no hay una sesion en curso se redirigira a la pagina de logueo.
        return redirect(url_for('login_route'))