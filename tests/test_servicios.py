"""
Pruebas automatizadas del módulo de servicios.

Cubre:
- Validaciones de servicios (precio negativo, tipo inválido).
- Polimorfismo sobre referencias de tipo Servicio.
- Cálculos de costos: básico, con impuesto, con descuento, ambos.
- Registro, consulta y listado de servicios.
- Cambio de disponibilidad.
"""

import unittest
from models.servicio import Servicio
from models.reserva_sala import ReservaSala
from models.alquiler_equipo import AlquilerEquipo
from models.asesoria import AsesoriaEspecializada
from services.servicio_service import ServicioService
from exceptions.excepciones_personalizadas import (
    ServicioInvalidoError,
    ParametroFaltanteError,
    CalculoCostoError,
)


class TestServicioAbstracto(unittest.TestCase):
    """La clase Servicio es abstracta y no debe poder instanciarse directamente."""

    def test_servicio_no_se_puede_instanciar(self):
        with self.assertRaises(TypeError):
            Servicio(
                codigo="SRV-001", nombre="Servicio genérico",
                descripcion="Desc", precio_base=10000,
            )


class TestServicioValidaciones(unittest.TestCase):
    """Validaciones de datos de los servicios."""

    def test_servicio_con_precio_negativo(self):
        with self.assertRaises(ServicioInvalidoError):
            ReservaSala(
                codigo="SRV-002", nombre="Sala X", descripcion="Desc",
                precio_base=-5000, capacidad=10, ubicacion="Ubi",
                duracion=1, equipamiento="Proyector", tarifa_por_hora=20000,
            )

    def test_servicio_sin_nombre(self):
        with self.assertRaises(ParametroFaltanteError):
            ReservaSala(
                codigo="SRV-003", nombre="", descripcion="Desc",
                precio_base=10000, capacidad=10, ubicacion="Ubi",
                duracion=1, equipamiento="Proyector", tarifa_por_hora=20000,
            )


class TestServicioService(unittest.TestCase):
    """Pruebas del ServicioService."""

    def setUp(self):
        self.service = ServicioService()

    def test_registrar_y_listar_servicios(self):
        self.service.registrar_servicio(
            tipo="sala", codigo="SRV-SALA-01", nombre="Sala A",
            descripcion="Sala de reuniones", precio_base=50000,
            capacidad=20, ubicacion="Piso 3", duracion=2,
            equipamiento="Proyector", tarifa_por_hora=40000,
        )
        self.service.registrar_servicio(
            tipo="equipo", codigo="SRV-EQ-01", nombre="Proyector",
            descripcion="Proyector LCD", precio_base=30000,
            nombre_equipo="Proyector", cantidad_disponible=5,
            precio_por_dia=25000, condiciones_alquiler="Entrega incluida",
        )
        servicios = self.service.listar_servicios()
        self.assertEqual(len(servicios), 2)

    def test_buscar_por_codigo(self):
        self.service.registrar_servicio(
            tipo="asesoria", codigo="SRV-AS-01", nombre="Asesoría",
            descripcion="Asesoría de software", precio_base=100000,
            especialidad="Software", profesional_asignado="Carlos",
            duracion=3, tarifa_por_hora=80000,
        )
        servicio = self.service.buscar_por_codigo("SRV-AS-01")
        self.assertIsNotNone(servicio)
        self.assertEqual(servicio.nombre, "Asesoría")

    def test_buscar_por_codigo_inexistente(self):
        servicio = self.service.buscar_por_codigo("SRV-INEXISTENTE")
        self.assertIsNone(servicio)

    def test_cambiar_disponibilidad(self):
        self.service.registrar_servicio(
            tipo="sala", codigo="SRV-DISP-01", nombre="Sala",
            descripcion="Desc", precio_base=10000, disponible=True,
            capacidad=10, ubicacion="Ubi", duracion=1,
            equipamiento="Proyector", tarifa_por_hora=20000,
        )
        self.service.cambiar_disponibilidad("SRV-DISP-01", False)
        servicio = self.service.buscar_por_codigo("SRV-DISP-01")
        self.assertFalse(servicio.disponible)

    def test_cambiar_disponibilidad_inexistente(self):
        with self.assertRaises(ParametroFaltanteError):
            self.service.cambiar_disponibilidad("SRV-INEXISTENTE", True)


