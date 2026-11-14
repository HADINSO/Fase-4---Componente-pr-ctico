"""
Servicio AsesoriaEspecializada.

Gestiona asesorías especializadas con especialidad, profesional asignado,
duración y tarifa por hora. Sobrescribe los métodos abstractos de Servicio.
"""

from exceptions.excepciones_personalizadas import ServicioInvalidoError, CalculoCostoError
from utils.validaciones import validar_entero_positivo, validar_precio, validar_no_vacio
from models.servicio import Servicio


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría especializada."""

    def __init__(self, codigo, nombre, descripcion, precio_base,
                 especialidad, profesional_asignado, duracion, tarifa_por_hora,
                 disponible=True, estado="ACTIVO"):
        super().__init__(codigo, nombre, descripcion, precio_base, disponible, estado)
        self._especialidad = None
        self._profesional_asignado = None
        self._duracion = None
        self._tarifa_por_hora = None

        self.especialidad = especialidad
        self.profesional_asignado = profesional_asignado
        self.duracion = duracion
        self.tarifa_por_hora = tarifa_por_hora

    @property
    def especialidad(self):
        return self._especialidad

    @especialidad.setter
    def especialidad(self, valor):
        self._especialidad = validar_no_vacio(valor, "especialidad")

    @property
    def profesional_asignado(self):
        return self._profesional_asignado

    @profesional_asignado.setter
    def profesional_asignado(self, valor):
        self._profesional_asignado = validar_no_vacio(valor, "profesional asignado")

    @property
    def duracion(self):
        return self._duracion

    @duracion.setter
    def duracion(self, valor):
        self._duracion = validar_entero_positivo(valor, "duración")

    @property
    def tarifa_por_hora(self):
        return self._tarifa_por_hora

    @tarifa_por_hora.setter
    def tarifa_por_hora(self, valor):
        self._tarifa_por_hora = validar_precio(valor, "tarifa por hora")

    def validar(self):
        """Valida la integridad de los datos de la asesoría (implementa Entidad)."""
        return self.validar_parametros()

    def validar_parametros(self):
        if self.duracion <= 0:
            raise ServicioInvalidoError("La duración de la asesoría debe ser mayor a cero.")
        if self.tarifa_por_hora < 0:
            raise ServicioInvalidoError("La tarifa por hora no puede ser negativa.")
        return True

    def calcular_costo(self, cantidad=1, impuesto=0.0, descuento=0.0):
        """
        Variantes de cálculo de costo para AsesoriaEspecializada:
        1. Costo básico: tarifa_por_hora * duracion * cantidad
        2. Costo con impuesto
        3. Costo con descuento
        4. Costo con impuesto y descuento
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
                f"Error calculando costo de AsesoriaEspecializada: {exc}"
            ) from exc

    def describir_servicio(self):
        return (f"Asesoría especializada '{self.nombre}' - {self.especialidad}. "
                f"Profesional: {self.profesional_asignado}, {self.duracion} hora(s), "
                f"tarifa ${self.tarifa_por_hora}/hora.")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "especialidad": self._especialidad,
            "profesional_asignado": self._profesional_asignado,
            "duracion": self._duracion,
            "tarifa_por_hora": self._tarifa_por_hora,
        })
        return data
