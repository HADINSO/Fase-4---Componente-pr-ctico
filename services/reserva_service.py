"""
Servicio ReservaService.

Capa de gestión de reservas. Permite registrar, consultar, listar, confirmar,
cancelar y finalizar reservas, validando disponibilidad y evitando conflictos.
"""

import logging
from models.reserva import Reserva
from exceptions.excepciones_personalizadas import (
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ReservaNoEncontradaError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    CalculoCostoError,
)
from utils.logger import (
    registrar_reserva,
    registrar_confirmacion_reserva,
    registrar_cancelacion_reserva,
    registrar_error_validacion,
    registrar_excepcion,
)

logger = logging.getLogger("software_fj")


class ReservaService:
    """Administra el ciclo de vida de las reservas en memoria."""

    def __init__(self):
        self._reservas = []

    def registrar_reserva(self, id_reserva, cliente, servicio, fecha, duracion,
                          estado="PENDIENTE"):
        """Registra una nueva reserva validando cliente, servicio y disponibilidad."""
        try:
            if cliente is None:
                raise ParametroFaltanteError("La reserva requiere un cliente válido.")
            if servicio is None:
                raise ParametroFaltanteError("La reserva requiere un servicio válido.")

            if self.buscar_por_id(id_reserva) is not None:
                raise ReservaInvalidaError(
                    f"Ya existe una reserva con el identificador {id_reserva}."
                )

            reserva = Reserva(
                id_reserva=id_reserva,
                cliente=cliente,
                servicio=servicio,
                fecha=fecha,
                duracion=duracion,
                estado=estado,
            )
            reserva.validar_disponibilidad()
            reserva.procesar_reserva()
            self._reservas.append(reserva)
            registrar_reserva(
                id_reserva, cliente.identificador, servicio.identificador, "registrada"
            )
            logger.info("Reserva registrada: %s", id_reserva)
            return reserva
        except (
            ReservaInvalidaError,
            OperacionNoPermitidaError,
            ParametroFaltanteError,
            ServicioNoDisponibleError,
        ) as exc:
            registrar_error_validacion(str(exc))
            registrar_excepcion(exc)
            raise
        except Exception as exc:
            registrar_error_validacion(f"Error inesperado registrando reserva: {exc}")
            registrar_excepcion(exc)
            raise

    def buscar_por_id(self, id_reserva):
        """Busca una reserva por su identificador."""
        for reserva in self._reservas:
            if reserva.identificador == id_reserva:
                return reserva
        return None

    def listar_reservas(self):
        """Devuelve la lista de reservas registradas."""
        return list(self._reservas)

    def confirmar_reserva(self, id_reserva):
        """Confirma una reserva si está pendiente."""
        reserva = self._obtener_o_error(id_reserva)
        try:
            reserva.confirmar()
            registrar_confirmacion_reserva(id_reserva)
            logger.info("Reserva confirmada: %s", id_reserva)
            return reserva
        except OperacionNoPermitidaError as exc:
            registrar_error_validacion(str(exc))
            registrar_excepcion(exc)
            raise
        except Exception as exc:
            registrar_error_validacion(f"Error confirmando reserva: {exc}")
            registrar_excepcion(exc)
            raise

    def cancelar_reserva(self, id_reserva):
        """Cancela una reserva si está pendiente o confirmada."""
        reserva = self._obtener_o_error(id_reserva)
        try:
            reserva.cancelar()
            registrar_cancelacion_reserva(id_reserva)
            logger.info("Reserva cancelada: %s", id_reserva)
            return reserva
        except OperacionNoPermitidaError as exc:
            registrar_error_validacion(str(exc))
            registrar_excepcion(exc)
            raise
        except Exception as exc:
            registrar_error_validacion(f"Error cancelando reserva: {exc}")
            registrar_excepcion(exc)
            raise

    def finalizar_reserva(self, id_reserva):
        """Finaliza una reserva si está confirmada."""
        reserva = self._obtener_o_error(id_reserva)
        try:
            reserva.finalizar()
            logger.info("Reserva finalizada: %s", id_reserva)
            return reserva
        except OperacionNoPermitidaError as exc:
            registrar_error_validacion(str(exc))
            registrar_excepcion(exc)
            raise
        except Exception as exc:
            registrar_error_validacion(f"Error finalizando reserva: {exc}")
            registrar_excepcion(exc)
            raise

    def consultar_reserva(self, id_reserva):
        """Devuelve los detalles de una reserva."""
        return self._obtener_o_error(id_reserva)

    def _obtener_o_error(self, id_reserva):
        reserva = self.buscar_por_id(id_reserva)
        if reserva is None:
            raise ReservaNoEncontradaError(
                f"No se encontró una reserva con identificador {id_reserva}."
            )
        return reserva

    def total_reservas(self):
        """Devuelve la cantidad de reservas registradas."""
        return len(self._reservas)

    def reservas_por_estado(self, estado):
        """Devuelve las reservas filtradas por estado."""
        return [r for r in self._reservas if r.estado == estado.upper()]
