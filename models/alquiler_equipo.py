"""
Servicio AlquilerEquipo.

Gestiona alquiler de equipos con nombre, cantidad disponible, precio por día
y condiciones de alquiler. Sobrescribe los métodos abstractos de Servicio.
"""

from exceptions.excepciones_personalizadas import ServicioInvalidoError, CalculoCostoError
from utils.validaciones import validar_entero_positivo, validar_precio, validar_no_vacio
from models.servicio import Servicio


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos."""

    def __init__(self, codigo, nombre, descripcion, precio_base,
                 nombre_equipo, cantidad_disponible, precio_por_dia,
                 condiciones_alquiler, disponible=True, estado="ACTIVO"):
        super().__init__(codigo, nombre, descripcion, precio_base, disponible, estado)
        self._nombre_equipo = None
        self._cantidad_disponible = None
        self._precio_por_dia = None
        self._condiciones_alquiler = None

        self.nombre_equipo = nombre_equipo
        self.cantidad_disponible = cantidad_disponible
        self.precio_por_dia = precio_por_dia
        self.condiciones_alquiler = condiciones_alquiler

    @property
    def nombre_equipo(self):
        return self._nombre_equipo

    @nombre_equipo.setter
    def nombre_equipo(self, valor):
        self._nombre_equipo = validar_no_vacio(valor, "nombre del equipo")

    @property
    def cantidad_disponible(self):
        return self._cantidad_disponible

    @cantidad_disponible.setter
    def cantidad_disponible(self, valor):
        self._cantidad_disponible = validar_entero_positivo(
            valor, "cantidad disponible", permitir_cero=True
        )

    @property
    def precio_por_dia(self):
        return self._precio_por_dia

    @precio_por_dia.setter
    def precio_por_dia(self, valor):
        self._precio_por_dia = validar_precio(valor, "precio por día")

    @property
    def condiciones_alquiler(self):
        return self._condiciones_alquiler

    @condiciones_alquiler.setter
    def condiciones_alquiler(self, valor):
        self._condiciones_alquiler = validar_no_vacio(valor, "condiciones de alquiler")

    def validar(self):
        """Valida la integridad de los datos del alquiler (implementa Entidad)."""
        return self.validar_parametros()

    def validar_parametros(self):
        if self.cantidad_disponible < 0:
            raise ServicioInvalidoError("La cantidad disponible no puede ser negativa.")
        if self.precio_por_dia < 0:
            raise ServicioInvalidoError("El precio por día no puede ser negativo.")
        return True

    def calcular_costo(self, cantidad=1, impuesto=0.0, descuento=0.0):
        """
        Variantes de cálculo de costo para AlquilerEquipo:
        1. Costo básico: precio_por_dia * cantidad
        2. Costo con impuesto
        3. Costo con descuento
        4. Costo con impuesto y descuento
        """
        try:
            self.validar_parametros()
            if self.cantidad_disponible < cantidad:
                raise CalculoCostoError(
                    f"No hay suficientes equipos disponibles: {self.cantidad_disponible} < {cantidad}"
                )
            subtotal = self.precio_por_dia * cantidad

            if descuento and descuento > 0:
                if descuento > 100:
                    raise CalculoCostoError("El descuento no puede exceder el 100%.")
                subtotal = subtotal * (1 - descuento / 100.0)

            if impuesto and impuesto > 0:
                subtotal = subtotal * (1 + impuesto / 100.0)

            return round(subtotal, 2)
        except CalculoCostoError:
            raise
        except Exception as exc:
            raise CalculoCostoError(
                f"Error calculando costo de AlquilerEquipo: {exc}"
            ) from exc

    def describir_servicio(self):
        return (f"Alquiler de equipo '{self.nombre_equipo}' - {self.nombre}. "
                f"Disponibles: {self.cantidad_disponible}, precio ${self.precio_por_dia}/día. "
                f"Condiciones: {self.condiciones_alquiler}.")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "nombre_equipo": self._nombre_equipo,
            "cantidad_disponible": self._cantidad_disponible,
            "precio_por_dia": self._precio_por_dia,
            "condiciones_alquiler": self._condiciones_alquiler,
        })
        return data
