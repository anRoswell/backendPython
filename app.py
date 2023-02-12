from http.client import HTTPException
import json
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_pyjwt import AuthManager, current_token, require_token

import psycopg2

load_dotenv()  # loads variables from .env file into environment


app = Flask(__name__)
url = os.environ.get("DATABASE_URL")  # gets variables from environment
connection = psycopg2.connect(url) 

app.config["JWT_ISSUER"] = "Flask_PyJWT" # Issuer of tokens
app.config["JWT_AUTHTYPE"] = "HS256" # HS256, HS512, RS256, or RS512
app.config["JWT_SECRET"] = "SECRETKEY" # string for HS256/HS512, bytes (RSA Private Key) for RS256/RS512
app.config["JWT_AUTHMAXAGE"] = 3600
app.config["JWT_REFRESHMAXAGE"] = 604800

auth_manager = AuthManager(app)

@app.route("/")
# @require_token()
def get_Data():
    registro = []
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, idnodo FROM nodo.data")
            registro = cursor.fetchall()

    print(registro)

    # Cerramos la conexión
    return registro

@app.route("/nodos")
# @require_token()
def get_nodos():
    conexion = psycopg2.connect("dbname=IoT user=postgres password=12345678")
    # Creamos el cursor con el objeto conexion
    cur = conexion.cursor()

    # Ejecutamos una consulta
    cur.execute( "SELECT id, descripcion, estado, createdat FROM nodo.nodos" )

    for id, descripcion, estado, createdat in cur.fetchall() :
        print('Id: ', id, 'Descripción: ',descripcion, 'Estado: ',estado, 'Fecha creación: ',createdat)

    # Recorremos los resultados y los mostramos
    registro = cur.fetchall()    
    print(registro)

    # Cierre de la comunicación con PostgreSQL
    cur.close()
    # Cerramos la conexión
    conexion.close()
    return json.dumps(registro)

@app.route("/logs")
@require_token()
def get_logs():
    conexion = psycopg2.connect("dbname=IoT user=postgres password=12345678")
    # Creamos el cursor con el objeto conexion
    cur = conexion.cursor()

    # Ejecutamos una consulta
    cur.execute( "SELECT id, registro, createdat FROM log.logs;" )

    for id, registro, createdat in cur.fetchall() :
        print('Id: ', id, 'registro: ',registro, 'Fecha creación: ',createdat)

    # Recorremos los resultados y los mostramos
    registro = cur.fetchall()    
    print(registro)

    # Cierre de la comunicación con PostgreSQL
    cur.close()
    # Cerramos la conexión
    conexion.close()
    return json.dumps(registro)