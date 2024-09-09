import flask_login
from flask import Flask, url_for, redirect, request, render_template, session, jsonify, flash
import mysql.connector
import hashlib


def conexion_db():
    global mydb, cursor
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        database='indenetwork'
    )
    cursor = mydb.cursor()


def grupos():
    # Si hay una sesion en curso se podrá accerder a la ruta de grupos.
    if 'miembroLogueado' in session:
        conexion_db()  # Conección con la base de datos para las consultas
        
        # OBTENCIÓN DE DATOS DE TODOS LOS GRUPOS:
        cursor.execute(
            "SELECT grupos.id_grupo, grupos.descripcion_grupo, grados.num_grado, grados.numGrupo_grado FROM grupos INNER JOIN grados ON grupos.fk_grado = grados.id_grado ORDER BY grados.num_grado ASC")
        # En la variable grupos_registrados se guardan todos los grupos registrados en la base de datos.
        grupos_totales = cursor.fetchall()
        
        if 'isTeacher' in session:
            # OBTENCIóN DE DATOS DE SOLO LOS GRUPOS DEL MIEMBRO:
            cursor.execute("SELECT grupos.id_grupo, grupos.descripcion_grupo, grados.num_grado, grados.numGrupo_grado FROM grupos INNER JOIN miembros ON grupos.fk_miembro = miembros.id_miembro INNER JOIN grados ON grupos.fk_grado = grados.id_grado WHERE grupos.fk_miembro = %s ORDER BY grupos.descripcion_grupo ASC",
                        (session['miembroLogueado'],))
            isTeacher = True
        else:
            # OBTENCIóN DE DATOS DE SOLO LOS GRUPOS DEL MIEMBRO:
            cursor.execute("SELECT grupos.id_grupo, grupos.descripcion_grupo, grados.num_grado, grados.numGrupo_grado FROM grupos INNER JOIN integrantes ON grupos.id_grupo = integrantes.fk_grupo INNER JOIN grados ON grupos.fk_grado = grados.id_grado WHERE integrantes.fk_miembro = %s ORDER BY grupos.descripcion_grupo ASC",
                    (session['miembroLogueado'],))
            isTeacher = False
            
        grupos_miembro = cursor.fetchall()

        # Se renderiza el html con la variable grupos_registrados.
        return render_template('grupos.html', grupos=grupos_totales, myGroups=grupos_miembro, profesor=isTeacher)

    # Si no hay una sesion en curso se redirigira a la pagina de logueo.
    else:
        return redirect(url_for('login_route'))


def search_group():
    if request.method == 'POST':
        conexion_db()
        nombreGrupo = request.form['grupo_aBuscar']
        if nombreGrupo.strip():
            try:
                # Obtener datos de todos los grupos según la búsqueda
                cursor.execute(
                    "SELECT grupos.id_grupo, grupos.descripcion_grupo, grados.num_grado, grados.numGrupo_grado FROM grupos INNER JOIN grados ON grupos.fk_grado = grados.id_grado WHERE grupos.descripcion_grupo LIKE %s OR grados.num_grado LIKE %s OR grados.numGrupo_grado LIKE %s ORDER BY grados.num_grado ASC", ('%' + nombreGrupo + '%', '%' + nombreGrupo + '%', '%' + nombreGrupo + '%'))
                grupos_encontrados = cursor.fetchall()

                # Obtener datos de solo los grupos del miembro
                cursor.execute("SELECT grupos.id_grupo, grupos.descripcion_grupo, grados.num_grado, grados.numGrupo_grado FROM grupos INNER JOIN integrantes ON grupos.id_grupo = integrantes.fk_grupo INNER JOIN grados ON grupos.fk_grado = grados.id_grado WHERE integrantes.fk_miembro = %s AND (grupos.descripcion_grupo LIKE %s OR grados.num_grado LIKE %s OR grados.numGrupo_grado LIKE %s) ORDER BY grupos.descripcion_grupo ASC",
                            (session['miembroLogueado'], '%' + nombreGrupo + '%', '%' + nombreGrupo + '%', '%' + nombreGrupo + '%'))
                grupos_miembro = cursor.fetchall()

                # Devolver los resultados como JSON
                return jsonify({
                    'grupos': grupos_encontrados,
                    'myGroups': grupos_miembro
                })

            except mysql.connector.Error as error:
                print("Error al ejecutar la consulta: ", error)
                return jsonify({'error': 'Error al ejecutar la consulta'})
        else:
            print("ERROR DE BUSQUEDA: No se ingresó un valor a buscar")
            return jsonify({'error': 'No se ingresó un valor a buscar'})
    else:
        return jsonify({'error': 'Método no permitido'})


