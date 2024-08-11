import flask_login
from flask import Flask, url_for, redirect, request, render_template, session, jsonify, flash
import mysql.connector, hashlib

def login():
    # Esta condicional verfica si hay alguna sesion en curso, si es valida no se podrá ingresar a esta ruta, será redirigido al inicio, ya que no puede iniciar sesion un usuario que ya inicio sesion.
    if 'miembroLogueado' in session:
        return redirect(url_for('inicio_interface'))
    else:  # Si no hay una sesion en curso se autorizará el ingreso a  la pagina de logueo.
        return render_template('login.html')