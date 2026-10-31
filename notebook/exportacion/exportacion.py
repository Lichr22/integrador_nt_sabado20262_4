#Rutina para convertir una lista de diccionarios en multiples fuentes de informacion
import json
from pathlib import Path

#1. Configuracion (cambiar segun su tabla)
NOMBRE_ENTIDAD="usuario"
CARPETA_PROYECTO=Path(__file__).resolve().parents[2]
CARPETA_CRUDOS=CARPETA_PROYECTO/"datos"/"crudos"
CARPETA_LIMPIOS=CARPETA_PROYECTO/"datos"/"limpios"
CARPETA_REPORTES=CARPETA_PROYECTO/"datos"/"reportes"

#2. Funciones genericas para elaborar los archivos

#2.1 CREAR LA CARPETA SI NO EXISTE
def preparar_carpeta(carpeta):
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta

#2.2 EXPORTAR A CSV
def exportar_csv(datos_df,carpeta,nombre_archivo):
    ruta=preparar_carpeta(carpeta)/f"{nombre_archivo}.csv"
    datos_df.to_csv(ruta,index=False,sep=";",encoding="utf-8-sig")
    return ruta

#2.3 EXPORTAR A JSON
def exportar_json(datos_df,carpeta,nombre_archivo):
    ruta=preparar_carpeta(carpeta)/f"{nombre_archivo}.json"
    #force_ascii=False permite ver tildes y ñ en el archivo
    datos_df.to_json(ruta,orient="records",date_format="iso",indent=2,force_ascii=False)
    return ruta

#2.4 EXPORTAR A EXCEL
def exportar_excel(datos_df,carpeta,nombre_archivo):
    ruta=preparar_carpeta(carpeta)/f"{nombre_archivo}.xlsx"
    try:
        datos_df.to_excel(ruta, index=False, engine="openpyxl")
    except ImportError:
        print(f"[ADVERTENCIA] No se pudo exportar a Excel ({ruta.name}). Falta instalar: pip install openpyxl")
        return None
    return ruta

#3. Genero los archivos en mi proyecto

# --- Entidad: USUARIO ---
def exportar_usuarios_crudos(datos_sucios_df):
    return [
        exportar_csv(datos_sucios_df,CARPETA_CRUDOS,f"{NOMBRE_ENTIDAD}_crudo"),
        exportar_json(datos_sucios_df,CARPETA_CRUDOS,f"{NOMBRE_ENTIDAD}_crudo"),
        exportar_excel(datos_sucios_df,CARPETA_CRUDOS,f"{NOMBRE_ENTIDAD}_crudo")
    ]

def exportar_usuarios_limpios(datos_limpios_df):
    return [
        exportar_csv(datos_limpios_df,CARPETA_LIMPIOS,f"{NOMBRE_ENTIDAD}_limpio"),
        exportar_json(datos_limpios_df,CARPETA_LIMPIOS,f"{NOMBRE_ENTIDAD}_limpio"),
        exportar_excel(datos_limpios_df,CARPETA_LIMPIOS,f"{NOMBRE_ENTIDAD}_limpio")
    ]

# --- Entidad: EMPRESA ---
def exportar_empresas_crudos(datos_sucios_df):
    return [
        exportar_csv(datos_sucios_df,CARPETA_CRUDOS,"empresa_crudo"),
        exportar_json(datos_sucios_df,CARPETA_CRUDOS,"empresa_crudo"),
        exportar_excel(datos_sucios_df,CARPETA_CRUDOS,"empresa_crudo")
    ]

def exportar_empresas_limpios(datos_limpios_df):
    return [
        exportar_csv(datos_limpios_df,CARPETA_LIMPIOS,"empresa_limpio"),
        exportar_json(datos_limpios_df,CARPETA_LIMPIOS,"empresa_limpio"),
        exportar_excel(datos_limpios_df,CARPETA_LIMPIOS,"empresa_limpio")
    ]

# --- Entidad: CATEGORIA ---
def exportar_categorias_crudos(datos_sucios_df):
    return [
        exportar_csv(datos_sucios_df,CARPETA_CRUDOS,"categoria_crudo"),
        exportar_json(datos_sucios_df,CARPETA_CRUDOS,"categoria_crudo"),
        exportar_excel(datos_sucios_df,CARPETA_CRUDOS,"categoria_crudo")
    ]

def exportar_categorias_limpios(datos_limpios_df):
    return [
        exportar_csv(datos_limpios_df,CARPETA_LIMPIOS,"categoria_limpio"),
        exportar_json(datos_limpios_df,CARPETA_LIMPIOS,"categoria_limpio"),
        exportar_excel(datos_limpios_df,CARPETA_LIMPIOS,"categoria_limpio")
    ]

# --- Funcion generica para cualquier entidad ---
def exportar_crudos(datos_sucios_df, entidad=NOMBRE_ENTIDAD):
    return [
        exportar_csv(datos_sucios_df,CARPETA_CRUDOS,f"{entidad}_crudo"),
        exportar_json(datos_sucios_df,CARPETA_CRUDOS,f"{entidad}_crudo"),
        exportar_excel(datos_sucios_df,CARPETA_CRUDOS,f"{entidad}_crudo")
    ]

def exportar_limpios(datos_limpios_df, entidad=NOMBRE_ENTIDAD):
    return [
        exportar_csv(datos_limpios_df,CARPETA_LIMPIOS,f"{entidad}_limpio"),
        exportar_json(datos_limpios_df,CARPETA_LIMPIOS,f"{entidad}_limpio"),
        exportar_excel(datos_limpios_df,CARPETA_LIMPIOS,f"{entidad}_limpio")
    ]