def insert_group(id_grupo: int):
    if id_grupo:  # Verifica que el id del grupo no este vacio.
        print("\nVARIABLE id_grupo: ", id_grupo)
        conexion_db()  # Crea la conección con la base de datos.
        # Se obtiene el id del miembro que se encuentra en la sesion.
        miembroLogueado = session.get('miembroLogueado')
        # Se imprime el valor de miembroLogueado.
        print(f"\nID MIEMBRO LOGUEADO: {miembroLogueado}")
        # Se verifica que el miembroLogueado no este vacio.
        if miembroLogueado:
            # Se verifica que el miembroLogueado sea un estudiante o profesor, si es profesor se salta la condicional.
            if 'isTeacher' in session:
                True
            # Si el miembroLogueado es un estudiante se verifica que el grado del grupo sea el mismo que el del miembroLogueado.
            else:
                cursor.execute("SELECT estudiantes.id_estudiante AS ID_ESTUDIANTE, estudiantes.fk_grado AS ID_GRADO_ESTUDIANTE FROM estudiantes INNER JOIN miembros ON estudiantes.id_estudiante = miembros.fk_estudiante WHERE miembros.id_miembro = %s", (miembroLogueado,))
                datos_estudiante = cursor.fetchone()
                print(f"\nID DEL ESTUDIANTE:  {
                    datos_estudiante[0]}\nGRADO DEL ESTUDIANTE: {datos_estudiante[1]}")
                # Lo que realiza la consulta es realizar una comparación entre el grado del grupo y el del miembroLogueado con INNER JOIN entre las tablas estudiantes, grupos, integrantes y miembros.
                cursor.execute("""
                    SELECT estudiantes.fk_grado AS GRADO_ESTUDIANTE, grupos.fk_grado AS GRADO_GRUPO 
                    FROM estudiantes 
                    INNER JOIN miembros ON estudiantes.id_estudiante = miembros.fk_estudiante
                    INNER JOIN grupos ON grupos.fk_grado = estudiantes.fk_grado
                    WHERE miembros.id_miembro = %s AND grupos.id_grupo = %s
                    """, (miembroLogueado, id_grupo))
                # En la variable resultado_consulta se guardan los resultados de la consulta.
                resultado_consulta = cursor.fetchall()
                # Se imprime el valor de resultado_consulta.
                print(f"\nCONSULTA DE COMPARACION de GRADOS: {
                    resultado_consulta}")
                # Si la variable resultado_consulta resulta con un valor significa que el miembroLogueado que resulta ser un estudiante esta autorizado a ingresar al grupo ya que cuenta con el mismo grado del grupo.
                if resultado_consulta:
                    print("RESULTADO DE COMPARACION: EL miembro logueado que resulta ser un estudiante esta autorizado a ingresar al grupo ya que cuenta con el mismo grado del grupo")
                    True
                # Si la variable resultado_consulta es vacia se redirigira a la pagina de grupos ya que el estudiante no cuenta con el mismo grado que el grupo.
                else:
                    print(
                        "RESULTADO DE COMPARACION: El miembros logueado que resulta ser un estudiante no cuenta con el mismo grado del grupo")
                    cursor.execute(
                        "SELECT fk_grado FROM grupos WHERE id_grupo = %s", (id_grupo,))
                    resultado_consulta2 = cursor.fetchall()
                    print(f"\nID DEL GRUPO: {resultado_consulta2[0][0]}\n")
                    # Se redirigira a la pagina de grupos.
                    return redirect(url_for('groups_interface'))

            # Se verifica que el miembro logueado no este en el grupo.
            cursor.execute("""
                    SELECT miembros.id_miembro 
                    FROM miembros
                    INNER JOIN integrantes ON miembros.id_miembro = integrantes.fk_miembro
                    WHERE integrantes.fk_miembro = %s AND integrantes.fk_grupo = %s
                """, (miembroLogueado, id_grupo))

            # En la variable verificacion_miembros_inGrupo se guardan los resultados de la consulta.
            verificacion_miembro_inGrupo = cursor.fetchall()
            print(f"\n¿YA SE ENCUENTRA EL MIEMBRO EN GRUPO?: {
                verificacion_miembro_inGrupo}")

            # Si la variable verificacion_miembros_inGrupo no es vacia significa que el miembroLogueado ya se encuentra en el grupo.
            if verificacion_miembro_inGrupo:
                print(
                    "RESULTADO DE VERIFICACION: Ya el miembro logueado se encuentra en el grupo")

                # Se redirigira a la pagina de grupos.
                return redirect(url_for('groups_interface'))

            # Si la variable verificacion_miembros_inGrupo es vacia significa que el miembroLogueado no se encuentra en el grupo.
            else:
                cursor.execute(
                    """INSERT INTO integrantes (fk_miembro, fk_grupo) VALUES (%s, %s)""", (miembroLogueado, id_grupo))

            # Confirma la transacción de datos a la base de datos.
            mydb.commit()
            # Se imprime el mensaje de que se inserto el usuario a la DB.
            print("\nSe ingreso el usuario al DB\n")
            # Se redirigira a la pagina del grupo el cual se renderiza con el nombre del grupo.
            return redirect(url_for('groups_interface'))
        # Si el miembroLogueado no se encuentra en la sesion se redirigira a la pagina de logueo.
        else:
            # El flash es un mensaje de alerta que se renderiza en el html.
            flash(
                'No se encontró el miembro logueado. Por favor, inicie sesión nuevamente.', 'danger')
            return redirect(url_for('login_route'))
    # Si el id del grupo es vacio se redirigira a la pagina de grupos.
    else:
        # El flash es un mensaje de alerta que se renderiza en el html.
        flash('No se proporcionó un valor válido para el grupo. Por favor, inténtelo de nuevo.', 'danger')
        # Se redirigira a la pagina de grupos.
        return redirect(url_for('group_interface'))


def viewPost_groups(id_grupo):
    if 'miembroLogueado' in session:
        print("\n\nFUNCION DE CONSULTA DE TAREAS")
        print(f"\nID DEL GRUPO: {id_grupo}\n")
        conexion_db()
        cursor.execute(
            "SELECT tareas.id_tarea, profesores.nombre_profesor, profesores.apellido_profesor, tareas.titulo_tarea, tareas.descripcion_tarea, tareas.archivo_tarea, tareas.fechaHora_tarea, tareas.fechaHoraVen_tarea, tareas.accesoCom_tarea FROM tareas INNER JOIN grupos ON tareas.fk_grupo = grupos.id_grupo INNER JOIN miembros ON grupos.fk_miembro = miembros.id_miembro INNER JOIN profesores ON miembros.fk_profesor = profesores.id_profesor WHERE grupos.id_grupo = %s ORDER BY tareas.fechaHora_tarea DESC", (
                id_grupo,)
        )
        tareas = cursor.fetchall()
        print(f"\nTAREAS: {tareas}\n")
        return jsonify(tareas)
    else:
        return redirect(url_for('login_route'))

def addTask(id_grupo):
    return redirect(url_for('groups_interface'))