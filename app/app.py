import flask_login
from flask import Flask, url_for, redirect, request, render_template, session, jsonify, flash
from routes import miembros, login, inicio, logining, perfil
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
def login_route():
    return login.login()
# -----------------------------------------------------------------------------------------------------------

# Ruta de la pagina de incio.


@app.route('/inicio')
def inicio_interface():
    return inicio.inicio()


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
def logining_function():
    logining.logining()


# -----------------------------------------------------------------------------------------------------------

# Ruta de la pagina de perfil.


@app.route('/perfil')
def perfil_route():
    return perfil.perfil()

# -----------------------------------------------------------------------------------------------------------

# Ruta de la pagina de manejo de los miembros


@app.route('/miembros')
def miembros_interface():
    return miembros.miembros()

# Ruta para insertar datos a miembros


@app.route('/miembros/insertar', methods=['GET', 'POST'])
def insertarmiembro():
    return miembros.insertarmiembro()

# Ruta para eliminar miembros


@app.route('/miembros/eliminar/<string:id_miembro>')
def eliminar_miembro(id_miembro):
    return miembros.eliminar_miembro(id_miembro)


@app.route('/miembros/refresh')
def refresh():
    return miembros.miembros_refresh()

# Ruta para editar miembro


@app.route('/miembros/editar/<string:id_miembro>', methods=['GET', 'POST'])
def editar_miembro(id_miembro):
    return miembros.editar_miembro(id_miembro)

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