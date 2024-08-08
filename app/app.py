import flask_login
from flask import Flask, url_for, redirect, request, render_template, session, jsonify, flash
import mysql.connector, hashlib
# Importacion de librerias.

# Inicializacion de la pagina
app = Flask(__name__)
# Esta linea es delicada ya que sin ella las sessiones no funcionaran.
app.secret_key = 'secret_key'

#Toco convertir la conexion con la db en una variable global y en una funcion para llamarla en donde se necesite.
def conexion_db():
    global mydb, cursor
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        database='indenetwork'
    )
    cursor = mydb.cursor()
# ------------------------------------------------------------------------------------------------------------

# Ruta de la pagina principal.


@app.route('/')
def index():
    return render_template('index.html')
# -----------------------------------------------------------------------------------------------------------

# Ruta para la pagina de login.


@app.route('/login')
def login():
    # Esta condicional verfica si hay alguna sesion en curso, si es valida no se podrá ingresar a esta ruta, será redirigido al inicio, ya que no puede iniciar sesion un usuario que ya inicio sesion.
    if 'miembroLogueado' in session:
        return redirect(url_for('inicio'))
    else:  # Si no hay una sesion en curso se autorizará el ingreso a  la pagina de logueo.
        return render_template('login.html')
# -----------------------------------------------------------------------------------------------------------

# Ruta de la pagina de incio.


@app.route('/inicio')
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
            return redirect(url_for('login'))
    else:  # Si no hay una sesion en curso se redirigira a la pagina de logueo.
        return redirect(url_for('login'))


''' ******SIN TERMINAR*******
@app.route('/inicio/search', methods=['POST'])
def inicio_search():
    if 'miembroLogueado' in session:
        if request.method == 'POST':
            valor_aBuscar = request.form['valor_aBuscar']
            if valor_aBuscar:
                cursor.execute(
                    "SELECT nombre_profesor, apellido_profesor FROM profesores WHERE (nombre_profesor = %s AND apellido_profesor = %s)  UNION SELECT nombre_estudiante, apellido_estudiante FROM estudiantes WHERE (nombre_estudiante = %s AND apellido_estudiante = %s)", (valor_aBuscar, valor_aBuscar, valor_aBuscar, valor_aBuscar))
                miembros_encontrados = cursor.fetchall()
                    
    else:
        return redirect(url_for('login'))
'''
# -----------------------------------------------------------------------------------------------------------

# Ruta para el procesamiento del login

@app.route('/logining', methods=['POST'])
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


# -----------------------------------------------------------------------------------------------------------

# Ruta de la pagina de perfil.


@app.route('/perfil')
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
        return redirect(url_for('login'))

# -----------------------------------------------------------------------------------------------------------

