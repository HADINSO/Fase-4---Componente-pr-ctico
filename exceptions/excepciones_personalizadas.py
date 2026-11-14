"""
Excepciones personalizadas del sistema SOFTWARE FJ.

Todas heredan de la clase base SoftwareFJError para permitir una captura
específica y controlada en las capas de servicio y de interfaz.
"""


class SoftwareFJError(Exception):
    """Excepción base de todas las excepciones del sistema SOFTWARE FJ."""

    def __init__(self, mensaje="Ocurrió un error en el sistema SOFTWARE FJ"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no pasan las validaciones."""

    def __init__(self, mensaje="Cliente inválido: los datos proporcionados no son correctos"):
        super().__init__(mensaje)


class ClienteDuplicadoError(SoftwareFJError):
    """Se intenta registrar un cliente con identificación ya existente."""

    def __init__(self, mensaje="Cliente duplicado: ya existe un cliente con esa identificación"):
        super().__init__(mensaje)


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un servicio no son válidos."""

    def __init__(self, mensaje="Servicio inválido: los datos proporcionados no son correctos"):
        super().__init__(mensaje)


class ServicioNoDisponibleError(SoftwareFJError):
    """Se intenta usar un servicio que no está disponible."""

    def __init__(self, mensaje="Servicio no disponible: el servicio solicitado no puede reservarse"):
        super().__init__(mensaje)


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no cumple las reglas de negocio."""

    def __init__(self, mensaje="Reserva inválida: no se puede realizar la operación solicitada"):
        super().__init__(mensaje)


class ReservaNoEncontradaError(SoftwareFJError):
    """Se busca una reserva que no existe en el sistema."""

    def __init__(self, mensaje="Reserva no encontrada: no existe una reserva con el identificador dado"):
        super().__init__(mensaje)


class OperacionNoPermitidaError(SoftwareFJError):
    """Se intenta una operación no permitida sobre una reserva en cierto estado."""

    def __init__(self, mensaje="Operación no permitida: el estado de la reserva no lo autoriza"):
        super().__init__(mensaje)


class CalculoCostoError(SoftwareFJError):
    """Error al calcular el costo de un servicio o reserva."""

    def __init__(self, mensaje="Error de cálculo de costo: parámetros incorrectos"):
        super().__init__(mensaje)


class ParametroFaltanteError(SoftwareFJError):
    """Falta un parámetro obligatorio para ejecutar una operación."""

    def __init__(self, mensaje="Parámetro faltante: se requiere un valor obligatorio que no fue proporcionado"):
        super().__init__(mensaje)
