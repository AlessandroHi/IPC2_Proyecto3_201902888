from ctypes import set_errno


class Empresa():
    def __init__(self, nombre, servicios):
        self.nombre = nombre
        self.servicios = servicios


if __name__ == "__main__":
    informaciones =[]

    mensaje ={
        'fecha': '1997/05/12',
        'nombre': 'hola',
        'tipo': 'TIPO',
        'edad': 'EDAD',
        'Servicios': [{'Servicio': 'a', 'positivo':1,'Negativo':1,'Neutro':0},
        {'Servicio': 'hol1', 'positivo':1,'Negativo':1,'Neutro':0},]

    }
    informaciones.append(mensaje)

    servicios = []
    servicios.append({'Servicio': 'escribi', 'positivo':1,'Negativo':1,'Neutro':0})
    servicios.append({'Servicio': 'graduacion', 'positivo':1,'Negativo':1,'Neutro':0})
    servicios.append({'Servicio': 'graduacion122', 'positivo':1,'Negativo':1,'Neutro':0})


    mensaje ={
        'fecha': '1998/03/12',
        'nombre': 'hola1',
        'tipo': 'tipo1',
        'edad': 'edad1',
        'Servicios':servicios,
    }
    informaciones.append(mensaje)

    mensaje ={
        'fecha': '1988/03/22',
        'nombre': 'hola2',
        'tipo': 'tipo2',
        'edad': 'edad1',
        'Servicios': [{'Servicio': 'hola', 'positivo':1,'Negativo':1,'Neutro':0},
        {'Servicio': 'hoal1', 'positivo':1,'Negativo':1,'Neutro':0},]

    }
    informaciones.append(mensaje)
    
    informaciones.sort(key=lambda x:x['fecha'])
   
    uno = 2
    dos = 2
    total = 4
    proce = (uno/total)*100
    print(proce)
    