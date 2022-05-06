from cmath import pi
from email import contentmanager
from email.mime import message
from functools import total_ordering
from logging.handlers import NTEventLogHandler
from operator import le
from Empresa import Empresa
from Servicio import Servicio
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom


class Manage():
    def __init__(self):
        self.positivos = []
        self.negativos = []
        self.empresas = []
        self.informacion = []

    def agregar_positivas(self, palabra):
        self.positivos.append(palabra)

    def agregar_negativas(self, palabra):
        self.negativos.append(palabra)

    def agregar_empresa(self, nombre, servicios):
        nuevo = Empresa(nombre, servicios)
        self.empresas.append(nuevo)

    def analizar(self, mensaje):

        rfecha = re.compile('(?:[0-9]{2}/){2}[0-9]{4}')
        fechas = re.findall(rfecha, mensaje)
        empreaux = ''  # nombre empresa

        for i in range(len(self.empresas)):
            empresa = self.empresas[i].nombre
            val = mensaje.find(str(empresa))
            if val != -1:
                empreaux = self.empresas[i]
                break

        contpos = 0
        for i in range(len(self.positivos)):
            palabra = self.positivos[i]
            val = mensaje.find(str(palabra))
            if val != -1:
                contpos += 1

        contneg = 0
        for i in range(len(self.negativos)):
            palabra = self.negativos[i]
            val = mensaje.find(str(palabra))
            if val != -1:
                contneg += 1

        estado = ''
        if contneg < contpos:
            estado = 'positivo'
        elif contneg > contpos:
            estado = 'negativo'
        elif contpos == contpos:
            estado = 'neutro'

        cant = 0
        cant2 = 0
        cant3 = 0
        if estado == 'positivo':
            cant = 1
        if estado == 'negativo':
            cant2 = 1
        if estado == 'neutro':
            cant3 = 1

        servicios = []
        for i in range(len(empreaux.servicios)):
            servicio = empreaux.servicios[i].nombre
            for j in range(len(empreaux.servicios[i].alias)):
                alias = empreaux.servicios[i].alias[j]
                val = mensaje.find(alias)
                if val != -1:
                    ser = {'Servicio': servicio, 'positivo': cant,
                           'Negativo': cant2, 'Neutro': cant3}
                    print(ser.get('Servicio'))
                    servicios.append(ser)

        info = {
            'fecha': fechas,
            'empresa': empreaux.nombre,
            'positivos': estado,
            'Servicios': servicios
        }

        self.informacion.append(info)
        self.informacion.sort(key=lambda x: x['fecha'])


    def prettify(self,element,indent='  '):
      queue =[(0,element)]
      while queue:
          level,element = queue.pop(0)
          children =[(level+1,child) for child in list(element)]
          if children:
              element.text = '\n' + indent * (level+1)
          if queue:
              element.tail = '\n' + indent * queue[0][0]
          else:
              element.tail = '\n' + indent * (level-1)
          queue[0:0] =children
   


    def base_datos(self):
      xml = ET.Element('lista_respuesta')
      for i in range(len(self.informacion)):
       respuetas = ET.SubElement(xml, 'respueta')
       fecha = self.informacion[i].get('fecha')
       cont = 0
       for j in range(len(self.informacion)):
           fecha2 = self.informacion[j].get('fecha')
           if fecha2 == fecha:
               cont += 1
       fechas =ET.SubElement(respuetas, 'fechas').text =  str(fecha[0])
       mensaje = ET.SubElement(respuetas, 'mensaje')
       total = ET.SubElement(mensaje, 'total').text = str(cont)
       men = self.informacion[i]
       pos = 0
       neg = 0
       neutro = 0
       
       for k in range(len(men.get('Servicios'))):
           pos = men.get('Servicios')[k].get('positivo')
           neg = men.get('Servicios')[k].get('Negativo')
           neutro = men.get('Servicios')[k].get('Neutro')
        
       positivo = ET.SubElement(mensaje, 'positivos').text = str(pos)
       negativo = ET.SubElement(mensaje, 'negativos').text = str(neg)
       neutros = ET.SubElement(mensaje, 'neutros').text = str(neutro)
       analisis = ET.SubElement(respuetas, 'analisis')
       empresa = ET.SubElement(analisis, 'empresa' , nombre =str(self.informacion[i].get('empresa')) )
       mensaje2 = ET.SubElement(empresa, 'mensaje')
       positivo1 = ET.SubElement(mensaje2, 'positivos').text = str(pos)
       negativo1 = ET.SubElement(mensaje2, 'negativos').text = str(neg)
       neutros1= ET.SubElement(mensaje2, 'neutros').text = str(neutro)
       servicos = ET.SubElement(empresa, 'servicios')
       for k in range(len(men.get('Servicios'))):
        serviciosname = men.get('Servicios')[k].get('Servicio') 
        pos = men.get('Servicios')[k].get('positivo')
        neg = men.get('Servicios')[k].get('Negativo')
        neutro = men.get('Servicios')[k].get('Neutro')
        total = pos + neg + neutro
        servicio = ET.SubElement(servicos,'servicio', nombre = serviciosname)
        mensaje3 = ET.SubElement(servicio,'mensaje')
        total = ET.SubElement(mensaje3,'total').text = str(total)
        positivo1 = ET.SubElement(mensaje3, 'positivos').text = str(pos)
        negativo1 = ET.SubElement(mensaje3, 'negativos').text = str(neg)
        neutros1= ET.SubElement(mensaje3, 'neutros').text = str(neutro)
 
      xml_estadisticas = ET.tostring(xml, 'utf-8')
      xml_parseado = minidom.parseString(xml_estadisticas).toprettyxml(indent='\t')

      f = open('base_datos.xml', 'w')
      f.write(xml_parseado)
      f.close()

    def prueba(self, mensaje):
        rfecha = re.compile('(?:[0-9]{2}/){2}[0-9]{4}')
        fechas = re.findall(rfecha, mensaje)
        usuario=''
        red = ''
        empreaux = ''
        total = 0
        palabras = mensaje.split()
        for i in range(len(palabras)):
            palabra = palabras[i]
            if palabra =='Usuario:':
                usuario = palabras[i+1]
            if palabra == 'social:':
                red = palabras[i+1]
        
        for i in range(len(self.empresas)):
            empresa = self.empresas[i].nombre
            val = mensaje.find(str(empresa))
            if val != -1:
                empreaux = self.empresas[i]
                break
        
        contpos = 0
        for i in range(len(self.positivos)):
            palabra = self.positivos[i]
            val = mensaje.find(str(palabra))
            if val != -1:
                contpos += 1
                total += 1

        contneg = 0
        for i in range(len(self.negativos)):
            palabra = self.negativos[i]
            val = mensaje.find(str(palabra))
            if val != -1:
                contneg += 1
                total += 1

        estado = ''
        if contneg < contpos:
            estado = 'positivo'
        elif contneg > contpos:
            estado = 'negativo'
        elif contpos == contpos:
            estado = 'neutro'

        
        
        #porcentajepos = (contpos/total)*100
        #porcentajeneg = (contneg/total)*100
        xml = ET.Element('respuesta')
        fecha = ET.SubElement(xml, 'fecha').text = str(fechas[0])
        redsocial = ET.SubElement(xml, 'red_social').text = red
        user = ET.SubElement(xml, 'usuario').text = usuario
        empresas = ET.SubElement(xml, 'empresas')
        empresa = ET.SubElement(empresas,'empresa',nombre = str(empreaux.nombre))
        for i in range(len(empreaux.servicios)):
            servicio = empreaux.servicios[i].nombre
            for j in range(len(empreaux.servicios[i].alias)):
                alias = empreaux.servicios[i].alias[j]
                val = mensaje.find(alias)
                if val != -1:
                  servicios = ET.SubElement(empresa,'servicio').text = str(servicio)
        palabrapos = ET.SubElement(xml,'palabras_positivas').text = str(contpos)
        palabrasneg = ET.SubElement(xml,'palabras_negativas').text = str(contneg)
        sentipos = ET.SubElement(xml,'sentimiento_positivos').text = str(0)+'%'
        sentineg = ET.SubElement(xml,'sentimiento_negativos').text = str(0)+'%'
        sentimiento = ET.SubElement(xml,'sentimiento_analizado').text = estado
        xml_estadisticas = ET.tostring(xml, 'utf-8')
        xml_parseado = minidom.parseString(xml_estadisticas).toprettyxml(indent='\t')

        f = open('prueba.xml', 'w')
        f.write(xml_parseado)
        f.close()

        
    
