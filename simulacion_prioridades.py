import random
import uuid
import pandas as pd
from faker import Faker

#1. Sembrar Semillas para los datos a simular
random.seed(42)
Faker.seed(42)

FILAS=200
NIVELES={"bajo": 1,    "medio": 2,    "alto": 3}
DIAS={1: 5,  2: 3, 3: 1}

#2. identificar los datos a similiar con su tipo de dato
#id (texto (UUID)), 
#nombre (texto), 
#nivel (entero), 
#dias_max_respuesta (entero).


def generar_datos(numero_filas=200):
    prioridades=[]
    for _ in range(numero_filas):
        prioridades.append({
            "id":str(uuid.uuid4()),
            "nombre":random.choice(list(NIVELES.keys())),
            "nivel":'NIVELES[nombre]',
            "dias_max_respuesta":'DIAS[nivel]',
        })
    return prioridades

tabla_ordenada_prioridades=pd.DataFrame(generar_datos())

print(tabla_ordenada_prioridades) 


def obtener_muestra(datos, porcentaje):
    
    return datos.sample(fraccion=porcentaje, random_state=random.randint(0,9999)).index

#7.2 funcion auxiliar para cambiar valores de un texto
def escribir_mal(texto):
    variantes=[texto.lower(),texto.title(), texto.capitalize(), f" {texto} ", "Andres"]
    return random.choice(variantes)

#7.3 funcion auxiliar para cambiar los booleanos
def convertir_booleano(valor):
    if valor:
        return random.choice(["SI","1"])
    else:
        return random.choice(["NO","0"])
