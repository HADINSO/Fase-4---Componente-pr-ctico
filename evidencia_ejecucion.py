"""
Script de generación de evidencias de ejecución real.

Ejecuta operaciones reales del sistema SOFTWARE FJ (registro de clientes,
servicios, reservas, cálculo de costos, errores controlados y continuidad)
e imprime los resultados. La salida se captura a archivos de texto en
EVIDENCIAS/ como capturas auténticas de ejecución.
"""

import io
from datetime import datetime

from services.cliente_service import ClienteService
from services.servicio_service import ServicioService
from services.reserva_service import ReservaService
from utils.logger import (
    configurar_logger, registrar_inicio_sistema, registrar_finalizacion_sistema,
    registrar_error_validacion, registrar_excepcion,
)
from exceptions.excepciones_personalizadas import (
    ParametroFaltanteError, ServicioInvalidoError, ServicioNoDisponibleError,
    ReservaInvalidaError, OperacionNoPermitidaError, CalculoCostoError,
)


def linea(titulo=""):
    return "\n" + "=" * 70 + (f"\n{titulo}" if titulo else "") + "\n" + "=" * 70


def ejecutar():
    salida = io.StringIO()

    def escribir(texto):
        salida.write(texto + "\n")

    escribir(linea("EVIDENCIA DE EJECUCIÓN REAL – SOFTWARE FJ"))
    escribir(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    escribir(f"Estudiante: JHON DAVINSON HINESTROZA MURILLO")
    escribir(f"Curso: Programación (213023) – Fase 4 – Componente práctico")
    escribir("Datos utilizados: ficticios, identificados como datos de prueba.")

    cliente_service = ClienteService()
    servicio_service = ServicioService()
    reserva_service = ReservaService()
    configurar_logger()
    registrar_inicio_sistema()

    def op(numero, descripcion, entrada_str, accion, esperado):
        escribir(f"\n--- Operación {numero}: {descripcion} ---")
        escribir(f"Datos de entrada: {entrada_str}")
        try:
            resultado = accion()
            escribir(f"Resultado obtenido: {resultado}")
            escribir(f"Estado: EXITOSA | Esperado: {esperado}")
        except Exception as exc:
            escribir(f"Resultado obtenido: ERROR CONTROLADO - {type(exc).__name__}: {exc}")
            escribir(f"Estado: ERROR CONTROLADO | Esperado: {esperado}")
            registrar_error_validacion(str(exc))
            registrar_excepcion(exc)

    # 1. Cliente válido
    op(1, "Registrar un cliente válido",
       "identificador=EVID-CLI-001, nombre='María González Pérez', identificacion='12345678', correo='maria@correo.com', teléfono='3001234567'",
       lambda: cliente_service.registrar_cliente(
           identificador="EVID-CLI-001", nombre_completo="María González Pérez",
           numero_identificacion="12345678", correo_electronico="maria@correo.com",
           telefono="3001234567", estado="ACTIVO"),
       "Cliente registrado exitosamente")

    # 2. Correo inválido
    op(2, "Registrar cliente con correo inválido",
       "identificador=EVID-CLI-002, nombre='Pedro Ramírez', identificacion='87654321', correo='correo-invalido', teléfono='3009876543'",
       lambda: cliente_service.registrar_cliente(
           identificador="EVID-CLI-002", nombre_completo="Pedro Ramírez",
           numero_identificacion="87654321", correo_electronico="correo-invalido",
           telefono="3009876543"),
       "Debe lanzar ClienteInvalidoError")

    # 3. Cliente duplicado
    op(3, "Registrar cliente duplicado",
       "identificador=EVID-CLI-DUP, nombre='Otro', identificacion='12345678' (duplicado), correo='otro@correo.com', teléfono='3001112223'",
       lambda: cliente_service.registrar_cliente(
           identificador="EVID-CLI-DUP", nombre_completo="Otro",
           numero_identificacion="12345678", correo_electronico="otro@correo.com",
           telefono="3001112223"),
       "Debe lanzar ClienteDuplicadoError")

    # 4. Otro cliente válido
    op(4, "Registrar otro cliente válido",
       "identificador=EVID-CLI-002, nombre='Ana López Torres', identificacion='11223344', correo='ana@correo.com', teléfono='3012223344'",
       lambda: cliente_service.registrar_cliente(
           identificador="EVID-CLI-002", nombre_completo="Ana López Torres",
           numero_identificacion="11223344", correo_electronico="ana@correo.com",
           telefono="3012223344", estado="ACTIVO"),
       "Cliente registrado exitosamente")

    # 5. Servicio sala
    op(5, "Crear servicio de reserva de sala",
       "tipo='sala', codigo='EVID-SALA-001', nombre='Sala de Conferencias A', precio_base=50000, capacidad=20, ubicación='Piso 3', duración=2, tarifa_por_hora=40000",
       lambda: servicio_service.registrar_servicio(
           tipo="sala", codigo="EVID-SALA-001", nombre="Sala de Conferencias A",
           descripcion="Sala para reuniones", precio_base=50000, disponible=True,
           capacidad=20, ubicacion="Piso 3", duracion=2,
           equipamiento="Proyector, pizarra", tarifa_por_hora=40000),
       "Servicio registrado exitosamente")

    # 6. Servicio alquiler equipos
    op(6, "Crear servicio de alquiler de equipos",
       "tipo='equipo', codigo='EVID-EQ-001', nombre='Alquiler de Proyectores', precio_base=30000, cantidad_disponible=5, precio_por_dia=25000",
       lambda: servicio_service.registrar_servicio(
           tipo="equipo", codigo="EVID-EQ-001", nombre="Alquiler de Proyectores",
           descripcion="Proyectores LCD", precio_base=30000, disponible=True,
           nombre_equipo="Proyector LCD 4000 lúmenes", cantidad_disponible=5,
           precio_por_dia=25000, condiciones_alquiler="Entrega incluida"),
       "Servicio registrado exitosamente")

    # 7. Servicio asesoría
    op(7, "Crear servicio de asesoría especializada",
       "tipo='asesoria', codigo='EVID-AS-001', nombre='Asesoría de Software', precio_base=100000, especialidad='Ingeniería de Software', profesional='Carlos Mendoza', duración=3, tarifa_por_hora=80000",
       lambda: servicio_service.registrar_servicio(
           tipo="asesoria", codigo="EVID-AS-001", nombre="Asesoría de Software",
           descripcion="Arquitectura de software", precio_base=100000,
           disponible=True, especialidad="Ingeniería de Software",
           profesional_asignado="Carlos Mendoza", duracion=3,
           tarifa_por_hora=80000),
       "Servicio registrado exitosamente")

    # 8. Precio negativo
    op(8, "Crear servicio con precio negativo",
       "tipo='sala', codigo='EVID-SALA-NEG', nombre='Sala Inválida', precio_base=-10000 (negativo), capacidad=20, ubicación='Piso 3', duración=2, tarifa_por_hora=40000",
       lambda: servicio_service.registrar_servicio(
           tipo="sala", codigo="EVID-SALA-NEG", nombre="Sala Inválida",
           descripcion="Prueba", precio_base=-10000, disponible=True,
           capacidad=20, ubicacion="Piso 3", duracion=2,
           equipamiento="Proyector", tarifa_por_hora=40000),
       "Debe lanzar ServicioInvalidoError")

    # 9. Costo básico
    op(9, "Calcular costo básico de servicio",
       "servicio='EVID-SALA-001', cantidad=1, impuesto=0, descuento=0",
       lambda: "$" + str(servicio_service.calcular_costo(
           "EVID-SALA-001", cantidad=1, impuesto=0.0, descuento=0.0)),
       "Costo = 40000 * 2 = 80000")

    # 10. Servicio inexistente
    op(10, "Calcular costo con servicio inexistente",
       "servicio='SRV-INEXISTENTE', cantidad=1, impuesto=0, descuento=0",
       lambda: servicio_service.calcular_costo("SRV-INEXISTENTE", cantidad=1,
                                               impuesto=0.0, descuento=0.0),
       "Debe lanzar ParametroFaltanteError")

    # 11. Reserva válida
    cliente1 = cliente_service.listar_clientes()[0]
    sala = servicio_service.buscar_por_codigo("EVID-SALA-001")
    op(11, "Crear una reserva válida",
       "id_reserva='EVID-RES-001', cliente='EVID-CLI-001', servicio='EVID-SALA-001', fecha='2026-11-20', duración=2",
       lambda: reserva_service.registrar_reserva(
           id_reserva="EVID-RES-001", cliente=cliente1, servicio=sala,
           fecha="2026-11-20", duracion=2),
       "Reserva en estado PENDIENTE")

    # 12. Confirmar reserva
    op(12, "Confirmar una reserva",
       "id_reserva='EVID-RES-001'",
       lambda: (reserva_service.confirmar_reserva("EVID-RES-001"),
                "Estado: " + reserva_service.consultar_reserva("EVID-RES-001").estado)[1],
       "Reserva en estado CONFIRMADA")

    # 13. Reserva sin cliente
    op(13, "Crear reserva sin cliente",
       "id_reserva='EVID-RES-SINCLI', cliente=None, servicio='EVID-SALA-001', fecha='2026-11-20', duración=2",
       lambda: reserva_service.registrar_reserva(
           id_reserva="EVID-RES-SINCLI", cliente=None, servicio=sala,
           fecha="2026-11-20", duracion=2),
       "Debe lanzar ParametroFaltanteError")

    # 14. Servicio no disponible
    servicio_nd = servicio_service.registrar_servicio(
        tipo="asesoria", codigo="EVID-ND-001", nombre="No Disponible",
        descripcion="Prueba", precio_base=50000, disponible=False,
        especialidad="Prueba", profesional_asignado="Nadie", duracion=1,
        tarifa_por_hora=40000)
    cliente2 = cliente_service.listar_clientes()[1]
    op(14, "Reservar servicio no disponible",
       "id_reserva='EVID-RES-ND', cliente='EVID-CLI-002', servicio='EVID-ND-001' (no disponible), fecha='2026-11-21', duración=1",
       lambda: reserva_service.registrar_reserva(
           id_reserva="EVID-RES-ND", cliente=cliente2, servicio=servicio_nd,
           fecha="2026-11-21", duracion=1),
       "Debe lanzar ServicioNoDisponibleError")

    # 15. Cancelar reserva finalizada
    asesoria = servicio_service.buscar_por_codigo("EVID-AS-001")
    reserva_service.registrar_reserva(
        id_reserva="EVID-RES-002", cliente=cliente1, servicio=asesoria,
        fecha="2026-11-21", duracion=1)
    reserva_service.confirmar_reserva("EVID-RES-002")
    reserva_service.finalizar_reserva("EVID-RES-002")
    op(15, "Cancelar reserva finalizada",
       "id_reserva='EVID-RES-002' (estado FINALIZADA)",
       lambda: reserva_service.cancelar_reserva("EVID-RES-002"),
       "Debe lanzar OperacionNoPermitidaError")

    # 16. Cancelar reserva pendiente
    equipo = servicio_service.buscar_por_codigo("EVID-EQ-001")
    reserva_service.registrar_reserva(
        id_reserva="EVID-RES-003", cliente=cliente2, servicio=equipo,
        fecha="2026-11-22", duracion=3)
    op(16, "Cancelar reserva pendiente",
       "id_reserva='EVID-RES-003' (estado PENDIENTE)",
       lambda: (reserva_service.cancelar_reserva("EVID-RES-003"),
                "Estado: " + reserva_service.consultar_reserva("EVID-RES-003").estado)[1],
       "Reserva en estado CANCELADA")

    # 17. Excepción encadenada
    escribir("\n--- Operación 17: Excepción encadenada (raise ... from) ---")
    try:
        try:
            servicio = servicio_service.buscar_por_codigo("SRV-ENCADENADO")
            if servicio is None:
                raise ParametroFaltanteError(
                    "Servicio no encontrado: SRV-ENCADENADO"
                )
        except ParametroFaltanteError as causa:
            raise CalculoCostoError("No se pudo calcular el costo") from causa
    except CalculoCostoError as exc:
        escribir("Datos de entrada: buscar servicio inexistente -> CalculoCostoError")
        escribir(f"Resultado obtenido: CalculoCostoError: {exc} | Causa: {exc.__cause__}")
        escribir("Estado: EXITOSA | Esperado: preservar la causa original")
        registrar_excepcion(exc, causa_original=exc.__cause__)

    # 18. Continuidad
    escribir("\n--- Operación 18: Continuidad del sistema tras un error ---")
    error_previo = None
    try:
        cliente_service.buscar_por_identificacion("ID-INEXISTENTE")
    except Exception as exc:
        error_previo = exc
        escribir(f"Error controlado (no detiene el sistema): {exc}")
    clientes = cliente_service.listar_clientes()
    nombre_tipo = type(error_previo).__name__ if error_previo else "ninguno"
    escribir(f"Resultado obtenido: El sistema continuó. Clientes registrados: {len(clientes)}. Error previo: {nombre_tipo}")
    escribir("Estado: EXITOSA | Esperado: el sistema sigue procesando operaciones independientes")

    escribir(linea("RESUMEN DE EJECUCIÓN"))
    escribir(f"Clientes registrados: {cliente_service.total_clientes()}")
    escribir(f"Servicios registrados: {servicio_service.total_servicios()}")
    escribir(f"Reservas registradas: {reserva_service.total_reservas()}")

    registrar_finalizacion_sistema()

    escribir(linea("CONTENIDO REAL DEL ARCHIVO DE LOGS"))
    from utils.logger import LOG_FILE
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            escribir(f.read())
    except Exception as exc:
        escribir(f"No se pudo leer el log: {exc}")

    return salida.getvalue()


if __name__ == "__main__":
    print(ejecutar())
