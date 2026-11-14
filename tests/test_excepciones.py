"""
Pruebas automatizadas de excepciones personalizadas y manejo avanzado.

Cubre:
- Jerarquía de excepciones personalizadas.
- try/except, try/except/else, try/except/finally.
- Encadenamiento de excepciones (raise ... from).
- Capturas múltiples y captura general de seguridad.
- Continuidad del programa ante errores.
- Registro de logs.
"""

import unittest
import logging
import os
import tempfile

from exceptions.excepciones_personalizadas import (
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
from utils.logger import (
    configurar_logger,
    registrar_evento,
    registrar_error_validacion,
    registrar_excepcion,
    LOGS_DIR,
    LOG_FILE,
)


class TestJerarquiaExcepciones(unittest.TestCase):
    """Todas las excepciones heredan de SoftwareFJError."""

    def test_software_fj_error_es_exception(self):
        self.assertTrue(issubclass(SoftwareFJError, Exception))

    def test_todas_heredan_de_software_fj_error(self):
        excepciones = [
            ClienteInvalidoError, ClienteDuplicadoError,
            ServicioInvalidoError, ServicioNoDisponibleError,
            ReservaInvalidaError, ReservaNoEncontradaError,
            OperacionNoPermitidaError, CalculoCostoError,
            ParametroFaltanteError,
        ]
        for exc in excepciones:
            self.assertTrue(issubclass(exc, SoftwareFJError))

    def test_mensajes_claros(self):
        exc = ClienteInvalidoError("Correo inválido")
        self.assertEqual(str(exc), "Correo inválido")

    def test_captura_por_tipo_especifico(self):
        try:
            raise ClienteDuplicadoError("Duplicado")
        except ClienteDuplicadoError as exc:
            self.assertIsInstance(exc, SoftwareFJError)

    def test_captura_general_de_seguridad(self):
        capturado = None
        try:
            raise CalculoCostoError("Costo inválido")
        except (ClienteInvalidoError, ParametroFaltanteError):
            capturado = "especifico"
        except SoftwareFJError as exc:
            capturado = exc
        self.assertIsInstance(capturado, CalculoCostoError)


class TestEstructurasManejoErrores(unittest.TestCase):
    """try/except, try/except/else y try/except/finally."""

    def test_try_except_else(self):
        ejecutado_else = False
        try:
            resultado = 10 / 2
        except ZeroDivisionError:
            resultado = 0
        else:
            ejecutado_else = True
        self.assertTrue(ejecutado_else)
        self.assertEqual(resultado, 5.0)

    def test_try_except_else_no_ejecuta_si_hay_excepcion(self):
        ejecutado_else = False
        try:
            resultado = 10 / 0
        except ZeroDivisionError:
            resultado = 0
        else:
            ejecutado_else = True
        self.assertFalse(ejecutado_else)
        self.assertEqual(resultado, 0)

    def test_try_except_finally(self):
        finally_ejecutado = False
        try:
            raise ValueError("error de prueba")
        except ValueError:
            pass
        finally:
            finally_ejecutado = True
        self.assertTrue(finally_ejecutado)

    def test_try_except_finally_siempre_ejecuta(self):
        ejecutado = []
        try:
            raise RuntimeError("error")
        except RuntimeError:
            ejecutado.append("except")
        finally:
            ejecutado.append("finally")
        self.assertEqual(ejecutado, ["except", "finally"])


class TestEncadenamientoExcepciones(unittest.TestCase):
    """raise ... from conserva la causa original."""

    def test_excepcion_encadenada_conserva_causa(self):
        try:
            try:
                raise ParametroFaltanteError("servicio no encontrado")
            except ParametroFaltanteError as causa:
                raise CalculoCostoError("no se pudo calcular") from causa
        except CalculoCostoError as exc:
            self.assertIsNotNone(exc.__cause__)
            self.assertIsInstance(exc.__cause__, ParametroFaltanteError)
            self.assertEqual(str(exc.__cause__), "servicio no encontrado")

    def test_excepcion_encadenada_mensaje_combinado(self):
        try:
            try:
                raise ServicioInvalidoError("precio negativo")
            except ServicioInvalidoError as causa:
                raise ReservaInvalidaError("reserva inválida") from causa
        except ReservaInvalidaError as exc:
            self.assertIsInstance(exc.__cause__, ServicioInvalidoError)


class TestContinuidadPrograma(unittest.TestCase):
    """Un error no debe detener el procesamiento de operaciones independientes."""

    def test_continuidad_despues_de_error(self):
        resultados = []
        # Operación que falla
        try:
            raise ClienteInvalidoError("datos inválidos")
        except ClienteInvalidoError:
            resultados.append("error manejado")
        # Operación independiente que continúa
        try:
            resultados.append("operación exitosa")
        except Exception:
            resultados.append("error inesperado")
        self.assertEqual(resultados, ["error manejado", "operación exitosa"])

    def test_varias_operaciones_independientes(self):
        contador = [0]
        fallidas = 0

        def incrementar():
            contador[0] += 1

        operaciones = [
            lambda: (_ for _ in ()).throw(ClienteInvalidoError("falla 1")),
            incrementar,
            lambda: (_ for _ in ()).throw(ServicioInvalidoError("falla 2")),
            incrementar,
        ]
        for operacion in operaciones:
            try:
                operacion()
            except (ClienteInvalidoError, ServicioInvalidoError):
                fallidas += 1
        self.assertEqual(contador[0], 2)
        self.assertEqual(fallidas, 2)


class TestRegistroLogs(unittest.TestCase):
    """El sistema de logs registra eventos y errores."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.log_path = os.path.join(self.tmpdir, "software_fj.log")
        self.logger = logging.getLogger("software_fj_test")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        handler = logging.FileHandler(self.log_path, encoding="utf-8")
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        )
        self.logger.addHandler(handler)

    def test_registra_evento_info(self):
        self.logger.info("Evento de prueba INFO")
        with open(self.log_path, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        self.assertIn("Evento de prueba INFO", contenido)
        self.assertIn("INFO", contenido)

    def test_registra_evento_error(self):
        self.logger.error("Error de validación de prueba")
        with open(self.log_path, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        self.assertIn("Error de validación de prueba", contenido)
        self.assertIn("ERROR", contenido)

    def test_niveles_log(self):
        self.logger.debug("mensaje debug")
        self.logger.warning("mensaje advertencia")
        self.logger.critical("mensaje crítico")
        with open(self.log_path, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        self.assertIn("DEBUG", contenido)
        self.assertIn("WARNING", contenido)
        self.assertIn("CRITICAL", contenido)


if __name__ == "__main__":
    unittest.main()
