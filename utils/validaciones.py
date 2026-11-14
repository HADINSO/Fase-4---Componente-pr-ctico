"""
Funciones de validación reutilizables para el sistema SOFTWARE FJ.

Centralizan la comprobación de formatos obligatorios: correo electrónico,
número de identificación, teléfono, precios y cadenas no vacías.
"""

import re
from exceptions.excepciones_personalizadas import (
    ClienteInvalidoError,
    ParametroFaltanteError,
    ServicioInvalidoError,
)


def validar_no_vacio(valor, nombre_campo):
    """Valida que un valor de cadena no esté vacío ni sea None."""
    if valor is None or str(valor).strip() == "":
        raise ParametroFaltanteError(f"El campo '{nombre_campo}' es obligatorio y no puede estar vacío")
    return str(valor).strip()


def validar_correo_electronico(correo):
    """Valida el formato de una dirección de correo electrónico."""
    validar_no_vacio(correo, "correo electrónico")
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(patron, str(correo).strip()):
        raise ClienteInvalidoError(
            f"Formato de correo electrónico inválido: '{correo}'"
        )
    return str(correo).strip()


def validar_identificacion(identificacion):
    """Valida que la identificación sea alfanumérica y no vacía."""
    validar_no_vacio(identificacion, "identificación")
    identificacion = str(identificacion).strip()
    if not re.match(r"^[A-Za-z0-9]+$", identificacion):
        raise ClienteInvalidoError(
            f"Identificación inválida: '{identificacion}'. Solo se permiten letras y números."
        )
    if len(identificacion) < 5:
        raise ClienteInvalidoError(
            f"Identificación demasiado corta: '{identificacion}'. Mínimo 5 caracteres."
        )
    return identificacion


def validar_telefono(telefono):
    """Valida que el teléfono contenga solo dígitos y tenga longitud razonable."""
    validar_no_vacio(telefono, "teléfono")
    telefono = str(telefono).strip()
    if not re.match(r"^[0-9]{7,15}$", telefono):
        raise ClienteInvalidoError(
            f"Número telefónico inválido: '{telefono}'. Debe tener entre 7 y 15 dígitos."
        )
    return telefono


def validar_nombre(nombre):
    """Valida que el nombre no esté vacío y contenga caracteres razonables."""
    validar_no_vacio(nombre, "nombre")
    nombre = str(nombre).strip()
    if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", nombre):
        raise ClienteInvalidoError(
            f"Nombre inválido: '{nombre}'. Solo se permiten letras y espacios."
        )
    if len(nombre) < 3:
        raise ClienteInvalidoError(
            f"Nombre demasiado corto: '{nombre}'. Mínimo 3 caracteres."
        )
    return nombre


def validar_precio(precio, nombre_campo="precio"):
    """Valida que un precio sea un número mayor o igual a cero."""
    try:
        valor = float(precio)
    except (TypeError, ValueError):
        raise ServicioInvalidoError(
            f"El {nombre_campo} debe ser un número válido."
        )
    if valor < 0:
        raise ServicioInvalidoError(
            f"El {nombre_campo} no puede ser negativo: {valor}"
        )
    return valor


def validar_entero_positivo(valor, nombre_campo="valor", permitir_cero=False):
    """Valida que un valor sea un número entero positivo (o no negativo si se permite)."""
    try:
        valor_int = int(valor)
    except (TypeError, ValueError):
        raise ParametroFaltanteError(
            f"El campo '{nombre_campo}' debe ser un número entero."
        )
    if permitir_cero:
        if valor_int < 0:
            raise ParametroFaltanteError(
                f"El campo '{nombre_campo}' no puede ser negativo."
            )
    else:
        if valor_int <= 0:
            raise ParametroFaltanteError(
                f"El campo '{nombre_campo}' debe ser mayor a cero."
            )
    return valor_int


def validar_cadena_no_vacia(valor, nombre_campo):
    """Valida que un valor sea una cadena no vacía."""
    return validar_no_vacio(valor, nombre_campo)
