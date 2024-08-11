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

def miembros():
    conexion_db()
    datos_estudiantes = []
    datos_profesores = []
    # Aqui se toman los datos que estan guardados en la base de datos para mostrarlos en "miembros.html"
    cursor.execute('SELECT * FROM miembros')
    miembros_registrados = cursor.fetchall()
    cursor.execute('SELECT fk_estudiante FROM miembros')
    ids_estudiantes = cursor.fetchall()
    cursor.execute('SELECT fk_profesor FROM miembros')
    ids_profesores = cursor.fetchall()
    # Reemplazar los valores None por un espacio en blanco en los resultados
    miembros_registrados_con_blancos = [tuple(
        '' if valor is None else valor for valor in miembro) for miembro in miembros_registrados]
    ids_estudiantes_sin_none = [tuple(
    valor for valor in id_estudiante if valor is not None) for id_estudiante in ids_estudiantes if any(id_estudiante)]
    ids_profesores_sin_none = [tuple(
    valor for valor in id_profesor if valor is not None) for id_profesor in ids_profesores if any(id_profesor)]

    for id_estudiante in ids_estudiantes_sin_none:
       cursor.execute('SELECT * FROM estudiantes WHERE id_estudiante = %s ',(id_estudiante ))
       datos_estudiantes.append(cursor.fetchall())
    for id_profesor in ids_profesores_sin_none:
       cursor.execute('SELECT * FROM profesores WHERE id_profesor = %s ',(id_profesor))
       datos_profesores.append(cursor.fetchall())
    print(datos_estudiantes)
    print(datos_profesores)
    # Conteo de cuantos estudiantes hay registrados
    cursor.execute(
        'SELECT COUNT(tipo_miembro) FROM MIEMBROs WHERE tipo_miembro= "Estudiante"')
    total_estudiantes = cursor.fetchone()
    # Conteo de cuantos profesores hay registrados
    cursor.execute(
        'SELECT COUNT(tipo_miembro) FROM MIEMBROs WHERE tipo_miembro= "Profesor"')
    total_profesores = cursor.fetchone()
    return render_template('miembros.html', miembros=tuple(list(reversed(miembros_registrados_con_blancos))), total_estudiantes=total_estudiantes, total_profesores=total_profesores, profesores= datos_profesores, estudiantes = datos_estudiantes)


def miembros_refresh():
    try:
        # Vaciar las listas explícitamente si fuera necesario
        datos_estudiantes = []
        datos_profesores = []

        miembros()  # Llama a la función que ya vacía las listas y recarga los datos
        conexion_db()
        mydb.commit()
        flash('Datos recargados correctamente')
        return redirect(url_for('miembros_interface'))
    except Exception as e:  # Captura la excepción y almacena el mensaje
        flash(f'Error al cargar los datos: {str(e)}')
        return redirect(url_for('miembros_interface'))

def editar_miembro(id_miembro):
    conexion_db()
    cursor.execute(
        'SELECT * FROM MIEMBRO WHERE id_miembro = %s', (id_miembro,))
    datos = cursor.fetchall()
    if request.method == 'POST':
        # Captura de los datos puestos en el formulario

        matricula = request.form['numero_matricula']
        documento = request.form['numero_documento']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tipo_miembro = request.form['tipo_miembro']
        grado = request.form['grado']
        grupo = request.form['grupo']
        try:
            cursor.execute('UPDATE MIEMBRO SET numeroMatricula_miembro = %s, nombre_miembro = %s, apellido_miembro = %s, numeroDocumento_miembro = %s, tipo_miembro = %s, grado_miembro = %s, grupo_miembro = %s WHERE id_miembro = %s',
                        (matricula, nombre, apellido, documento, tipo_miembro, grado, grupo, id_miembro,))
            mydb.commit()
            flash('Miembro actualizado correctamente')
            return redirect(url_for('miembros'))
        except:
            flash('Error.')
            return redirect(url_for('miembros'))

    return render_template('editar_miembro.html', id_miembro=id_miembro, datos_miembro=datos)


def eliminar_miembro(id_miembro):
    conexion_db()
    # consulta para eliminar el miembro de la base de datos
    cursor.execute('DELETE  FROM MIEMBRO WHERE id_miembro = %s', (id_miembro,))
    # Subir los cambios realizados a la base de datos
    mydb.commit()
    flash('Miembro Eliminado Correctamente')
    return redirect(url_for('miembros'))


def insertarmiembro():
    conexion_db()
    if request.method == 'POST':

        # Captura de los datos puestos en el formulario

        matricula = request.form['numero_matricula']
        documento = request.form['numero_documento']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tipo_miembro = request.form['tipo_miembro']
        grado = request.form['grado']
        grupo = request.form['grupo']

        # si el tipo de miebro es Profesor los campos grado y grupo pasan a ser nulos, ya que un porfesor no pertenece a un grado o a un grupo
        if tipo_miembro == 'Profesor':
            grado = None
            grupo = None

        try:
            # Se hace la peticion de Mysql para insertar los datos
            cursor.execute('INSERT INTO MIEMBRO (numeroMatricula_miembro,nombre_miembro,apellido_miembro,numeroDocumento_miembro,tipo_miembro,grado_miembro,grupo_miembro) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                        (matricula, nombre, apellido, documento, tipo_miembro, grado, grupo,))
            # se suben los cambios hechos a la base de datos
            mydb.commit()
            # Mensaje para mostrar en el estatus de la interfaz de miembros
            flash('Datos del miembro guardados correctamente.')
            return redirect(url_for('miembros'))
        except Exception:
            if tipo_miembro == 'Estudiante':
                # Si el tipo de miembro es estudiante, los campos grado y grupo deben ser seleccionados, sino hace la siguiente funcion
                if grado == '#' and grupo == '#' and grado == '#' or grupo == '#':
                    flash(
                        'Error, los campos grado y grupo deben ser seleccionados para estudiante, no pueden estar en "#" ')
                    return redirect(url_for('miembros'))
            if tipo_miembro == '#':
                flash('Seleccione el tipo de miembro.')
                return redirect(url_for('miembros'))

            # si ocurre un error, se mostrara este mensaje
            if Exception:
                flash(f'Fallo en guardar los datos, intente de nuevo. {Exception}')
                return redirect(url_for('miembros'))
    return render_template('insert.html')