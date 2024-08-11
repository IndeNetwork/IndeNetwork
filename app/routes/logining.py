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

def logining():
    if request.method == 'POST': # Si hay metodo es POST se procede a realizar el login.
        try:
            conexion_db() # Se realiza la conexion con la db.
            # Documento ID.
            document = int(request.form['inputDocumentNumber'])
            password = request.form['inputPass']  # Contraseña.
            isTeacher = request.form.getlist('IsTeacher')  # Check de profesor.

            # Verifica que los datos no esten vacios.
            if not document or not password:
                return "DATOS NO INGRESADOS"

        # Verifica que los datos sean numericos.
        except (ValueError, KeyError):
            return "ERROR EN EL PROCESO DE LOGIN: DATOS INCORRECTOS"

        #Se intenta realizar el login.
        try:
            # Aqui se verifica si el miembro es un profesor o estudiante.
            if isTeacher:
                query = "SELECT miembros.id_miembro, profesores.numDocumento_profesor FROM miembros INNER JOIN profesores ON miembros.fk_profesor = profesores.id_profesor WHERE profesores.numDocumento_profesor = %s"
                session['isTeacher'] = True
            else:
                query = "SELECT miembros.id_miembro, estudiantes.numDocumento_estudiante FROM miembros INNER JOIN estudiantes ON miembros.fk_estudiante = estudiantes.id_estudiante WHERE estudiantes.numDocumento_estudiante = %s"

            # Se realiza la consulta con el query dependiendo si es un profesor o estudiante.
            cursor.execute(query, (document,))
            result = cursor.fetchone()
            # Se verifica que el miembro exista.
            if not result:
                return "MIEMBRO NO ENCONTRADO"

            # Se extraen los datos de la base de datos y se guardan en cada variable correspondiente.
            ID_miembro_encontrado, db_password = result

            # Se verifica que la contrasena sea correcta.
            if password == str(db_password):  # Comparar contraseñas de manera segura
                print("Las contraseñas son correctas, son iguales")
                # Se redirige a la pagina de inicio y se guarda el id del miembro en la variable de sesion miembroLogueado.
                session['miembroLogueado'] = int(ID_miembro_encontrado)
                return redirect(url_for('inicio'))
            else:
                return "CONTRASEÑA INCORRECTA"
        #Si ocurre un error, se mostrara el mensaje y lo especifica.
        except mysql.connector.Error as err:
            return f"ERROR EN EL PROCESO DE LOGIN: ERROR EN LA BASE DE DATOS: {str(err)}"
        #Se ciera la conexion con la db.
        finally:
            cursor.close()
            mydb.close()
            
    else:   # Si no hay metodo es POST se redirige a la pagina de logueo.
        return redirect(url_for('login'))