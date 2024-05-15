# Importacion de librerias.
import mysql.connector
from flask import Flask, url_for, redirect, request, render_template, session, jsonify

# Inicializacion de la pagina
app = Flask(__name__)
# Esta linea es delicada ya que sin ella las sessiones no funcionaran.
app.secret_key = 'secret_key'

# Conexion con la base de datos de railway.
mydb = mysql.connector.connect(
    host='roundhouse.proxy.rlwy.net',
    user='root',
    password='alzSPNqOksaVjmzIgLKqqcuiHwCaCFei',
    port=36119,
    database='railway'
)

# Ejecutador de comandos/consultas de la base de datos.
cursor = mydb.cursor()
# ------------------------------------------------------------------------------------------------------------

# Ruta de la pagina principal.


@app.route('/')
def index():
    return render_template('index.html')
# ------------------------------------------------------------------------------------------------------------

# Ruta de la pagina de registro.


@app.route("/register")
def register():
    if session:  # Esta condicional verfica si hay alguna sesion en curso, si es valida no se podrá ingresar a esta ruta, será redirigido al inicio, ya que no se puede registrar un usuario ya registrado.
        return redirect(url_for('inicio'))
    else:  # Si no hay una sesion en curso se autorizará el ingreso a  la pagina de registro.
        return render_template('register.html')

# -----------------------------------------------------------------------------------------------------------

# Ruta para la pagina de login.


@app.route('/login')
def login():
    if session:  # Esta condicional verfica si hay alguna sesion en curso, si es valida no se podrá ingresar a esta ruta, será redirigido al inicio, ya que no puede iniciar sesion un usuario que ya inicio sesion.
        return redirect(url_for('inicio'))
    else:  # Si no hay una sesion en curso se autorizará el ingreso a  la pagina de logueo.
        return render_template('login.html')
# -----------------------------------------------------------------------------------------------------------

# Ruta de la pagina de incio.


@app.route('/inicio')
def inicio():
    # Se crea una variable en donde se almacenara el docuemento del usuario que inicio sesion.
    documentoLogueado = 0
    if session:  # Si hay una sesion en curso se podrá accerder al inicio.
        # En esta variable se almacena el documento del usuario logueado.Luego se redirige al inicio.
        documentoLogueado = session['documentoLogueado']
        return render_template('inicio.html')
    else:  # Si no hay una sesion en curso se redirigira a la pagina de logueo.
        return redirect(url_for('login'))

# -----------------------------------------------------------------------------------------------------------

# Ruta para el procesamiento del registro.


@app.route('/registering', methods=['GET', 'POST'])
def regitering():
    if request.method == 'POST':
        # Aqui se obtienen todos los valores de los inputs del formulario de "register.html". int y str son para obtener los valores respectivamente en numero entero y tipo texto.
        document = int(request.form['inputDocumentNumber'])
        password = str(request.form['inputPassword'])
        username = str(request.form['inputUsername'])
        email = str(request.form['inputEmail'])
        biography = str(request.form['textareaBiography'])
        # Esta es la ruta de la imagen de perfil por defecto.
        imageProfile = "{{url_for('static', filename='img/ICONS/User_sinFoto.png')}}"

        # Aqui se verifica si se ingreso algun numero de documento y si es el caso se busca ese numero en la base de datos en la tabla MATRICULE para verficar si esta matriculado en el colegio.
        if document:
            cursor.execute(
                # Se hace una consulta en la base de datos en la tabla MATRICULE para buscar el numero de documento que ingreso el usuario en el registro.
                "SELECT * FROM MATRICULE WHERE documentNumber_matricule = %s", (document,))
            # Aqui se obtiene el primer valor arrojado por la consulta en la base de datos.
            matricula_encontrada = cursor.fetchone()

            if matricula_encontrada:
                print("MATRICULA ENCONTRADA")
                # Con el documento ya verificado, tambn se verifica el nombre de usuario y el correo electronico para que no haya datos duplicados en la tabla de PROFILE y ACCOUNT.
                cursor.execute(
                    "SELECT * FROM PROFILE WHERE nickname_profile = %s", (username,))
                username_encontrado = cursor.fetchone()
                cursor.execute(
                    "SELECT * FROM ACCOUNT WHERE email_account = %s", (email,))
                email_encontrado = cursor.fetchone()

                # Si se encuentra un correo electronico y/o un nombre de usuario en la base de datos no se permitira registrarse, debe ingresarse un dato diferente no existente.
                if username_encontrado:
                    print("EL NOMBRE DE USUARIO INGRESADO YA ESTA EN USO")
                    return "EL NOMBRE DE USUARIO INGRESADO YA ESTA EN USO"
                if email_encontrado:
                    print("EL CORREO ELECTRÓNICO INGRESADO YA ESTA EN USO")
                    return "EL CORREO ELECTRÓNICO INGRESADO YA ESTA EN USO"
                else:  # Si nada esta duplicado se procede con la insersion de datos a la base de datos.
                    cursor.execute(
                        # Se inserta en la tabla ACCOUNT el correo electronico y contraseña.
                        "INSERT INTO ACCOUNT (email_account, pass_account, document_account) VALUES (%s, %s, %s)", (email, password, document))
                    if biography:
                        # Dependiendo de que si o no se ingrese datos de biografia, si se deben ingresaran los datos a la tabla PROFILE, el nombre de usuario y ruta por defecto de la  imagen de perfil.
                        cursor.execute(
                            "INSERT INTO PROFILE (nickname_profile, biography_profile, image_profile) VALUES (%s, %s, %s)", (username, biography, imageProfile,))
                    else:
                        cursor.execute(
                            "INSERT INTO PROFILE (nickname_profile, biography_profile, image_profile) VALUES (%s, %s, %s)", (username, '', imageProfile))
                    # Confirmar los cambios en la base de datos y redirigir a la ruta inicio.
                    mydb.commit()
                    return redirect(url_for('login'))

            else:
                print("MATRICULA NO ENCONTRADA")
                return "MATRICULA NO ENCONTRADA"
        else:
            print("DATOS NO INGRESADOS")
            return "DATOS NO INGRESADOS"
