"""
Clase abstracta Servicio y servicios especializados.

Servicio define la interfaz común (calcular_costo, describir_servicio,
validar_parametros). ReservaSala, AlquilerEquipo y AsesoriaEspecializada
sobrescriben estos métodos con su propia lógica, demostrando polimorfismo.
"""

from abc import abstractmethod
from exceptions.excepciones_personalizadas import (
    ServicioInvalidoError,
    CalculoCostoError,
    ParametroFaltanteError,
)
from utils.validaciones import validar_precio, validar_entero_positivo, validar_no_vacio
from models.entidad import Entidad


class Servicio(Entidad):
    """Servicio ofrecido por SOFTWARE FJ (clase abstracta)."""

    def __init__(self, codigo, nombre, descripcion, precio_base, disponible=True, estado="ACTIVO"):
        super().__init__(codigo)
        self._nombre = None
        self._descripcion = None
        self._precio_base = None
        self._disponible = bool(disponible)
        self._estado = str(estado).upper().strip()

        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_base = precio_base

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_no_vacio(valor, "nombre del servicio")

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = validar_no_vacio(valor, "descripción del servicio")

    @property
    def precio_base(self):
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor):
        self._precio_base = validar_precio(valor, "precio base")

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        self._estado = str(valor).upper().strip()

    @abstractmethod
    def calcular_costo(self, cantidad=1, impuesto=0.0, descuento=0.0):
        """Calcula el costo del servicio (variantes de argumentos)."""
        pass

    @abstractmethod
    def describir_servicio(self):
        """Devuelve una descripción legible del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self):
        """Valida los parámetros específicos del servicio."""
        pass

    def to_dict(self):
        return {
            "codigo": self.identificador,
            "nombre": self._nombre,
            "descripcion": self._descripcion,
            "precio_base": self._precio_base,
            "disponible": self._disponible,
            "estado": self._estado,
            "tipo": self.__class__.__name__,
            "fecha_creacion": self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def __str__(self):
        return (f"{self.__class__.__name__}(codigo={self.identificador}, "
                f"nombre={self._nombre}, precio_base={self._precio_base}, "
                f"disponible={self._disponible})")