""" Ruta de la pagina de manejo de los miembros


@app.route('/miembros')
def miembros():
    # Aqui se toman los datos que estan guardados en la base de datos para mostrarlos en "miembros.html"
    cursor.execute('SELECT * FROM MIEMBROs')
    miembros_registrados = cursor.fetchall()
    # Reemplazar los valores None por un espacio en blanco en los resultados
    miembros_registrados_con_blancos = [tuple(
        '' if valor is None else valor for valor in miembro) for miembro in miembros_registrados]
    # Conteo de cuantos estudiantes hay registrados
    cursor.execute(
        'SELECT COUNT(tipo_miembro) FROM MIEMBROs WHERE tipo_miembro= "Estudiante"')
    total_estudiantes = cursor.fetchone()
    # Conteo de cuantos profesores hay registrados
    cursor.execute(
        'SELECT COUNT(tipo_miembro) FROM MIEMBROs WHERE tipo_miembro= "Profesor"')
    total_profesores = cursor.fetchone()
    return render_template('miembros.html', miembros=tuple(list(reversed(miembros_registrados_con_blancos))), total_estudiantes=total_estudiantes, total_profesores=total_profesores)

# Ruta para insertar datos a miembros


@app.route('/miembros/insertar', methods=['GET', 'POST'])
def insertarmiembro():
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

# Ruta para eliminar miembros


@app.route('/miembros/eliminar/<string:id_miembro>')
def eliminar_miembro(id_miembro):
    # consulta para eliminar el miembro de la base de datos
    cursor.execute('DELETE  FROM MIEMBRO WHERE id_miembro = %s', (id_miembro,))
    # Subir los cambios realizados a la base de datos
    mydb.commit()
    flash('Miembro Eliminado Correctamente')
    return redirect(url_for('miembros'))


@app.route('/miembros/refresh')
def miembros_refresh():
    try:
        miembros()
        mydb.commit()
        flash('Datos recargados correctamente')
        return redirect(url_for('miembros'))
    except Exception:
        flash(f'Error al cargar los datos, {Exception}')
        return redirect(url_for('miembros'))

# Ruta para editar miembro


@app.route('/miembros/editar/<string:id_miembro>', methods=['GET', 'POST'])
def editar_miembro(id_miembro):
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
"""
# -----------------------------------------------------------------------------------------------------------
"""********GRUPOS AUN SIN TERMINAR********


@app.route('/grupos')
def grupos():
    if 'miembroLogueado' in session:
        cursor.execute("SELECT * FROM GRUPO")
        grupos_registrados = cursor.fetchall()
        grupos_spacesWhite = [tuple(
            '' if valor is None else valor for valor in grupo) for grupo in grupos_registrados]
        return render_template('grupos.html', grupos=tuple(list(reversed(grupos_spacesWhite))))
    else:
        return redirect(url_for('login'))


@app.route('/grupos/search', methods=['GET', 'POST'])
def search_group():
    if request.method == 'POST':
        nombreGrupo = request.form['grupo_aBuscar']
        if nombreGrupo.strip():
            cursor.execute(
                'SELECT * FROM GRUPO WHERE nombre_grupo = %s', (nombreGrupo,))
            grupos_encontrados = cursor.fetchall()
            if grupos_encontrados:
                grupos_spacesWhite = [tuple(
                    '' if valor is None else valor for valor in grupo) for grupo in grupos_encontrados]
                return render_template('grupos.html', grupos=tuple(list(reversed(grupos_spacesWhite))))
            else:
                return redirect(url_for('grupos'))
        else:
            return redirect(url_for('grupos'))


@app.route('/grupos/insertar/<string:id_grupo>')
def insertar_grupo(id_grupo):
    if id_grupo:
        print(f"\n{id_grupo}\n")
        miembroLogueado = int(session['miembroLogueado'][0])
        cursor.execute(
            "SELECT id_miembro FROM MIEMBRO WHERE matricula_miembro = %s", (miembroLogueado))
        id_miembro = cursor.fetchone()
        if id_miembro:
            print(id_miembro)

        cursor.execute("INSERT INTO INTEGRANTE (id_miembro, id_grupo) VALUES (%s, %s)",
                    (id_miembro, id_grupo))
        mydb.commit()
        return redirect(url_for('grupos'))
        cursor.execute("SELECT id_integrante FROM INTEGRANTE WHERE id_miembro = %s AND id_grupo = %s",
                    (session['miembroLogueado'], id_grupo))
        integrante_existe = cursor.fetchone()
        if integrante_existe:
            session['integranteGrupo'] = integrante_existe
            print(f"\n{session['miembroLogueado']
                    }\n ---------------- \n{session['integranteGrupo']}\n")
            return redirect(url_for('inicio'))
    else:
        return render_template('inicio.html')
"""

# ------------------------------------------------------------------------------------------------------------
# Ruta para amigos-chat
@app.route('/amigos_chat')
def amigos_chat():
    cursor.execute("SELECT  nombre_miembro, apellido_miembro FROM MIEMBRO")
    MIEMBRO = cursor.fetchall()
    print(MIEMBRO)
    return render_template('amigos_chat.html', MIEMBRO=MIEMBRO)

# ------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------

# Funcion para cerrar sesión


@app.route('/logout')
def logout():
    # Aqui se elimina mediante ".pop" y si no hay una session devolverá "None".
    session.pop('miembroLogueado', None)
    # Finalmente se redirecciona a la pantalla de login.
    return redirect(url_for('login'))
# -----------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True, port=4000)