# -----------------------------------------------------------------------------------------------------------

# Ruta para el procesamiento del login


@app.route('/logining', methods=['POST'])
def logining():
    if request.method == 'POST':
        # Se obtienen los datos de los inputs del formulario de login.html.
        document = int(request.form['inputDocumentNumber'])
        password = request.form['inputPass']

        if document:
            # Se verifica si el documento se encuentra en la tabla ACCOUNT.
            cursor.execute(
                "SELECT * FROM ACCOUNT WHERE document_account = %s ", (
                    document,)
            )
            matricula_encontrada = cursor.fetchone()
            if matricula_encontrada:
                print(
                    "MATRICULA ENCONTRADA")
                # Si se encuentra el documento en la tabla ACCOUNT se procede a verificar la contraseña de ingreso.
                cursor.execute(
                    "SELECT * FROM ACCOUNT WHERE pass_account = %s", (password,)
                )
                contraseña_verificada = cursor.fetchone()
                if contraseña_verificada:
                    # Si la contraseña es verificada se redireccionará a la ruta inicio.
                    session['documentoLogueado'] = document
                    return redirect(url_for('inicio'))
                else:
                    print("CONTRASEÑA INCORRECTA")
                    return "CONTRASEÑA INCORRECTA"
            else:
                print("MATRICULA NO ENCONTRADA")
                return "MATRICULA NO ENCONTRADA"
        else:
            print("DATOS NO INGRESADOS")
            return "DATOS NO INGRESADOS"
# -----------------------------------------------------------------------------------------------------------

# Ruta de la pagina de perfil.


@app.route('/perfil')
def perfil():
    documentoLogueado = 0

    if session:  # Aqui se verifica si hay alguna session abierta y si no la hay no se podra acceder al perfil.
        documentoLogueado = session['documentoLogueado']
        print(documentoLogueado)
        cursor.execute("SELECT PROFILE.image_profile, PROFILE.nickname_profile, PROFILE.biography_profile FROM ACCOUNT INNER JOIN PROFILE ON ACCOUNT.profile_account=PROFILE.id_profile WHERE ACCOUNT.document_account= %s", (documentoLogueado,))
        datosProfile = cursor.fetchone()
        if datosProfile:
            # Separar por variable los datos arrojados por la consulta.
            imagen = str(datosProfile[0])
            if imagen == "None":
                imagen = str(
                    url_for('static', filename='img/ICONS/UserCirculo_ICO.png'))
            username = str(datosProfile[1])
            biografia = str(datosProfile[2])
        cursor.execute(
            "SELECT name_matricule, lastname_matricule,type_matricule, grade_matricule, group_matricule FROM MATRICULE WHERE documentNumber_matricule = %s", (documentoLogueado,))
        datosMatricule = cursor.fetchone()
        if datosMatricule:
            # Separar por variable los datos arrojados por la consulta.
            nombre = str(datosMatricule[0])
            apellido = str(datosMatricule[1])
            type = str(datosMatricule[2])
            if type == "Estudiante":
                grado = str(datosMatricule[3])
                grupo = str(datosMatricule[4])
            else:
                grado = str("Sin")
                grupo = str("grupo asignado")
        # Aqui se renderiza perfil.html y se carga los datos separados anteriormente encontrado en la consulta sql.
        return render_template('perfil.html', imagen=imagen, username=username, biografia=biografia, grado=grado, grupo=grupo, typeUser=type, nombre=nombre, apellido=apellido)
    else:
        # Aqui se redirecciona a login, ya que no hay una session abierta.
        return redirect(url_for('login'))
# -----------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True, port=4000)
