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

#3. Establecer una constante para EL NUMERO DE SIMULACIONES
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
