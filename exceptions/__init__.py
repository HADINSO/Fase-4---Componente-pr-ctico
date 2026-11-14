"""Paquete de excepciones personalizadas del sistema SOFTWARE FJ."""

from .excepciones_personalizadas import (
    SoftwareFJError,
    ClienteInvalidoError,
    ClienteDuplicadoError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    ReservaNoEncontradaError,
    OperacionNoPermitidaError,
    CalculoCostoError,
    ParametroFaltanteError,
)

__all__ = [
    "SoftwareFJError",
    "ClienteInvalidoError",
    "ClienteDuplicadoError",
    "ServicioInvalidoError",
    "ServicioNoDisponibleError",
    "ReservaInvalidaError",
    "ReservaNoEncontradaError",
    "OperacionNoPermitidaError",
    "CalculoCostoError",
    "ParametroFaltanteError",
]
