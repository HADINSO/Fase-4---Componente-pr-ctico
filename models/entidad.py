"""
Clase abstracta base Entidad.

Define la estructura común de todas las entidades del sistema:
identificador y fecha de creación. Impide la instanciación directa
y obliga a las subclases a implementar los métodos abstractos validar()
y to_dict().
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """Entidad base del dominio de SOFTWARE FJ."""

    def __init__(self, identificador):
        if identificador is None or str(identificador).strip() == "":
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio")
        self._identificador = str(identificador).strip()
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self):
        """Identificador único de la entidad (solo lectura)."""
        return self._identificador

    @property
    def fecha_creacion(self):
        """Fecha y hora de creación de la entidad (solo lectura)."""
        return self._fecha_creacion

    @abstractmethod
    def validar(self):
        """Valida la integridad de los datos de la entidad."""
        pass

    @abstractmethod
    def to_dict(self):
        """Convierte la entidad a un diccionario para registro o reporte."""
        pass

    def __str__(self):
        return f"{self.__class__.__name__}(identificador={self._identificador})"

    def __repr__(self):
        return self.__str__()
