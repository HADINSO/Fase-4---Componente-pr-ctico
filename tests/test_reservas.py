"""
Pruebas automatizadas del módulo de reservas.

Cubre:
- Creación de reservas.
- Confirmación de reservas.
- Cancelaciones.
- Estados no permitidos (cancelar finalizada, confirmar cancelada, etc.).
- Reserva sin cliente ni servicio.
- Duraciones inválidas.
- Servicio no disponible.
"""

import unittest
from models.cliente import Cliente
from models.reserva_sala import ReservaSala
from models.alquiler_equipo import AlquilerEquipo
from models.asesoria import AsesoriaEspecializada
from models.reserva import Reserva
from services.reserva_service import ReservaService
from services.cliente_service import ClienteService
from services.servicio_service import ServicioService
from exceptions.excepciones_personalizadas import (
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ReservaNoEncontradaError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
)


class _Fixtures:
    """Crea clientes y servicios de apoyo para las pruebas de reservas."""

    @staticmethod
    def crear_cliente(identificador="CLI-RES-001", identificacion="12345678"):
        return Cliente(
            identificador=identificador,
            nombre_completo="Cliente Reserva",
            numero_identificacion=identificacion,
            correo_electronico="cliente@correo.com",
            telefono="3001234567",
        )

    @staticmethod
    def crear_servicio_disponible(codigo="SRV-RES-001"):
        return ReservaSala(
            codigo=codigo, nombre="Sala Disponible", descripcion="Desc",
            precio_base=50000, capacidad=20, ubicacion="Piso 3",
            duracion=2, equipamiento="Proyector", tarifa_por_hora=40000,
            disponible=True,
        )

    @staticmethod
    def crear_servicio_no_disponible(codigo="SRV-RES-ND"):
        return ReservaSala(
            codigo=codigo, nombre="Sala No Disponible", descripcion="Desc",
            precio_base=50000, capacidad=20, ubicacion="Piso 3",
            duracion=2, equipamiento="Proyector", tarifa_por_hora=40000,
            disponible=False,
        )


class TestCreacionReserva(unittest.TestCase):
    """Pruebas de creación de reservas."""

    def test_crear_reserva_valida(self):
        cliente = _Fixtures.crear_cliente()
        servicio = _Fixtures.crear_servicio_disponible()
        reserva = Reserva(
            id_reserva="RES-001", cliente=cliente, servicio=servicio,
            fecha="2026-11-20", duracion=2,
        )
        self.assertEqual(reserva.estado, Reserva.PENDIENTE)
        self.assertEqual(reserva.cliente.identificador, "CLI-RES-001")
        self.assertEqual(reserva.servicio.identificador, "SRV-RES-001")
        self.assertGreaterEqual(reserva.costo, 0)

    def test_crear_reserva_sin_cliente(self):
        servicio = _Fixtures.crear_servicio_disponible()
        with self.assertRaises(ParametroFaltanteError):
            Reserva(
                id_reserva="RES-002", cliente=None, servicio=servicio,
                fecha="2026-11-20", duracion=2,
            )

    def test_crear_reserva_sin_servicio(self):
        cliente = _Fixtures.crear_cliente()
        with self.assertRaises(ParametroFaltanteError):
            Reserva(
                id_reserva="RES-003", cliente=cliente, servicio=None,
                fecha="2026-11-20", duracion=2,
            )

    def test_crear_reserva_duracion_cero(self):
        cliente = _Fixtures.crear_cliente()
        servicio = _Fixtures.crear_servicio_disponible()
        with self.assertRaises(ParametroFaltanteError):
            Reserva(
                id_reserva="RES-004", cliente=cliente, servicio=servicio,
                fecha="2026-11-20", duracion=0,
            )

    def test_crear_reserva_duracion_negativa(self):
        cliente = _Fixtures.crear_cliente()
        servicio = _Fixtures.crear_servicio_disponible()
        with self.assertRaises(ParametroFaltanteError):
            Reserva(
                id_reserva="RES-005", cliente=cliente, servicio=servicio,
                fecha="2026-11-20", duracion=-2,
            )

    def test_crear_reserva_servicio_no_disponible(self):
        cliente = _Fixtures.crear_cliente()
        servicio = _Fixtures.crear_servicio_no_disponible()
        with self.assertRaises(ServicioNoDisponibleError):
            Reserva(
                id_reserva="RES-006", cliente=cliente, servicio=servicio,
                fecha="2026-11-20", duracion=2,
            ).validar_disponibilidad()


