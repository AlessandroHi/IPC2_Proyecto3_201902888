from cgi import print_form
from cmath import pi
import re
import os
import xml.etree.ElementTree as ET
from flask import Flask, json
from flask import jsonify
from flask.globals import request
from flask_cors import CORS
from xml.dom import minidom
from Servicio import Servicio
from Manage import Manage

global archivo

manage = Manage() #SE USARA PARA EL MANEJO DE INFORMACION Y GET 

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET']) # LA INICIALIZACION DE LA APi
def index():
    return('Api en Flask')

@app.route('/add', methods=['POST']) #MANEJO DE ARCHIVOS XML
def add_various():
    archivo = request.files['archivo']
    tree = ET.parse(archivo)
    raiz = tree.getroot()
    for diccionario in raiz.iter('diccionario'):
        pass
        for positivos in diccionario.iter('sentimientos_positivos'):
            pass
            for palabra in positivos:
               manage.agregar_positivas(palabra.text.replace(' ','')) # SE AGREGAN LAS PALABRAS POSITIVAS AL DICCIONARIO
        for negativo in diccionario.iter('sentimientos_negativos'):
            pass
            for palabra in negativo:
               manage.agregar_negativas(palabra.text) # SE AGREGAN LAS PALABRAS NEGATIVAS AL DICCIONARIO
        for empresas in diccionario.iter('empresas_analizar'):
                pass
                for empresa in empresas.iter('empresa'):
                   pass
                   for nombre in empresa.iter('nombre'):
                       name = nombre.text
                       List_services = []
                   for sevicio in empresa.iter('servicio'):
                       nombreser = sevicio.attrib['nombre']
                       List_aliasServices = []
                       for alias in sevicio.iter('alias'):
                           List_aliasServices.append(alias.text)
                       List_services.append(Servicio(nombreser.lower(),List_aliasServices))
                   manage.agregar_empresa(name,List_services)
    for mensajes in raiz.iter('lista_mensajes'):
        pass
        for  mensaje in mensajes.iter('mensaje'):
            manage.analizar(mensaje.text.replace('\t',''))

    manage.base_datos()

    return jsonify({'ok':True, 'msg':'Archivo XML cargado correctamente...'}), 200

@app.route('/prueba', methods=['POST']) #MANEJO DE MENSAJE PRUEBA
def add_prueba():
    xml = request.data.decode('UTF-8')
    raiz = ET.XML(xml)
    for  mensaje in raiz.iter('mensaje'):
            manage.prueba(mensaje.text.replace('\t',''))

    return jsonify({'ok':True, 'msg':'Archivo XML cargado correctamente...'}), 200

@app.route('/consultar', methods=['GET'])
def consultar():
    if request.method != 'GET':
        return 'Peticion no válida'
    file = open('base_datos.xml', 'r')
    contenido = ''.join(file.readlines())
    file.close()
    return contenido

@app.route('/consultar2', methods=['GET'])
def consultar2():
    if request.method != 'GET':
        return 'Peticion no válida'
    file = open('prueba.xml', 'r')
    contenido = ''.join(file.readlines())
    file.close()
    return contenido

@app.route('/reset', methods=['GET'])
def reset():
    os.remove('base_datos.xml')
    return('Api reiniciada')

@app.route('/documentacion', methods=['GET'])
def documentacion():
    if request.method != 'GET':
        return 'Petición no válida'
    file = "Ensayo.pdf"
    os.popen(file)
    return 'Abriendo documentacion...'



if __name__ == "__main__":
    app.run(port=5000, debug=True)