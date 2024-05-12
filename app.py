# Importacion de librerias
import mysql.connector
from flask import Flask, url_for, redirect, request, render_template, session

# Inicializacion de la pagina
app = Flask(__name__)

# Conexion con la base de datos
mydb = mysql.connector.connect(
    host='roundhouse.proxy.rlwy.net',
    user='root',
    password='alzSPNqOksaVjmzIgLKqqcuiHwCaCFei',
    port=36119,
    database='railway'
)

# Ejecutador de comandos de la base de datos
cursor = mydb.cursor()

# Ruta de la pagina principal


@app.route('/')
def index():
    return render_template('index.html')

# Ruta de la pagina de registro


@app.route("/register")
def register():
    return render_template('register.html')

# Ruta para la pagina de login


@app.route('/login')
def login():
    return render_template('login.html')

# Ruta de la pagina de incio


@app.route('/home')
def home():
    return render_template('home.html')

# Ruta para el procesamiento del registro


@app.route('/registering', methods=['GET', 'POST'])
def regitering():
    if request.method == 'POST':
        document = int(request.form['inputDocumentNumber'])
        password = str(request.form['inputPassword'])
        username = str(request.form['inputUsername'])
        email = str(request.form['inputEmail'])
        biography = str(request.form['textareaBiography'])
        imageProfile = "{{url_for('static', filename='img/ICONS/User_sinFoto.png')}}"

        if document:
            cursor.execute(
                "SELECT * FROM MATRICULE WHERE documentNumber_matricule = %s", (document,))
            matricula_encontrada = cursor.fetchone()

            if matricula_encontrada:
                print("MATRICULA ENCONTRADA")
                cursor.execute(
                    "SELECT * FROM PROFILE WHERE nickname_profile = %s", (username,))
                username_encontrado = cursor.fetchone()
                cursor.execute(
                    "SELECT * FROM ACCOUNT WHERE email_account = %s", (email,))
                email_encontrado = cursor.fetchone()

                if username_encontrado:
                    print("EL NOMBRE DE USUARIO INGRESADO YA ESTA USADO")
                    return "EL NOMBRE DE USUARIO INGRESADO YA ESTA EN USO"
                if email_encontrado:
                    print("EL CORREO ELECTRÓNICO INGRESADO YA ESTA EN USO")
                    return "EL CORREO ELECTRÓNICO INGRESADO YA ESTA EN USO"
                else:
                    cursor.execute(
                        "INSERT INTO ACCOUNT (email_account, pass_account) VALUES (%s, %s)", (email, password,))
                    if biography:
                        cursor.execute(
                            "INSERT INTO PROFILE (nickname_profile, biography_profile, image_profile) VALUES (%s, %s, %s)", (username, biography, imageProfile,))
                    else:
                        cursor.execute(
                            "INSERT INTO PROFILE (nickname_profile, biography_profile, image_profile) VALUES (%s, %s, %s)", (username, '', imageProfile))
                    mydb.commit()
                    return redirect(url_for('home'))

            else:
                print("MATRICULA NO ENCONTRADA")
                return "MATRICULA NO ENCONTRADA"
        else:
            print("DATOS NO INGRESADOS")
            return "DATOS NO INGRESADOS"

# Ruta para el procesamiento del login


@app.route('/logining', methods=['POST'])
def logining():
    if request.method == 'POST':
        document = int(request.form['inputDocumentNumber'])
        password = request.form['inputPass']

        if document:
            cursor.execute(
                "SELECT * FROM MATRICULE WHERE documentNumber_matricule = %s ", (
                    document,)
            )
            matricula_encontrada = cursor.fetchone()
            print(
                "MATRICULA ENCONTRADA")
            if matricula_encontrada:
                cursor.execute(
                    "SELECT * FROM ACCOUNT WHERE pass_account = %s", (password,)
                )
                contraseña_verificada = cursor.fetchone()
                if contraseña_verificada:
                    return redirect(url_for('home'))
                else:
                    return "CONTRASEÑA INCORRECTA"
            else:
                print("MATRICULA NO ENCONTRADA")
                return "MATRICULA NO ENCONTRADA"
        else:
            print("DATOS NO INGRESADOS")
            return "DATOS NO INGRESADOS"


if __name__ == '__main__':
    app.run(debug=True, port=3000)
