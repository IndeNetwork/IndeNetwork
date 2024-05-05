#Importacion de librerias
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

# Ruta de la pagina de login
@app.route('/login')
def login():
    return render_template('login.html')

# Ruta de la pagina de incio
@app.route('/home')
def home():
    return render_template('home.html')

# Ruta para el procesamiento del login
@app.route('/logining', methods=['POST'])
def logining():
    if request.method == 'POST':
        email = request.form['inputDocumentNumber']
        password = request.form['inputPass']

        if email and password:
            cursor.execute(
                "SELECT * FROM ACCOUNTS WHERE documentNumber_account = %s AND pass_account = %s", (email, password))
            user_encontrado = cursor.fetchone()
            print(user_encontrado)
            if user_encontrado:
                return redirect(url_for('home'))
            else:
                return "USUARIO NO REGISTRADO"
        else:
            return "DATOS INVALIDOS", 400


if __name__ == '__main__':
    app.run(debug=True, port=3000)
