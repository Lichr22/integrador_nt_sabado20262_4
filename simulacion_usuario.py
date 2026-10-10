import random
import uuid
import pandas as pd
from faker import Faker


#1. Sembrar semillas para los datos a simular
random.seed(42)
Faker.seed(42)

#2. Identificar los datos a simular con su tipo de dato
#id (texto (UUID)),
# nombre (texto)*****,
# correo (texto),
#contraseña_hash (texto),
# rol (texto),
# activo (booleano),
# fecha_registro (fecha),
# descripcion (texto),
# area_responsable (texto)*****

#3. Establecer una constante para el NUMERO DE SIMULACIONES
FILAS=250
ROLES=["administrador","empresario","estudiante","profesor"]
FALSITO = Faker("es_CO")

#4. Funcion generadora
def generar_datos(numero_filas=400):
    usuarios=[]
    for _ in range(numero_filas):
        usuarios.append({
            "id":str(uuid.uuid4()),
            "nombre":FALSITO.name(),
            "correo":FALSITO.email(),
            "contraseña_hash":FALSITO.sha256(),
            "activo":random.choice([True,False]),
            "rol":random.choice(ROLES),
            "fecha_registro":FALSITO.date_time_between(start_date="-2y",end_date="now"),
        })
    return usuarios

#5. Convirtiendo los datos generado en un dataframe con PANDAS
tabla_ordenada_usuarios=pd.DataFrame(generar_datos())

#6. Probar la funcion
print(tabla_ordenada_usuarios)

#7. Preparar la simulación para ensuciar mis datos

#7.1 Funcion para obtener una muestra de los datos
def obtener_muestra(datos, porcentaje):
    return datos.sample(fraccion=porcentaje,random_state=random.randint(0, 9999)).index

#7.2 Funcion auxiliar para cambiar valores de un texto
def escribir_mal(texto):
    variantes=[texto.lower(),texto.title(),texto.capitalize(),f" {texto} ", "Juan Jose"]
    return random.choice(variantes)

#7.3 Funcion auxilixar para cambiar los booleanos
def covertir_booleanos(valor):
    if valor:
        return random.choice(["SI", "1"])
    else: 
        return random.choice(["NO", "0"])

#7.4 Funcion principal para ensuciar los datos simulados
def ensuciar_datos(datos_df):
    datos_df=datos_df.copy()

    #Nombre el 10% tenga espacios y el 8% este en mayuscula
    filas_elegidas = obtener_muestra(datos_df, 0.1) 
    datos_df.loc[filas_elegidas, "nombre"] = " "+datos_df.loc[filas_elegidas, "nombre"]+" " 

    filas_elegidas = obtener_muestra(datos_df, 0.08) 
    datos_df.loc[filas_elegidas, "nombre"] = datos_df.loc[filas_elegidas, "nombre"].str.upper()

    #Correo: el 5% de los datos este sin @ 
    filas_elegidas = obtener_muestra(datos_df, 0.05)
    datos_df.loc[filas_elegidas, "correo"] = datos_df.loc[filas_elegidas, "correo"].str.replace("@", "")

    #Correo : el 4% de los correos no deberia tener ningun valor (None)
    filas_elegidas = obtener_muestra(datos_df, 0.04)
    datos_df.loc[filas_elegidas, "correo"] = None

    #Rol: Aplicar errores de escritura (variantes)
    filas_elegidas = obtener_muestra(datos_df, 0.1)
    datos_df.loc[filas_elegidas, "rol"] = datos_df.loc[filas_elegidas, "rol"].apply(escribir_mal)

    #Activo: En ocasiones llega SI, NO 1, 0
    datos_df["activo"] = datos_df["activo"].astype(object)
    filas_elegidas = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "activo"] = datos_df.loc[filas_elegidas, "activo"].map(covertir_booleanos)

    #Mezclar el formato de la fecha
    #ISO => YYYY-mm-dd HH-MM-SS
    #LATINO => d/m/y h:m
    iso=datos_df["fecha_registro"].dt.strtime("%Y-%m-%d %h:%M:%S")
    latino = datos_df["fecha_registro"].dt.strtime("%d/%m/%y %H:%M")
    datos_df["fecha_registro"]=iso
    filas_elegidas = obtener_muestra(datos_df, 0.25)
    datos_df.loc[filas_elegidas, "fecha_registro"] = latino.loc[filas_elegidas]

