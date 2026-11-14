"""
Servicio ReservaSala.

Gestiona reservas de salas con capacidad, ubicación, duración, equipamiento
y tarifa por hora. Sobrescribe los métodos abstractos de Servicio.
"""

from exceptions.excepciones_personalizadas import ServicioInvalidoError, CalculoCostoError
from utils.validaciones import validar_entero_positivo, validar_precio, validar_no_vacio
from models.servicio import Servicio


class ReservaSala(Servicio):
    """Servicio de reserva de salas."""

    def __init__(self, codigo, nombre, descripcion, precio_base,
                 capacidad, ubicacion, duracion, equipamiento, tarifa_por_hora,
                 disponible=True, estado="ACTIVO"):
        super().__init__(codigo, nombre, descripcion, precio_base, disponible, estado)
        self._capacidad = None
        self._ubicacion = None
        self._duracion = None
        self._equipamiento = None
        self._tarifa_por_hora = None

        self.capacidad = capacidad
        self.ubicacion = ubicacion
        self.duracion = duracion
        self.equipamiento = equipamiento
        self.tarifa_por_hora = tarifa_por_hora

    @property
    def capacidad(self):
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor):
        self._capacidad = validar_entero_positivo(valor, "capacidad")

    @property
    def ubicacion(self):
        return self._ubicacion

    @ubicacion.setter
    def ubicacion(self, valor):
        self._ubicacion = validar_no_vacio(valor, "ubicación")

    @property
    def duracion(self):
        return self._duracion

    @duracion.setter
    def duracion(self, valor):
        self._duracion = validar_entero_positivo(valor, "duración")

    @property
    def equipamiento(self):
        return self._equipamiento

    @equipamiento.setter
    def equipamiento(self, valor):
        self._equipamiento = validar_no_vacio(valor, "equipamiento")

    @property
    def tarifa_por_hora(self):
        return self._tarifa_por_hora

    @tarifa_por_hora.setter
    def tarifa_por_hora(self, valor):
        self._tarifa_por_hora = validar_precio(valor, "tarifa por hora")

    def validar(self):
        """Valida la integridad de los datos de la sala (implementa Entidad)."""
        return self.validar_parametros()

    def validar_parametros(self):
        if self.capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser mayor a cero.")
        if self.tarifa_por_hora < 0:
            raise ServicioInvalidoError("La tarifa por hora no puede ser negativa.")
        return True

    def calcular_costo(self, cantidad=1, impuesto=0.0, descuento=0.0):
        """
        Variantes de cálculo de costo para ReservaSala:
        1. Costo básico: tarifa_por_hora * duracion * cantidad
        2. Costo con impuesto: aplica impuesto sobre el subtotal
        3. Costo con descuento: aplica descuento sobre el subtotal
        4. Costo con impuesto y descuento: ambos
        """
        try:
            self.validar_parametros()
            subtotal = self.tarifa_por_hora * self.duracion * cantidad

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
                f"Error calculando costo de ReservaSala: {exc}"
            ) from exc

    def describir_servicio(self):
        return (f"Reserva de sala '{self.nombre}' en {self.ubicacion}, "
                f"capacidad {self.capacidad} personas, {self.duracion} hora(s), "
                f"equipamiento: {self.equipamiento}, tarifa ${self.tarifa_por_hora}/hora.")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "capacidad": self._capacidad,
            "ubicacion": self._ubicacion,
            "duracion": self._duracion,
            "equipamiento": self._equipamiento,
            "tarifa_por_hora": self._tarifa_por_hora,
        })
        return data
