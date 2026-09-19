import random
import uuid
from faker import Faker

#1. Sembrar semillas para los datos a simular
random.seed(42)
Faker.seed(42)

#2. Identificar los datos a simular con su tipo de dato
#id (texto (UUID)),
# nombre (texto)*****,
# descripcion (texto),
# area_responsable (texto)*****

#3. Establecer una constante para EL NUMERO DE SIMULACIONES
FILAS=250

#4. Funcion generadorea
def generar_datos(numero_filas):
    pass