class TestPolimorfismo(unittest.TestCase):
    """Polimorfismo: operaciones sobre referencias de tipo Servicio."""

    def setUp(self):
        self.servicios = [
            ReservaSala(
                codigo="SRV-POL-01", nombre="Sala A", descripcion="Desc",
                precio_base=50000, capacidad=20, ubicacion="Piso 3",
                duracion=2, equipamiento="Proyector", tarifa_por_hora=40000,
            ),
            AlquilerEquipo(
                codigo="SRV-POL-02", nombre="Proyector", descripcion="Desc",
                precio_base=30000, nombre_equipo="Proyector LCD",
                cantidad_disponible=5, precio_por_dia=25000,
                condiciones_alquiler="Entrega incluida",
            ),
            AsesoriaEspecializada(
                codigo="SRV-POL-03", nombre="Asesoría", descripcion="Desc",
                precio_base=100000, especialidad="Software",
                profesional_asignado="Carlos", duracion=3,
                tarifa_por_hora=80000,
            ),
        ]

    def test_describir_servicio_polimorfico(self):
        for servicio in self.servicios:
            descripcion = servicio.describir_servicio()
            self.assertIsInstance(descripcion, str)
            self.assertGreater(len(descripcion), 0)

    def test_calcular_costo_polimorfico(self):
        for servicio in self.servicios:
            costo = servicio.calcular_costo(cantidad=1)
            self.assertIsInstance(costo, (int, float))
            self.assertGreaterEqual(costo, 0)

    def test_todos_son_instancia_de_servicio(self):
        for servicio in self.servicios:
            self.assertIsInstance(servicio, Servicio)


class TestCalculosCosto(unittest.TestCase):
    """Cálculos de costos con variantes de argumentos."""

    def setUp(self):
        self.sala = ReservaSala(
            codigo="SRV-COST-01", nombre="Sala", descripcion="Desc",
            precio_base=50000, capacidad=20, ubicacion="Piso 3",
            duracion=2, equipamiento="Proyector", tarifa_por_hora=40000,
        )
        self.equipo = AlquilerEquipo(
            codigo="SRV-COST-02", nombre="Proyector", descripcion="Desc",
            precio_base=30000, nombre_equipo="Proyector LCD",
            cantidad_disponible=5, precio_por_dia=25000,
            condiciones_alquiler="Entrega incluida",
        )
        self.asesoria = AsesoriaEspecializada(
            codigo="SRV-COST-03", nombre="Asesoría", descripcion="Desc",
            precio_base=100000, especialidad="Software",
            profesional_asignado="Carlos", duracion=3, tarifa_por_hora=80000,
        )

    def test_costo_basico_sala(self):
        # tarifa_por_hora * duracion * cantidad = 40000 * 2 * 1 = 80000
        costo = self.sala.calcular_costo(cantidad=1, impuesto=0.0, descuento=0.0)
        self.assertEqual(costo, 80000.0)

    def test_costo_con_impuesto(self):
        costo = self.sala.calcular_costo(cantidad=1, impuesto=19.0, descuento=0.0)
        self.assertAlmostEqual(costo, 80000 * 1.19, places=2)

    def test_costo_con_descuento(self):
        costo = self.sala.calcular_costo(cantidad=1, impuesto=0.0, descuento=10.0)
        self.assertAlmostEqual(costo, 80000 * 0.90, places=2)

    def test_costo_con_impuesto_y_descuento(self):
        costo = self.sala.calcular_costo(cantidad=1, impuesto=19.0, descuento=10.0)
        esperado = 80000 * 0.90 * 1.19
        self.assertAlmostEqual(costo, esperado, places=2)

    def test_costo_basico_equipo(self):
        # precio_por_dia * cantidad = 25000 * 1 = 25000
        costo = self.equipo.calcular_costo(cantidad=1, impuesto=0.0, descuento=0.0)
        self.assertEqual(costo, 25000.0)

    def test_costo_basico_asesoria(self):
        # tarifa_por_hora * duracion * cantidad = 80000 * 3 * 1 = 240000
        costo = self.asesoria.calcular_costo(cantidad=1, impuesto=0.0, descuento=0.0)
        self.assertEqual(costo, 240000.0)

    def test_descuento_mayor_a_100_lanza_excepcion(self):
        with self.assertRaises(CalculoCostoError):
            self.sala.calcular_costo(cantidad=1, impuesto=0.0, descuento=150.0)

    def test_cantidad_menor_a_disponible_equipo(self):
        costo = self.equipo.calcular_costo(cantidad=3, impuesto=0.0, descuento=0.0)
        self.assertEqual(costo, 25000 * 3)

    def test_cantidad_mayor_a_disponible_equipo(self):
        with self.assertRaises(CalculoCostoError):
            self.equipo.calcular_costo(cantidad=100, impuesto=0.0, descuento=0.0)


class TestServicioServiceCalculoPolimorfico(unittest.TestCase):
    """Cálculo de costos mediante el servicio (polimorfismo)."""

    def setUp(self):
        self.service = ServicioService()
        self.service.registrar_servicio(
            tipo="sala", codigo="SRV-SVC-01", nombre="Sala",
            descripcion="Desc", precio_base=50000, capacidad=20,
            ubicacion="Piso 3", duracion=2, equipamiento="Proyector",
            tarifa_por_hora=40000,
        )

    def test_calcular_costo_via_servicio(self):
        costo = self.service.calcular_costo(
            servicio_codigo="SRV-SVC-01", cantidad=1, impuesto=0.0,
            descuento=0.0,
        )
        self.assertEqual(costo, 80000.0)

    def test_calcular_costo_servicio_inexistente(self):
        with self.assertRaises(ParametroFaltanteError):
            self.service.calcular_costo(
                servicio_codigo="SRV-INEXISTENTE", cantidad=1,
                impuesto=0.0, descuento=0.0,
            )


if __name__ == "__main__":
    unittest.main()
