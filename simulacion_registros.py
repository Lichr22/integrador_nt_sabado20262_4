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
 fecha_registro (fecha), 
 observacion (texto), 
 estado (texto),
id_usuario (texto (UUID)), 
id_reto (texto (UUID))
'''

#3. Establecer una constante para el número de simulaciones
FILAS=800
ESTADOS=["Activo","No Activo","Bloqueado","En revisión","en_curso","EN CURSO","Cerrado"]
IDS_USUARIO=[321,123,456,654,789]
IDS_RETO=[1,2,3,4,5]
falsito=Faker("es_CO")
fecha_inicio=falsito.date_time_between(start_date="-1y", end_date="+3m")

#4. Funcion generadora
def generar_datos(numero_filas=800):
    registros=[]
    for _ in range(numero_filas):
        registros.append({
            "id":str(uuid.uuid4()),
            "fecha_registro":falsito.date_time_between(start_date="-1y", end_date="now"),
            "observacion":falsito.sentence(nb_words=10),
            "estado":random.choice(ESTADOS),
            "id_usuario":random.choice(IDS_USUARIO),
            "id_reto":random.choice(IDS_RETO)
            })
    return registros

#5. Convirtiendo los datos generados en un dataFrame con PANDAS
tabla_ordenada_registros=pd.DataFrame(generar_datos())

#6. Probar la funcionón
print(tabla_ordenada_registros)

#7. Preparar la simulación para ensuciar los datos

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
     datos_df=datos_df.copy()

     filas_elegidas=obtener_muestra(datos_df,0.2)
     datos_df.loc[filas_elegidas,"observación"]= None

     filas_elegidas=obtener_muestra(datos_df,0.1)
     datos_df.loc[filas_elegidas,"estado"]=datos_df.loc[filas_elegidas,"estado"].map(escribir_mal)

     #Nezclar el formato de la fecha
     #ISO = 2026-10-03 YYYY-mm-dd
     #LATINO = d/m/y h:m

     iso=datos_df["fecha_registro"].dt.strtime("%Y-%m-%d %H:%M:%S")
     latino=datos_df["fecha_registro"].dt.strtime("%d/%m/8%y %H:%M")
     datos_df["fecha_registro"]=iso
     filas_elegidas=obtener_muestra(datos_df,0.25)
     datos_df.loc[filas_elegidas,"fecha_registro"]=latino.loc[filas_elegidas]

     filas_elegidas = obtener_muestra(datos_df, 0.10)
     filas_origen = obtener_muestra(datos_df, 0.10)
     datos_df.loc[filas_elegidas, ["id_usuario", "id_reto"]] = datos_df.loc[filas_origen, ["id_usuario", "id_reto"]].values

     # 5% de las filas repetidas tal cual (duplicados exactos)
     filas_elegidas = obtener_muestra(datos_df, 0.05)
     duplicados_exactos = datos_df.loc[filas_elegidas].copy()
     datos_df = pd.concat([datos_df, duplicados_exactos], ignore_index=True)

