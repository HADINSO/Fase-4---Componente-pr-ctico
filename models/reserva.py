"""
Modelo Reserva.

Integra cliente y servicio, gestiona el ciclo de vida de una reserva
(PENDIENTE, CONFIRMADA, CANCELADA, FINALIZADA) y aplica las reglas de negocio
que impiden operaciones inválidas sobre los estados.
"""

from datetime import datetime
from exceptions.excepciones_personalizadas import (
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ReservaNoEncontradaError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    CalculoCostoError,
)
from utils.validaciones import validar_entero_positivo, validar_no_vacio
from models.entidad import Entidad


class Reserva(Entidad):
    """Reserva de un servicio para un cliente."""

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    FINALIZADA = "FINALIZADA"

    ESTADOS_PERMITIDOS = (PENDIENTE, CONFIRMADA, CANCELADA, FINALIZADA)

    def __init__(self, id_reserva, cliente, servicio, fecha, duracion,
                 estado=PENDIENTE, costo=None):
        super().__init__(id_reserva)
        if cliente is None:
            raise ParametroFaltanteError("La reserva requiere un cliente.")
        if servicio is None:
            raise ParametroFaltanteError("La reserva requiere un servicio.")

        self._cliente = cliente
        self._servicio = servicio
        self._fecha = None
        self._duracion = None
        self._costo = None
        self._estado = None

        self.fecha = fecha
        self.duracion = duracion
        self.estado = estado
        self._costo = costo if costo is not None else self.calcular_costo()

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = validar_no_vacio(valor, "fecha de la reserva")

    @property
    def duracion(self):
        return self._duracion

    @duracion.setter
    def duracion(self, valor):
        valor_int = validar_entero_positivo(valor, "duración de la reserva", permitir_cero=False)
        self._duracion = valor_int

    @property
    def costo(self):
        return self._costo

    @costo.setter
    def costo(self, valor):
        self._costo = valor

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        valor = str(valor).upper().strip()
        if valor not in self.ESTADOS_PERMITIDOS:
            raise ReservaInvalidaError(
                f"Estado de reserva inválido: '{valor}'. "
                f"Estados permitidos: {', '.join(self.ESTADOS_PERMITIDOS)}."
            )
        self._estado = valor

    def validar(self):
        """Valida la integridad de la reserva (implementa Entidad)."""
        return self.validar_disponibilidad()

    # ---------------- Validación de disponibilidad ----------------

    def validar_disponibilidad(self):
        """Valida que el servicio exista, esté disponible y la reserva sea coherente."""
        if self._servicio is None:
            raise ReservaInvalidaError("No se puede validar: la reserva no tiene servicio asignado.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' no está disponible para reservar."
            )
        if self._duracion is None or self._duracion <= 0:
            raise ReservaInvalidaError("La duración de la reserva debe ser mayor a cero.")
        return True

    # ---------------- Operaciones del ciclo de vida ----------------

    def calcular_costo(self):
        """Calcula el costo usando el polimorfismo del servicio (costo básico)."""
        try:
            return self._servicio.calcular_costo(cantidad=1)
        except Exception as exc:
            raise CalculoCostoError(
                f"No se pudo calcular el costo de la reserva {self.identificador}"
            ) from exc

    def calcular_costo_con(self, cantidad=1, impuesto=0.0, descuento=0.0):
        """Calcula el costo delegando en la variante de argumentos del servicio."""
        try:
            return self._servicio.calcular_costo(
                cantidad=cantidad, impuesto=impuesto, descuento=descuento
            )
        except Exception as exc:
            raise CalculoCostoError(
                f"No se pudo calcular el costo de la reserva {self.identificador}"
            ) from exc

    def confirmar(self):
        """Confirma la reserva si está pendiente."""
        if self._estado == self.CANCELADA:
            raise OperacionNoPermitidaError(
                "No se puede confirmar una reserva cancelada."
            )
        if self._estado == self.FINALIZADA:
            raise OperacionNoPermitidaError(
                "No se puede confirmar una reserva finalizada."
            )
        self.validar_disponibilidad()
        self._estado = self.CONFIRMADA
        return True

    def cancelar(self):
        """Cancela la reserva si está pendiente o confirmada."""
        if self._estado == self.FINALIZADA:
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva finalizada."
            )
        if self._estado == self.CANCELADA:
            raise OperacionNoPermitidaError(
                "La reserva ya está cancelada."
            )
        self._estado = self.CANCELADA
        return True

    def finalizar(self):
        """Finaliza la reserva si está confirmada."""
        if self._estado != self.CONFIRMADA:
            raise OperacionNoPermitidaError(
                "Solo se pueden finalizar reservas confirmadas."
            )
        self._estado = self.FINALIZADA
        return True

    def procesar_reserva(self):
        """Procesa la reserva completa: valida, calcula costo y deja pendiente."""
        self.validar_disponibilidad()
        self._costo = self.calcular_costo_con()
        self._estado = self.PENDIENTE
        return self.to_dict()

    def consultar_detalles(self):
        """Devuelve un diccionario con los detalles completos de la reserva."""
        return {
            "id_reserva": self.identificador,
            "cliente": self._cliente.to_dict(),
            "servicio": self._servicio.to_dict(),
            "fecha": self._fecha,
            "duracion": self._duracion,
            "costo": self._costo,
            "estado": self._estado,
            "fecha_creacion": self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def to_dict(self):
        return {
            "id_reserva": self.identificador,
            "cliente_id": self._cliente.identificador,
            "cliente_nombre": self._cliente.nombre_completo,
            "servicio_codigo": self._servicio.identificador,
            "servicio_nombre": self._servicio.nombre,
            "tipo_servicio": self._servicio.__class__.__name__,
            "fecha": self._fecha,
            "duracion": self._duracion,
            "costo": self._costo,
            "estado": self._estado,
            "fecha_creacion": self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def __str__(self):
        return (f"Reserva(id={self.identificador}, cliente={self._cliente.identificador}, "
                f"servicio={self._servicio.identificador}, estado={self._estado}, "
                f"costo={self._costo})")
