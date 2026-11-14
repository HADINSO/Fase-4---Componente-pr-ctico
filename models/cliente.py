"""
Modelo Cliente.

Representa a un cliente de SOFTWARE FJ. Hereda de Entidad y encapsula
los datos personales con propiedades getter/setter y validaciones rigurosas.
"""

from datetime import datetime
from exceptions.excepciones_personalizadas import (
    ClienteInvalidoError,
    ParametroFaltanteError,
)
from utils.validaciones import (
    validar_correo_electronico,
    validar_identificacion,
    validar_telefono,
    validar_nombre,
)
from models.entidad import Entidad


class Cliente(Entidad):
    """Cliente del sistema SOFTWARE FJ."""

    ESTADO_ACTIVO = "ACTIVO"
    ESTADO_INACTIVO = "INACTIVO"

    def __init__(self, identificador, nombre_completo, numero_identificacion,
                 correo_electronico, telefono, estado=ESTADO_ACTIVO):
        super().__init__(identificador)
        self._nombre_completo = None
        self._numero_identificacion = None
        self._correo_electronico = None
        self._telefono = None
        self._fecha_registro = datetime.now()
        self._estado = None

        self.nombre_completo = nombre_completo
        self.numero_identificacion = numero_identificacion
        self.correo_electronico = correo_electronico
        self.telefono = telefono
        self.estado = estado

    # ---------------- Propiedades ----------------

    @property
    def nombre_completo(self):
        return self._nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, valor):
        self._nombre_completo = validar_nombre(valor)

    @property
    def numero_identificacion(self):
        return self._numero_identificacion

    @numero_identificacion.setter
    def numero_identificacion(self, valor):
        self._numero_identificacion = validar_identificacion(valor)

    @property
    def correo_electronico(self):
        return self._correo_electronico

    @correo_electronico.setter
    def correo_electronico(self, valor):
        self._correo_electronico = validar_correo_electronico(valor)

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        self._telefono = validar_telefono(valor)

    @property
    def fecha_registro(self):
        return self._fecha_registro

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        valor = str(valor).upper().strip()
        if valor not in (self.ESTADO_ACTIVO, self.ESTADO_INACTIVO):
            raise ClienteInvalidoError(
                f"Estado de cliente inválido: '{valor}'. Use ACTIVO o INACTIVO."
            )
        self._estado = valor

    # ---------------- Métodos de la entidad ----------------

    def validar(self):
        """Valida que todos los datos del cliente sean correctos."""
        self.nombre_completo = self._nombre_completo
        self.numero_identificacion = self._numero_identificacion
        self.correo_electronico = self._correo_electronico
        self.telefono = self._telefono
        return True

    def actualizar(self, **kwargs):
        """Actualiza los campos permitidos del cliente."""
        permitidos = {
            "nombre_completo": "nombre_completo",
            "numero_identificacion": "numero_identificacion",
            "correo_electronico": "correo_electronico",
            "telefono": "telefono",
            "estado": "estado",
        }
        for clave, valor in kwargs.items():
            if clave in permitidos:
                setattr(self, clave, valor)
            else:
                raise ParametroFaltanteError(
                    f"El campo '{clave}' no es actualizable en un cliente."
                )

    def to_dict(self):
        return {
            "identificador": self.identificador,
            "nombre_completo": self._nombre_completo,
            "numero_identificacion": self._numero_identificacion,
            "correo_electronico": self._correo_electronico,
            "telefono": self._telefono,
            "fecha_registro": self._fecha_registro.strftime("%Y-%m-%d %H:%M:%S"),
            "estado": self._estado,
            "fecha_creacion": self._fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def __str__(self):
        return (f"Cliente(id={self.identificador}, "
                f"nombre={self._nombre_completo}, "
                f"id={self._numero_identificacion}, "
                f"estado={self._estado})")
