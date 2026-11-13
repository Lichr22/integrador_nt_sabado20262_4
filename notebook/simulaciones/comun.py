"""
Utilidades compartidas por todas las simulaciones.

- Semilla única para que cada ejecución produzca exactamente los mismos datos.
- Fecha de referencia fija: las fechas simuladas no dependen del día en que se ejecute.
- Identificadores UUID deterministas (uuid5) por entidad e índice, de modo que las
  llaves foráneas de 'retos' y 'registros' apunten a ids que existen realmente.
"""

import random
import uuid
from datetime import datetime, timedelta

from faker import Faker

SEMILLA = 42

# Las fechas "relativas" (hace 1 año, hasta hoy, dentro de 3 meses) se calculan
# respecto a esta fecha fija, no respecto a datetime.now().
FECHA_REFERENCIA = datetime(2026, 10, 31)

# Espacio de nombres propio del proyecto para generar los UUID deterministas.
_ESPACIO_IDS = uuid.uuid5(uuid.NAMESPACE_DNS, "integrador-nt-sabado20262-4")


def sembrar(semilla: int = SEMILLA) -> None:
    """Reinicia las semillas de random y Faker antes de generar una entidad."""
    random.seed(semilla)
    Faker.seed(semilla)


def generar_id(entidad: str, indice: int) -> str:
    """Devuelve el UUID determinista de la fila `indice` de la `entidad`."""
    return str(uuid.uuid5(_ESPACIO_IDS, f"{entidad}-{indice}"))


def ids_de(entidad: str, cantidad: int) -> list[str]:
    """Devuelve los `cantidad` ids que genera la simulación de `entidad`."""
    return [generar_id(entidad, i) for i in range(cantidad)]


def hace_dias(dias: int) -> datetime:
    """Fecha `dias` días antes de FECHA_REFERENCIA (usa negativos para el futuro)."""
    return FECHA_REFERENCIA - timedelta(days=dias)
