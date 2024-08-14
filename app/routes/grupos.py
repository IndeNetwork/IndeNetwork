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

# ********GRUPOS AUN SIN TERMINAR********


def grupos():
    if 'miembroLogueado' in session:
        conexion_db()
        cursor.execute(
            "SELECT fk_profesor, fk_grado, descripcion_grupo, fk_asignatura FROM grupos")
        grupos_registrados = cursor.fetchall()
        grupos_diccionario = {}
        for grupo in grupos_registrados:
            grupo_dict = {
                'fk_profesor': grupo[0],
                'fk_grado': grupo[1],
                'descripcion_grupo': grupo[2],
                'fk_asignatura': grupo[3]
            }
            grupos_diccionario[grupo_dict['descripcion_grupo']] = grupo_dict
            print(grupos_diccionario)
        return render_template('grupos.html', grupos=grupos_diccionario)
    else:
        return redirect(url_for('login_route'))


def search_group():
    if request.method == 'POST':
        conexion_db()
        nombreGrupo = request.form['grupo_aBuscar']
        if nombreGrupo.strip():
            cursor.execute(
                'SELECT fk_profesor, fk_grado, descripcion_grupo, fk_asignatura FROM grupos WHERE descripcion_grupo LIKE %s', (nombreGrupo,))
            grupos_encontrados = cursor.fetchall()
            if grupos_encontrados:
                grupos_spacesWhite = [tuple(
                    '' if valor is None else valor for valor in grupo) for grupo in grupos_encontrados]
                return render_template('grupos.html', grupos=tuple(list(reversed(grupos_spacesWhite))))
            else:
                return redirect(url_for('grupos_interface'))
        else:
            return redirect(url_for('grupos_interface'))


def insert_group(id_grupo):
    conexion_db()
    if id_grupo:
        print(f"\n{id_grupo}\n")
        miembroLogueado = int(session['miembroLogueado'][0])
        cursor.execute(
            "SELECT id_miembro FROM miembros WHERE id_miembro = %s", (miembroLogueado))
        id_miembro = cursor.fetchone()
        if id_miembro:
            print(id_miembro)

        cursor.execute("INSERT INTO integrantes (id_miembro, id_grupo) VALUES (%s, %s)",
                       (id_miembro, id_grupo))
        mydb.commit()
        return redirect(url_for('grupos'))
        cursor.execute("SELECT id_integrante FROM integrantes WHERE id_miembro = %s AND id_grupo = %s",
                       (session['miembroLogueado'], id_grupo))
        integrante_existe = cursor.fetchone()
        if integrante_existe:
            session['integranteGrupo'] = integrante_existe
            print(f"\n{session['miembroLogueado']
                       }\n ---------------- \n{session['integranteGrupo']}\n")
            return redirect(url_for('inicio'))
    else:
        return render_template('inicio.html')
