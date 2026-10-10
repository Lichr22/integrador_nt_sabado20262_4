import random
import uuid
import pandas as pd
from faker import Faker

# 1. Sembrar Semillas para los datos a simular
random.seed(42)
Faker.seed(42)

# 2. identificar los datos a similiar con su tipo de dato
# id (texto (UUID)), 
# nombre (texto), 
# nivel (entero), 
# dias_max_respuesta (entero).

# 3. Establecer una constante para el NUMERO DE SIMULACIONES
FILAS = 200

# 5 prioridades reales
NIVELES = {
    "muy baja": 1,
    "baja": 2,
    "media": 3,
    "alta": 4,
    "critica": 5
}

# Dias de respuesta segun el nivel
DIAS = {
    1: 10,
    2: 7, 
    3: 5, 
    4: 2, 
    5: 1
}

# 7 Preparar simulacion para ensuciar datos

# 7.1 funcion para obtener una muestra de los datos
def obtener_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index

# 7.2 funcion auxiliar para cambiar valores de un texto
def escribir_mal(texto):
    variantes=[texto.lower(),texto.title(), texto.capitalize(), f" {texto} ", "Andres"]
    return random.choice(variantes)

# 7.4 funcion principal para ensuciar los datos simulados
def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # Ensuciar 'nombre': variantes como MAYUSCULAS, con espacios, o Capitalizado ('ALTA', ' alta ', 'Alta')
    filas_nombre = obtener_muestra(datos_df, 0.30)
    def variar_nombre(nombre):
        variantes = [nombre.upper(), f" {nombre} ", nombre.capitalize()]
        return random.choice(variantes)
    datos_df.loc[filas_nombre, "nombre"] = datos_df.loc[filas_nombre, "nombre"].apply(variar_nombre)

    # Convertir a object para soportar textos, nulos y numeros mezclados
    datos_df["nivel"] = datos_df["nivel"].astype(object)

    # Ensuciar 'nivel': 7% en None
    filas_nivel_none = obtener_muestra(datos_df, 0.07)
    datos_df.loc[filas_nivel_none, "nivel"] = None

    # Ensuciar 'nivel': a veces como TEXTO ('3') o la palabra ('tres')
    mapa_palabras = {1: "uno", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco"}
    
    idx_not_null = datos_df[datos_df["nivel"].notna()].index
    num_ensuciar = int(len(idx_not_null) * 0.20)
    filas_nivel_texto = pd.Series(idx_not_null).sample(n=num_ensuciar, random_state=42).values
    
    def ensuciar_nivel(val):
        if pd.isna(val): return val
        val_int = int(val)
        return random.choice([str(val_int), mapa_palabras[val_int]])
        
    datos_df.loc[filas_nivel_texto, "nivel"] = datos_df.loc[filas_nivel_texto, "nivel"].apply(ensuciar_nivel)

    # Ensuciar 'dias_max_respuesta': 5% en None y 3% con un valor absurdo (999)
    filas_dias_none = obtener_muestra(datos_df, 0.05)
    datos_df.loc[filas_dias_none, "dias_max_respuesta"] = None
    
    filas_dias_absurdos = obtener_muestra(datos_df, 0.03)
    datos_df.loc[filas_dias_absurdos, "dias_max_respuesta"] = 999

    # 8% de las filas repetidas tal cual (duplicados exactos)
    num_duplicados = int(len(datos_df) * 0.08)
    filas_duplicadas = datos_df.sample(n=num_duplicados, random_state=random.randint(0, 9999))
    datos_df = pd.concat([datos_df, filas_duplicadas], ignore_index=True)

    return datos_df

# 4. Funcion generadora
def generar_prioridades(n=200):
    prioridades = []
    for _ in range(n):
        nombre = random.choice(list(NIVELES.keys()))
        nivel = NIVELES[nombre]
        dias = DIAS[nivel]
        
        prioridades.append({
            "id": str(uuid.uuid4()),
            "nombre": nombre,
            "nivel": nivel,
            "dias_max_respuesta": dias,
        })
    
    # 5. Conviertiendo los datos generados en un dataframe con pandas 
    df_limpio = pd.DataFrame(prioridades)
    df_sucio = ensuciar(df_limpio)
    
    return df_sucio

# 6. probar la funcion
if __name__ == "__main__":
    df = generar_prioridades(FILAS)
    print("--- FORMA DEL DATAFRAME ---")
    print(df.shape)
    
    print("\n--- PRIMEROS REGISTROS ---")
    print(df.head())
    
    print("\n--- VALORES NULOS POR COLUMNA ---")
    print(df.isna().sum())
