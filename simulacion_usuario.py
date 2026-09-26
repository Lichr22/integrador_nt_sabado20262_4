import random
import uuid
import pandas as pd
from faker import Faker

#1. Sembrar Semillas para los datos a simular
random.seed(42)
Faker.seed(42)

#2. identificar los datos a similiar con su tipo de dato
# id (texto(UUID)),
# nombre (texto)****,
# correo (texto),
# contrasena_hash(texto),
# rol (texto)*****,
# activo(boolean),
# fecha(texto)***,

#3. Establecer una constante para el NUMERO DE SIMULACIONES
FILAS=250
ROLES=["administrador", "empresario", "estudiante", "profesor"]
FALSITO = Faker("es_CO")


#4. Funcion generadora
def generar_datos(numero_filas=400):
    usuarios=[]
    for _ in range(numero_filas):
        usuarios.append({
            "id": str(uuid.uuid4()),
            "nombre": FALSITO.name(),
            "correo": FALSITO.email(),
            "contrasena_hash":FALSITO.sha256(),
            "activo":random.choice([True,False]),
            "fecha_registro":FALSITO.date_time_between(start_date="-2y", end_date="now"),


        })
    return usuarios

#5. Conviertiendo los datos generados en un dataframe con pandas 
tabla_ordenada_usuarios=pd.DataFrame(generar_datos())


#5. probar la funcion
print(tabla_ordenada_usuarios)