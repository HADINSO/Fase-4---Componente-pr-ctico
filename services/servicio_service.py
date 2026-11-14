"""
Servicio ServicioService.

Capa de gestión de servicios. Permite registrar, consultar, listar, cambiar
disponibilidad y calcular costos mediante polimorfismo sobre referencias
de tipo Servicio.
"""

import logging
from models.servicio import Servicio
from models.reserva_sala import ReservaSala
from models.alquiler_equipo import AlquilerEquipo
from models.asesoria import AsesoriaEspecializada
from exceptions.excepciones_personalizadas import (
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    ParametroFaltanteError,
    CalculoCostoError,
)
from utils.logger import (
    registrar_servicio,
    registrar_error_validacion,
    registrar_excepcion,
)

logger = logging.getLogger("software_fj")


class ServicioService:
    """Administra el catálogo de servicios de SOFTWARE FJ."""

    TIPOS_SERVICIO = {
        "sala": ReservaSala,
        "equipo": AlquilerEquipo,
        "asesoria": AsesoriaEspecializada,
    }

    def __init__(self):
        self._servicios = []

    def registrar_servicio(self, tipo, codigo, nombre, descripcion, precio_base,
                           disponible=True, estado="ACTIVO", **kwargs):
        """Registra un servicio especializado según el tipo indicado."""
        try:
            tipo_clave = str(tipo).lower().strip()
            if tipo_clave not in self.TIPOS_SERVICIO:
                raise ServicioInvalidoError(
                    f"Tipo de servicio inválido: '{tipo}'. "
                    f"Tipos permitidos: {', '.join(self.TIPOS_SERVICIO.keys())}."
                )
            if self.buscar_por_codigo(codigo) is not None:
                raise ServicioInvalidoError(
                    f"Ya existe un servicio con código {codigo}."
                )

            clase = self.TIPOS_SERVICIO[tipo_clave]
            servicio = clase(
                codigo=codigo,
                nombre=nombre,
                descripcion=descripcion,
                precio_base=precio_base,
                disponible=disponible,
                estado=estado,
                **kwargs,
            )
            servicio.validar_parametros()
            self._servicios.append(servicio)
            registrar_servicio(codigo, nombre, "registrado")
            logger.info("Servicio registrado: %s (%s)", codigo, tipo_clave)
            return servicio
        except (ServicioInvalidoError, ParametroFaltanteError) as exc:
            registrar_error_validacion(str(exc))
            registrar_excepcion(exc)
            raise
        except Exception as exc:
            registrar_error_validacion(f"Error inesperado registrando servicio: {exc}")
            registrar_excepcion(exc)
            raise

    def buscar_por_codigo(self, codigo):
        """Busca un servicio por su código."""
        for servicio in self._servicios:
            if servicio.identificador == codigo:
                return servicio
        return None

    def listar_servicios(self):
        """Devuelve la lista de servicios registrados."""
        return list(self._servicios)

    def cambiar_disponibilidad(self, codigo, disponible):
        """Cambia el estado de disponibilidad de un servicio."""
        servicio = self.buscar_por_codigo(codigo)
        if servicio is None:
            raise ParametroFaltanteError(
                f"No se encontró un servicio con código {codigo}."
            )
        servicio.disponible = bool(disponible)
        logger.info(
            "Disponibilidad cambiada: %s -> disponible=%s", codigo, disponible
        )
        return servicio

    def consultar_servicio(self, codigo):
        """Devuelve los detalles de un servicio."""
        servicio = self.buscar_por_codigo(codigo)
        if servicio is None:
            raise ParametroFaltanteError(
                f"No se encontró un servicio con código {codigo}."
            )
        return servicio

    def calcular_costo(self, servicio_codigo, cantidad=1, impuesto=0.0, descuento=0.0):
        """
        Calcula el costo de un servicio mediante polimorfismo.
        Admite variantes: básico, con impuesto, con descuento, ambos.
        """
        servicio = self.buscar_por_codigo(servicio_codigo)
        if servicio is None:
            raise ParametroFaltanteError(
                f"No se encontró un servicio con código {servicio_codigo}."
            )
        try:
            costo = servicio.calcular_costo(
                cantidad=cantidad, impuesto=impuesto, descuento=descuento
            )
            logger.info(
                "Costo calculado: servicio=%s cantidad=%s impuesto=%s descuento=%s -> %s",
                servicio_codigo, cantidad, impuesto, descuento, costo,
            )
            return costo
        except CalculoCostoError as exc:
            registrar_error_validacion(str(exc))
            registrar_excepcion(exc)
            raise
        except Exception as exc:
            registrar_error_validacion(f"Error calculando costo: {exc}")
            registrar_excepcion(exc)
            raise CalculoCostoError(
                f"No se pudo calcular el costo del servicio {servicio_codigo}"
            ) from exc

    def total_servicios(self):
        """Devuelve la cantidad de servicios registrados."""
        return len(self._servicios)
