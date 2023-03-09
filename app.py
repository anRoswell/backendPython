from http.client import HTTPException
import json
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_pyjwt import AuthManager, current_token, require_token

import psycopg2

app = Flask(__name__)
app.run(debug=True)

import logging
file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

load_dotenv()  # loads variables from .env file into environment

url = os.environ.get("DATABASE_URL")  # gets variables from environment
connection = psycopg2.connect(url) 

app.config["JWT_ISSUER"] = "Flask_PyJWT" # Issuer of tokens
app.config["JWT_AUTHTYPE"] = "HS256" # HS256, HS512, RS256, or RS512
app.config["JWT_SECRET"] = "SECRETKEY" # string for HS256/HS512, bytes (RSA Private Key) for RS256/RS512
app.config["JWT_AUTHMAXAGE"] = 3600
app.config["JWT_REFRESHMAXAGE"] = 604800

auth_manager = AuthManager(app)
print(auth_manager)

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route("/", methods=['GET'])
# @require_token()
def get_Data():
    # Cerramos la conexión
    return "Ok conectados!!!"

@app.route("/storeprocedure", methods=['GET'])
def callStoreProcedure():
    registro = []
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT procesos.sp_sensores('LISTAR', '')")
            registro = cursor.fetchall()

    print(registro)

    # Cerramos la conexión
    return registro 

@app.route("/saveInStoreProcedure", methods=['POST'])
def saveStoreProcedure():
    try:
        # opcion = request.form.get('opcion')
        opcion = 'REGISTRAR'
        sensores = ''
        print(opcion)
        sensores = {
            "fecha_hora": '',
            "tipo": 'ph',
            "valor": '001'
        }
        sensores = repr(sensores)

        print(sensores)
        response = []
        with connection:
            with connection.cursor() as cursor:
                cursor.callproc("procesos.sp_sensores", [opcion, sensores])
                response = cursor.fetchall()

        print(response)
         # Cerramos la conexión
        return response 
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

@app.route("/waterPotability", methods=['GET'])
# @require_token()
def get_waterPotability():
    registro = []
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity, potability FROM public.water_potability")
            registro = cursor.fetchall()

    print(registro)

    # Cerramos la conexión
    return registro

@app.route("/water", methods=['GET'])
def get_water():
    conexion = psycopg2.connect("dbname=postgres user=postgres password=12345678")
    # Creamos el cursor con el objeto conexion
    cur = conexion.cursor()

    # Ejecutamos una consulta
    cur.execute( "SELECT ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity, potability FROM public.water_potability" )

    for ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity, potability in cur.fetchall() :
        print('ph: ', ph, 'hardness: ', hardness, 'solids: ', solids)

    # Recorremos los resultados y los mostramos
    registro = cur.fetchall()    
    print(registro)

    # Cierre de la comunicación con PostgreSQL
    cur.close()
    # Cerramos la conexión
    conexion.close()
    return json.dumps(registro)

@app.route("/nodos", methods=['GET'])
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

@app.route("/logs", methods=['GET'])
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

# @app.route('/login', methods=['POST'])
@app.route('/login', methods=['GET'])
def do_admin_login():
    # if request.form['password'] == 'password' and request.form['username'] == 'admin':
    #     session['logged_in'] = True
    # else:
    #     return not_found()
    
    return jsonify({'response': 'wrong password'})

# Create auth and refresh tokens with the auth_manager object
# @app.route("/login")
# def post_token():
#     username = request.form["username"]
#     password = request.form["password"]

#     return {
#         "auth_token": auth_token.signed,
#         "refresh_token": refresh_token.signed
#     }, 200

@app.route('/hello', methods = ['GET'])
def api_hello():
    app.logger.info('informing')
    app.logger.warning('warning')
    app.logger.error('screaming bloody murder!')
    
    return "check your logs\n"
