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

#4. Funcion generadora
def generar_datos(numero_filas):
    pass