class TestConfirmacionCancelacionReserva(unittest.TestCase):
    """Pruebas de confirmación, cancelación y estados no permitidos."""

    def setUp(self):
        self.cliente = _Fixtures.crear_cliente()
        self.servicio = _Fixtures.crear_servicio_disponible()
        self.reserva = Reserva(
            id_reserva="RES-ST-001", cliente=self.cliente,
            servicio=self.servicio, fecha="2026-11-20", duracion=2,
        )

    def test_confirmar_reserva_pasada_a_confirmada(self):
        self.reserva.confirmar()
        self.assertEqual(self.reserva.estado, Reserva.CONFIRMADA)

    def test_confirmar_reserva_cancelada_no_permitido(self):
        self.reserva.cancelar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.confirmar()

    def test_confirmar_reserva_finalizada_no_permitido(self):
        self.reserva.confirmar()
        self.reserva.finalizar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.confirmar()

    def test_cancelar_reserva_pasada_a_cancelada(self):
        self.reserva.cancelar()
        self.assertEqual(self.reserva.estado, Reserva.CANCELADA)

    def test_cancelar_reserva_finalizada_no_permitido(self):
        self.reserva.confirmar()
        self.reserva.finalizar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.cancelar()

    def test_cancelar_reserva_ya_cancelada_no_permitido(self):
        self.reserva.cancelar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.cancelar()

    def test_finalizar_reserva_solo_desde_confirmada(self):
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.finalizar()
        self.reserva.confirmar()
        self.reserva.finalizar()
        self.assertEqual(self.reserva.estado, Reserva.FINALIZADA)

    def test_estados_permitidos(self):
        self.assertIn(Reserva.PENDIENTE, Reserva.ESTADOS_PERMITIDOS)
        self.assertIn(Reserva.CONFIRMADA, Reserva.ESTADOS_PERMITIDOS)
        self.assertIn(Reserva.CANCELADA, Reserva.ESTADOS_PERMITIDOS)
        self.assertIn(Reserva.FINALIZADA, Reserva.ESTADOS_PERMITIDOS)

    def test_estado_invalido_lanza_excepcion(self):
        with self.assertRaises(ReservaInvalidaError):
            Reserva(
                id_reserva="RES-007", cliente=self.cliente,
                servicio=self.servicio, fecha="2026-11-20", duracion=2,
                estado="ESTADO-INVALIDO",
            )


class TestReservaService(unittest.TestCase):
    """Pruebas del ReservaService."""

    def setUp(self):
        self.cliente_service = ClienteService()
        self.servicio_service = ServicioService()
        self.reserva_service = ReservaService()
        self.cliente_service.registrar_cliente(
            identificador="CLI-SVC-001", nombre_completo="Cliente Svc",
            numero_identificacion="99887766", correo_electronico="c@correo.com",
            telefono="3001234567",
        )
        self.servicio_service.registrar_servicio(
            tipo="sala", codigo="SRV-SVC-001", nombre="Sala Svc",
            descripcion="Desc", precio_base=50000, capacidad=20,
            ubicacion="Piso 3", duracion=2, equipamiento="Proyector",
            tarifa_por_hora=40000,
        )

    def _obtener_cliente(self):
        return self.cliente_service.buscar_por_id("CLI-SVC-001")

    def _obtener_servicio(self):
        return self.servicio_service.buscar_por_codigo("SRV-SVC-001")

    def test_registrar_reserva(self):
        reserva = self.reserva_service.registrar_reserva(
            id_reserva="RES-SVC-001", cliente=self._obtener_cliente(),
            servicio=self._obtener_servicio(), fecha="2026-11-20", duracion=2,
        )
        self.assertEqual(reserva.estado, Reserva.PENDIENTE)
        self.assertEqual(self.reserva_service.total_reservas(), 1)

    def test_listar_reservas(self):
        self.reserva_service.registrar_reserva(
            id_reserva="RES-SVC-002", cliente=self._obtener_cliente(),
            servicio=self._obtener_servicio(), fecha="2026-11-20", duracion=2,
        )
        reservas = self.reserva_service.listar_reservas()
        self.assertEqual(len(reservas), 1)

    def test_confirmar_reserva_via_service(self):
        self.reserva_service.registrar_reserva(
            id_reserva="RES-SVC-003", cliente=self._obtener_cliente(),
            servicio=self._obtener_servicio(), fecha="2026-11-20", duracion=2,
        )
        self.reserva_service.confirmar_reserva("RES-SVC-003")
        reserva = self.reserva_service.consultar_reserva("RES-SVC-003")
        self.assertEqual(reserva.estado, Reserva.CONFIRMADA)

    def test_cancelar_reserva_via_service(self):
        self.reserva_service.registrar_reserva(
            id_reserva="RES-SVC-004", cliente=self._obtener_cliente(),
            servicio=self._obtener_servicio(), fecha="2026-11-20", duracion=2,
        )
        self.reserva_service.cancelar_reserva("RES-SVC-004")
        reserva = self.reserva_service.consultar_reserva("RES-SVC-004")
        self.assertEqual(reserva.estado, Reserva.CANCELADA)

    def test_reserva_no_encontrada(self):
        with self.assertRaises(ReservaNoEncontradaError):
            self.reserva_service.consultar_reserva("RES-INEXISTENTE")

    def test_reserva_duplicada(self):
        self.reserva_service.registrar_reserva(
            id_reserva="RES-SVC-005", cliente=self._obtener_cliente(),
            servicio=self._obtener_servicio(), fecha="2026-11-20", duracion=2,
        )
        with self.assertRaises(ReservaInvalidaError):
            self.reserva_service.registrar_reserva(
                id_reserva="RES-SVC-005", cliente=self._obtener_cliente(),
                servicio=self._obtener_servicio(), fecha="2026-11-20", duracion=2,
            )

    def test_reservas_por_estado(self):
        self.reserva_service.registrar_reserva(
            id_reserva="RES-EST-001", cliente=self._obtener_cliente(),
            servicio=self._obtener_servicio(), fecha="2026-11-20", duracion=2,
        )
        pendientes = self.reserva_service.reservas_por_estado("PENDIENTE")
        self.assertEqual(len(pendientes), 1)


if __name__ == "__main__":
    unittest.main()
