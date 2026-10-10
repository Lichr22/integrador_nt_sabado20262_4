'''
El elemento central: la necesidad que publica la empresa. Crea el script `src/simular_retos.py`. 
Con la libreria **Faker** genera 500 filas falsas de la tabla `retos`, con las MISMAS columnas que usa Backend II.
Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos 
distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el
mismo y tu compañero pueda reproducirlo.
'''

import random
import uuid
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker


#1. Sembrar semillas para los datos a simular
random.seed(42)
Faker.seed(42)

#2. Identificar los datos a simular con su tipo de dato
'''
 id (texto (UUID)), 
 nombre (texto), 
 descripcion (texto), 
 fecha_inicio (fecha), 
 fecha_fin (fecha), 
 estado (texto),
id_empresa (texto (UUID)), 
id_categoria (texto (UUID)), 
id_prioridad (texto (UUID)).
'''

#3. Establecer una constante para el número de simulaciones
FILAS=500
ESTADOS=["Activo","No Activo","Bloqueado","En revisión","en_curso","EN CURSO","Cerrado"]
IDS_EMPRESA=[321,123,456,654,789]
IDS_CATEGORIA=[1,2,3,4,5]
IDS_PRIORIDAD=[1,2,3,4,5]
falsito=Faker("es_CO")
fecha_inicio=falsito.date_time_between(start_date="-1y", end_date="+3m")

#4. Funcion generadora
def generar_datos(numero_filas=500):
    retos=[]
    for _ in range(numero_filas):
        retos.append({
            "id":str(uuid.uuid4()),
            "nombre":falsito.sentence(nb_words=6).rstrip("."),
            "descripcion":falsito.sentence(nb_words=12),
            "fecha_inicio":falsito.date_time_between(start_date="-1y", end_date="+3m"),
            "fecha_fin":fecha_inicio + timedelta(days=random.randint(15, 180)),
            "estado":random.choice(ESTADOS),
            "id_empresa":random.choice(IDS_EMPRESA),
            "id_categoria":random.choice(IDS_CATEGORIA),
            "id_prioridad":random.choice(IDS_PRIORIDAD)
        })
    return retos

#5. Convirtiendo los datos generados en un dataFrame con PANDAS
tabla_ordenada_retos=pd.DataFrame(generar_datos())

#Probar la funcionón
print(tabla_ordenada_retos)

#7.1 Funcion para obtener una muestra de los datos


#7.1 Funcion para obtener una muestra de los datos
def obtener_muestra(datos,porcentaje):
    return datos.sample(fraccion=porcentaje,random_state=random.randint(0,9999)).index

#7.2 Función auxiliar para cambiar valores de un texto
def escribir_mal(texto):
    variantes=[texto.lower(), texto.title(), texto.capitalize(), f" {texto} ", "JuanJo"]
    return random.choice(variantes)

#7.3 Funcion auxiliar para cambiar los booleanos
def convertir_booleano(valor):
        if valor:
             return random.choice(["SI","1"])
        else:
             return random.choice(["NO","0"])

#7.4 Funcion principal para ensuciar los datos simulados
def ensuciar(datos_df):
     # 5% de las filas repetidas tal cual (duplicados exactos)
     filas_elegidas = obtener_muestra(datos_df, 0.05)
     duplicados_exactos = datos_df.loc[filas_elegidas].copy()
     datos_df = pd.concat([datos_df, duplicados_exactos], ignore_index=True)

     # Nombre: 10% con espacios sobrantes
     filas_elegidas = obtener_muestra(datos_df, 0.10)
     datos_df.loc[filas_elegidas, "nombre"] = "  " + datos_df.loc[filas_elegidas, "nombre"] + "  "

     # Descripcion: 12% en None (nulos)
     filas_elegidas = obtener_muestra(datos_df, 0.12)
     datos_df.loc[filas_elegidas, "descripcion"] = None

     # Fecha_inicio: dos formatos mezclados ("2026-03-02" y "02/03/2026")
     iso_fi = datos_df["fecha_inicio"].dt.strftime("%Y-%m-%d")
     latino_fi = datos_df["fecha_inicio"].dt.strftime("%d/%m/%Y")
     datos_df["fecha_inicio"] = iso_fi
     filas_elegidas = obtener_muestra(datos_df, 0.50)  # 50% de cada formato para mezclar
     datos_df.loc[filas_elegidas, "fecha_inicio"] = latino_fi.loc[filas_elegidas]

     # Fecha_fin: 8% en None y 5% ANTERIOR a fecha_inicio (error lógico)
     filas_elegidas = obtener_muestra(datos_df, 0.08)
     datos_df.loc[filas_elegidas, "fecha_fin"] = None

     filas_elegidas = obtener_muestra(datos_df, 0.05)
     # Convertimos temporalmente a datetime para restar días y asegurar que sea anterior
     fechas_dt = pd.to_datetime(datos_df.loc[filas_elegidas, "fecha_inicio"], errors="coerce")
     datos_df.loc[filas_elegidas, "fecha_fin"] = (fechas_dt - pd.Timedelta(days=5)).dt.strftime("%Y-%m-%d")

     filas_elegidas=obtener_muestra(datos_df,0.1)
     datos_df.loc[filas_elegidas,"estado"]=datos_df.loc[filas_elegidas,"estado"].map(escribir_mal)