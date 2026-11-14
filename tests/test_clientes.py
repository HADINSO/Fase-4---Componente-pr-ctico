"""
Pruebas automatizadas del módulo de clientes.

Cubre:
- Instanciación de la clase abstracta Entidad (no debe permitirla).
- Validaciones de clientes (campos obligatorios, correo, identificación,
  teléfono).
- Clientes duplicados.
- Encapsulamiento mediante propiedades.
"""

import unittest
from unittest.mock import patch

from models.entidad import Entidad
from models.cliente import Cliente
from services.cliente_service import ClienteService
from exceptions.excepciones_personalizadas import (
    ClienteInvalidoError,
    ClienteDuplicadoError,
    ParametroFaltanteError,
    CalculoCostoError,
)


class TestEntidadAbstracta(unittest.TestCase):
    """La clase Entidad es abstracta y no debe poder instanciarse directamente."""

    def test_entidad_no_se_puede_instanciar(self):
        with self.assertRaises(TypeError):
            Entidad(identificador="ID-001")


class TestClienteValidaciones(unittest.TestCase):
    """Validaciones de datos del cliente."""

    def test_cliente_valido(self):
        cliente = Cliente(
            identificador="CLI-001",
            nombre_completo="Juan Pérez",
            numero_identificacion="12345678",
            correo_electronico="juan@correo.com",
            telefono="3001234567",
        )
        self.assertEqual(cliente.identificador, "CLI-001")
        self.assertEqual(cliente.nombre_completo, "Juan Pérez")
        self.assertEqual(cliente.estado, "ACTIVO")
        cliente.validar()

    def test_nombre_vacio_lanza_excepcion(self):
        with self.assertRaises(ParametroFaltanteError):
            Cliente(
                identificador="CLI-002",
                nombre_completo="",
                numero_identificacion="12345678",
                correo_electronico="juan@correo.com",
                telefono="3001234567",
            )

    def test_correo_invalido_lanza_excepcion(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente(
                identificador="CLI-003",
                nombre_completo="Juan Pérez",
                numero_identificacion="12345678",
                correo_electronico="correo-invalido",
                telefono="3001234567",
            )

    def test_identificacion_invalida_lanza_excepcion(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente(
                identificador="CLI-004",
                nombre_completo="Juan Pérez",
                numero_identificacion="abc!@#",
                correo_electronico="juan@correo.com",
                telefono="3001234567",
            )

    def test_telefono_invalido_lanza_excepcion(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente(
                identificador="CLI-005",
                nombre_completo="Juan Pérez",
                numero_identificacion="12345678",
                correo_electronico="juan@correo.com",
                telefono="abc",
            )

    def test_encapsulamiento_setter_valida(self):
        cliente = Cliente(
            identificador="CLI-006",
            nombre_completo="Juan Pérez",
            numero_identificacion="12345678",
            correo_electronico="juan@correo.com",
            telefono="3001234567",
        )
        cliente.nombre_completo = "Juan Pérez Actualizado"
        self.assertEqual(cliente.nombre_completo, "Juan Pérez Actualizado")
        with self.assertRaises(ClienteInvalidoError):
            cliente.correo_electronico = "invalido"


class TestClienteServiceDuplicados(unittest.TestCase):
    """Validación de clientes duplicados en el servicio."""

    def setUp(self):
        self.service = ClienteService()
        self.service.registrar_cliente(
            identificador="CLI-010",
            nombre_completo="María López",
            numero_identificacion="11223344",
            correo_electronico="maria@correo.com",
            telefono="3001112223",
        )

    def test_registrar_cliente_duplicado_lanza_excepcion(self):
        with self.assertRaises(ClienteDuplicadoError):
            self.service.registrar_cliente(
                identificador="CLI-011",
                nombre_completo="Otro",
                numero_identificacion="11223344",
                correo_electronico="otro@correo.com",
                telefono="3002223333",
            )

    def test_buscar_por_identificacion_existente(self):
        cliente = self.service.buscar_por_identificacion("11223344")
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente.nombre_completo, "María López")

    def test_buscar_por_identificacion_inexistente(self):
        cliente = self.service.buscar_por_identificacion("99999999")
        self.assertIsNone(cliente)

    def test_listar_clientes(self):
        clientes = self.service.listar_clientes()
        self.assertEqual(len(clientes), 1)

    def test_total_clientes(self):
        self.assertEqual(self.service.total_clientes(), 1)

    def test_actualizar_cliente(self):
        cliente = self.service.actualizar_cliente(
            "CLI-010", telefono="3009998888"
        )
        self.assertEqual(cliente.telefono, "3009998888")

    def test_actualizar_cliente_inexistente(self):
        with self.assertRaises(ParametroFaltanteError):
            self.service.actualizar_cliente("CLI-INEXISTENTE", nombre="X")


if __name__ == "__main__":
    unittest.main()
