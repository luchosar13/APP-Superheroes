from flask import Flask, request, render_template, flash, redirect, url_for
from flasgger import Swagger
from pymongo import ASCENDING
from bson import json_util
import mongo_server
import os
import re

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
swagger = Swagger(app)


def obtener_imagenes(nombre_personaje):
    carpeta = os.path.join(app.static_folder, 'images')
    nombre_base = nombre_personaje.lower().replace(' ', '_')
    return [f'images/{img}' for img in os.listdir(carpeta) if img.startswith(nombre_base)]


@app.route("/")
def cards():
    consulta = request.args.get("q", "").strip()
    try:
        if consulta:
            filtro = {"nombre": {"$regex": consulta, "$options": "i"}}
            datoss = list(mongo_server.coleccion.find(filtro))
        else:
            datoss = list(mongo_server.coleccion.find())
    except Exception as e:
        return f"Error con la base de datos: {e}", 500

    for item in datoss:
        item['imagenes'] = obtener_imagenes(item['nombre'])

    return render_template("home.html", datos=datoss)


@app.route("/personaje/<nombre>")
def detalle_personaje(nombre):
    personaje = mongo_server.coleccion.find_one({"nombre": nombre})
    personaje['imagenes'] = obtener_imagenes(personaje['nombre'])
    if personaje:
        return render_template("detalle.html", personaje=personaje)
    else:
        return "Personaje no encontrado", 404
    

@app.route("/<casa>")
def detalle_personajes_por_casa(casa):
    # Expresión regular insensible a mayusculas
    regex = re.compile(f"^{casa}$", re.IGNORECASE)
    personajes = list(mongo_server.coleccion.find({"casa": regex,"tipo":"Heroe"}))
    
    if not personajes:
        return "No se encontraron personajes de esta casa.", 404

    for personaje in personajes:
        personaje['imagenes'] = obtener_imagenes(personaje['nombre'])

    casa_cap = casa.capitalize() if casa.lower() != "dc" else "DC"

    return render_template("por_casa.html", personajes=personajes, casa=casa_cap)

@app.route("/agregar", methods=["GET", "POST"])
def agregar_personaje():
    if request.method == "POST":
        try:
            nuevo = {
                "nombre": request.form["nombre"],
                "nombre_real": request.form["nombre_real"],
                "anio_aparicion": int(request.form["anio_aparicion"]),
                "casa": request.form["casa"],
                "tipo": request.form["tipo"],
                "equipamiento": request.form["equipamiento"],
                "biografia": request.form["biografia"]
            }
            mongo_server.coleccion.insert_one(nuevo)
            flash(f"Personaje '{nuevo['nombre']}' agregado correctamente.", "success")
            return redirect(url_for("cards"))
        except Exception as e:
            flash(f"Error al agregar personaje: {e}", "danger")
    return render_template("agregar.html")


@app.route("/modificar", methods=["GET", "POST"])
def modificar_personaje():
    if request.method == "POST":
        nombre = request.form["nombre"]
        personaje = mongo_server.coleccion.find_one({"nombre": nombre})
        if personaje:
            campos = {
                "nombre_real": request.form["nombre_real"],
                "anio_aparicion": int(request.form["anio_aparicion"]),
                "casa": request.form["casa"],
                "tipo": request.form["tipo"],
                "equipamiento": request.form["equipamiento"],
                "biografia": request.form["biografia"]
            }
            mongo_server.coleccion.update_one({"nombre": nombre}, {"$set": campos})
            flash(f"Personaje '{nombre}' modificado correctamente.", "success")
            return redirect(url_for("cards"))
        else:
            flash(f"Personaje '{nombre}' no encontrado.", "warning")
    return render_template("modificar.html")


@app.route("/eliminar", methods=["GET", "POST"])
def eliminar_personaje():
    if request.method == "POST":
        nombre = request.form["nombre"]
        resultado = mongo_server.coleccion.delete_one({"nombre": nombre})
        if resultado.deleted_count:
            flash(f"Personaje '{nombre}' eliminado correctamente.", "success")
        else:
            flash(f"No se encontró el personaje '{nombre}'.", "warning")
        return redirect(url_for("cards"))
    return render_template("eliminar.html")
