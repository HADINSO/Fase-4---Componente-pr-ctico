"""
Servicio ClienteService.

Capa de gestión de clientes. Utiliza listas internas para almacenar las
entidades en memoria y aplica validaciones de duplicados y formato.
"""

import logging
from models.cliente import Cliente
from exceptions.excepciones_personalizadas import (
    ClienteInvalidoError,
    ClienteDuplicadoError,
    ParametroFaltanteError,
)
from utils.logger import (
    registrar_cliente,
    registrar_error_validacion,
    registrar_excepcion,
)

logger = logging.getLogger("software_fj")


class ClienteService:
    """Administra el ciclo de vida de los clientes en memoria."""

    def __init__(self):
        self._clientes = []

    def registrar_cliente(self, identificador, nombre_completo,
                          numero_identificacion, correo_electronico,
                          telefono, estado="ACTIVO"):
        """Registra un nuevo cliente. Lanza ClienteDuplicadoError si ya existe."""
        try:
            if self.buscar_por_identificacion(numero_identificacion) is not None:
                raise ClienteDuplicadoError(
                    f"Ya existe un cliente con identificación {numero_identificacion}."
                )
            cliente = Cliente(
                identificador=identificador,
                nombre_completo=nombre_completo,
                numero_identificacion=numero_identificacion,
                correo_electronico=correo_electronico,
                telefono=telefono,
                estado=estado,
            )
            cliente.validar()
            self._clientes.append(cliente)
            registrar_cliente(identificador, nombre_completo, "registrado")
            logger.info("Cliente registrado exitosamente: %s", identificador)
            return cliente
        except (ClienteDuplicadoError, ClienteInvalidoError, ParametroFaltanteError) as exc:
            registrar_error_validacion(str(exc))
            registrar_excepcion(exc)
            raise
        except Exception as exc:
            registrar_error_validacion(f"Error inesperado registrando cliente: {exc}")
            registrar_excepcion(exc)
            raise

    def buscar_por_identificacion(self, numero_identificacion):
        """Busca un cliente por su número de identificación."""
        for cliente in self._clientes:
            if cliente.numero_identificacion == numero_identificacion:
                return cliente
        return None

    def buscar_por_id(self, identificador):
        """Busca un cliente por su identificador interno."""
        for cliente in self._clientes:
            if cliente.identificador == identificador:
                return cliente
        return None

    def listar_clientes(self):
        """Devuelve la lista de clientes registrados."""
        return list(self._clientes)

    def actualizar_cliente(self, identificador, **kwargs):
        """Actualiza los campos de un cliente existente."""
        cliente = self.buscar_por_id(identificador)
        if cliente is None:
            raise ParametroFaltanteError(
                f"No se encontró un cliente con identificador {identificador}."
            )
        try:
            cliente.actualizar(**kwargs)
            logger.info("Cliente actualizado: %s", identificador)
            return cliente
        except (ClienteInvalidoError, ParametroFaltanteError) as exc:
            registrar_error_validacion(str(exc))
            registrar_excepcion(exc)
            raise
        except Exception as exc:
            registrar_error_validacion(f"Error inesperado actualizando cliente: {exc}")
            registrar_excepcion(exc)
            raise

    def eliminar_cliente(self, identificador):
        """Elimina un cliente de la lista interna."""
        cliente = self.buscar_por_id(identificador)
        if cliente is None:
            raise ParametroFaltanteError(
                f"No se encontró un cliente con identificador {identificador}."
            )
        self._clientes.remove(cliente)
        logger.info("Cliente eliminado: %s", identificador)
        return cliente

    def total_clientes(self):
        """Devuelve la cantidad de clientes registrados."""
        return len(self._clientes)
