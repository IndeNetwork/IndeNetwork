import flask_login
from flask import Flask, url_for, redirect, request, render_template, session, jsonify, flash
from routes import miembros, login, inicio, logining, perfil, grupos, amigos_chat
import mysql.connector
import hashlib
# Importacion de librerias.

# Inicializacion de la pagina
app = Flask(__name__)
# Esta linea es delicada ya que sin ella las sessiones no funcionaran.
app.secret_key = 'secret_key'

# Toco convertir la conexion con la db en una variable global y en una funcion para llamarla en donde se necesite.


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



# -----------------------------------------------------------------------------------------------------------

# Ruta para el procesamiento del login


@app.route('/logining', methods=['POST'])
def logining_function():
    return logining.logining()


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
# ********GRUPOS AUN SIN TERMINAR********

#Ruta para la pagina de grupos
@app.route('/grupos')
def groups_interface():
    return grupos.grupos()

#Ruta para la funcion de buscar grupos
@app.route('/grupos/search', methods=['GET', 'POST'])
def search_group():
    return grupos.search_group()

# Ruta para la funcion de insertar grupos
@app.route('/grupos/insertar/<string:id_grupo>')
def insert_group(id_grupo):
    return grupos.insert_group(id_grupo)

@app.route('/grupos/view/<string:id_grupo>')
def view_group(id_grupo):
    return grupos.viewPost_groups(id_grupo)

# ------------------------------------------------------------------------------------------------------------
# Ruta para obtener la lista de amigos y sus id
@app.route('/amigoschat')
def amigosChat_interface():
    return amigos_chat.amigos_chat()

# Ruta para enviar mensajes
@app.route('/amigoschat/<int:amigo_id>', methods=['GET', 'POST'])
def enviarMensaje_function(amigo_id):
    return amigos_chat.enviar_mensaje(amigo_id)

@app.route('/get_new_messages/<int:amigo_id>')
def get_new_messages(amigo_id):
    return amigos_chat.obtener_nuevos_mensajes(amigo_id)

# -----------------------------------------------------------------------------------------------------------

# Funcion para cerrar sesión


@app.route('/logout')
def logout():
    # Aqui se elimina mediante ".pop" y si no hay una session devolverá "None".
    session.pop('miembroLogueado', None)
    # Finalmente se redirecciona a la pantalla de login.
    return redirect(url_for('login_route'))
# -----------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True, port=4000)
