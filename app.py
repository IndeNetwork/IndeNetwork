import mysql.connector
from flask import Flask, url_for, redirect, request, render_template, session


app = Flask(__name__)


mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    port=3306,
    database='base_de_datos'
)


cursor = mydb.cursor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputContraseña']

        if email and password:
            cursor.execute(
                "SELECT * FROM usuarios WHERE correo_User = %s AND pass_User = %s", (email, password))
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
