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

def perfil():
    # Aqui se verifica si la session de miembro esta abierta y si no la hay no se podra acceder al perfil.
    if "miembroLogueado" in session:
        # A esta variable se comparte el valor de la matricula de la session del miembro logueado.
        miembroLogueado = session['miembroLogueado']
        # Se consulta el nombre, apellido, tipo, grado y grupo del miembro de acuerdo a su documento.
        if 'isTeacher' in session:
            query = "SELECT profesores.nombre_profesor, profesores.apellido_profesor, miembros.tipo_miembro FROM miembros INNER JOIN profesores ON miembros.fk_profesor = profesores.id_profesor WHERE id_miembro = %s"
        else:
            query = "SELECT estudiantes.nombre_estudiante, estudiantes.apellido_estudiante, miembros.tipo_miembros FROM miembros INNER JOIN estudiantes ON miembros.fk_estudiante = estudiantes.id_estudiante WHERE id_miembros = %s"
        
        cursor.execute(query, (miembroLogueado,))
        datosMiembro = cursor.fetchone()
        if datosMiembro:
            # Separar por variable como texto los datos arrojados por la consulta.
            nombre = str(datosMiembro[0])
            apellido = str(datosMiembro[1])
            tipo = str(datosMiembro[2])
            """
            grado = str(datosMiembro[3])
            grupo = str(datosMiembro[4])
            """

        # Aqui se renderiza perfil.html y se carga los datos anteriormente separados encontrados en la consulta.
        return render_template('perfil.html', nombre=nombre, apellido=apellido, tipo=tipo)
    else:
        # Aqui se redirecciona a login, ya que no hay una session abierta.
        return redirect(url_for('login_interface'))