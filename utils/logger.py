"""
Sistema de registro de eventos y errores (logs) de SOFTWARE FJ.

Utiliza el módulo logging de Python con rotación de archivos para evitar
que el registro crezca indefinidamente. El único archivo de persistencia
operativa es logs/software_fj.log.
"""

import logging
import logging.handlers
import os
from datetime import datetime

# Directorio y archivo de logs
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
LOG_FILE = os.path.join(LOGS_DIR, "software_fj.log")

# Configuración de rotación: máximo 5 MB por archivo, conserva 3 respaldos
MAX_BYTES = 5 * 1024 * 1024
BACKUP_COUNT = 3

_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"

_logger = None


def configurar_logger(nivel=logging.DEBUG):
    """Configura y devuelve el logger singleton del sistema."""
    global _logger
    if _logger is not None:
        return _logger

    os.makedirs(LOGS_DIR, exist_ok=True)

    logger = logging.getLogger("software_fj")
    logger.setLevel(nivel)
    logger.propagate = False

    if not logger.handlers:
        # Handler con rotación de archivo
        handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
            encoding="utf-8",
        )
        handler.setLevel(nivel)
        formatter = logging.Formatter(_FORMAT, datefmt=_DATEFMT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Handler de consola para eventos importantes durante ejecución interactiva
        consola = logging.StreamHandler()
        consola.setLevel(logging.INFO)
        consola.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(consola)

    _logger = logger
    return _logger


def obtener_logger():
    """Devuelve el logger configurado, inicializándolo si es necesario."""
    if _logger is None:
        return configurar_logger()
    return _logger


def registrar_evento(mensaje, nivel="INFO"):
    """Registra un evento genérico en el archivo de log."""
    logger = obtener_logger()
    nivel_log = getattr(logging, nivel.upper(), logging.INFO)
    logger.log(nivel_log, mensaje)


def registrar_inicio_sistema():
    registrar_evento("=== INICIO DEL SISTEMA SOFTWARE FJ ===", "INFO")


def registrar_finalizacion_sistema():
    registrar_evento("=== FINALIZACIÓN DEL SISTEMA SOFTWARE FJ ===", "INFO")


def registrar_cliente(identificador, nombre, accion="registro"):
    registrar_evento(
        f"Cliente {accion}: id={identificador}, nombre={nombre}", "INFO"
    )


def registrar_servicio(codigo, nombre, accion="creación"):
    registrar_evento(
        f"Servicio {accion}: codigo={codigo}, nombre={nombre}", "INFO"
    )


def registrar_reserva(id_reserva, cliente_id, servicio_codigo, accion="creación"):
    registrar_evento(
        f"Reserva {accion}: id={id_reserva}, cliente={cliente_id}, servicio={servicio_codigo}", "INFO"
    )


def registrar_confirmacion_reserva(id_reserva):
    registrar_evento(f"Reserva confirmada: id={id_reserva}", "INFO")


def registrar_cancelacion_reserva(id_reserva):
    registrar_evento(f"Reserva cancelada: id={id_reserva}", "INFO")


def registrar_advertencia(mensaje):
    registrar_evento(mensaje, "WARNING")


def registrar_error_validacion(mensaje):
    registrar_evento(mensaje, "ERROR")


def registrar_excepcion(excepcion, causa_original=None):
    """Registra una excepción personalizada, incluida su causa encadenada."""
    mensaje = f"Excepción: {type(excepcion).__name__} - {excepcion}"
    if causa_original is not None:
        mensaje += f" | Causa original: {type(causa_original).__name__} - {causa_original}"
    registrar_evento(mensaje, "ERROR")


def registrar_error_inesperado(mensaje):
    registrar_evento(mensaje, "CRITICAL")
