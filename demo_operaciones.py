"""
Módulo de demostración de operaciones del sistema SOFTWARE FJ.

Ejecuta 18 escenarios diferenciados (correctos e incorrectos) que cubren
los requisitos funcionales de la Fase 4. Cada operación registra:
número, descripción, datos de entrada, resultado esperado, resultado
obtenido, estado (EXITOSA / ERROR CONTROLADO) y excepción generada.

Los datos son ficticios y claramente identificados como datos de prueba.
"""

from exceptions.excepciones_personalizadas import (
    ClienteInvalidoError,
    ClienteDuplicadoError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ReservaNoEncontradaError,
    CalculoCostoError,
    ParametroFaltanteError,
)
from utils.logger import (
    registrar_evento,
    registrar_cliente,
    registrar_servicio,
    registrar_reserva,
    registrar_confirmacion_reserva,
    registrar_cancelacion_reserva,
    registrar_advertencia,
    registrar_excepcion,
    registrar_error_validacion,
)

# Identificadores de datos de prueba (ficticios)
PRUEBA_CLIENTE_1 = "CLI-TEST-001"
PRUEBA_CLIENTE_2 = "CLI-TEST-002"
PRUEBA_SERVICIO_SALA = "SRV-SALA-001"
PRUEBA_SERVICIO_EQUIPO = "SRV-EQUIPO-001"
PRUEBA_SERVICIO_ASESORIA = "SRV-ASES-001"
PRUEBA_RESERVA_1 = "RES-TEST-001"
PRUEBA_RESERVA_2 = "RES-TEST-002"
PRUEBA_RESERVA_3 = "RES-TEST-003"

resultados = []


def _registrar_resultado(numero, descripcion, entrada, esperado, obtenido,
                         estado, excepcion=None):
    resultados.append({
        "numero": numero,
        "descripcion": descripcion,
        "entrada": entrada,
        "esperado": esperado,
        "obtenido": obtenido,
        "estado": estado,
        "excepcion": type(excepcion).__name__ if excepcion else None,
        "mensaje_excepcion": str(excepcion) if excepcion else None,
    })
    estado_str = "EXITOSA" if estado == "EXITOSA" else "ERROR CONTROLADO"
    print(f"[{numero:02d}] {estado_str}: {descripcion}")
    if excepcion is not None:
        print(f"       Excepción: {type(excepcion).__name__} - {excepcion}")


def _mostrar_resumen():
    print("\n" + "=" * 70)
    print("RESUMEN DE LA DEMOSTRACIÓN DE OPERACIONES")
    print("=" * 70)
    exitosas = sum(1 for r in resultados if r["estado"] == "EXITOSA")
    controlados = sum(1 for r in resultados if r["estado"] == "ERROR CONTROLADO")
    print(f"Total de operaciones ejecutadas: {len(resultados)}")
    print(f"Exitosas: {exitosas}")
    print(f"Errores controlados: {controlados}")
    print("=" * 70)
    registrar_evento(
        f"Demo finalizada: {len(resultados)} operaciones, "
        f"{exitosas} exitosas, {controlados} errores controlados", "INFO"
    )


def ejecutar_demostracion(cliente_service, servicio_service, reserva_service):
    """Ejecuta los escenarios de demostración e imprime los resultados."""
    global resultados
    resultados = []

    print("\n" + "=" * 70)
    print("DEMOSTRACIÓN DE OPERACIONES - SOFTWARE FJ")
    print("Datos de prueba ficticios - Sistema de Gestión de Clientes,")
    print("Servicios y Reservas")
    print("=" * 70)

    # ---- OPERACIÓN 1: Registrar un cliente válido ----
    print("\n--- Operación 1: Registrar un cliente válido ---")
    entrada = {
        "identificador": PRUEBA_CLIENTE_1,
        "nombre": "María González Pérez",
        "identificacion": "12345678",
        "correo": "maria.gonzalez@correo.com",
        "telefono": "3001234567",
    }
    try:
        cliente = cliente_service.registrar_cliente(
            identificador=PRUEBA_CLIENTE_1,
            nombre_completo=entrada["nombre"],
            numero_identificacion=entrada["identificacion"],
            correo_electronico=entrada["correo"],
            telefono=entrada["telefono"],
            estado="ACTIVO",
        )
        obtenido = f"Cliente creado: {cliente.identificador} - {cliente.nombre_completo}"
        _registrar_resultado(
            1, "Registrar un cliente válido", entrada,
            "Cliente registrado exitosamente", obtenido, "EXITOSA",
        )
        registrar_cliente(cliente.identificador, cliente.nombre_completo, "registrado")
    except Exception as exc:
        _registrar_resultado(
            1, "Registrar un cliente válido", entrada,
            "Cliente registrado exitosamente",
            f"Error: {exc}", "ERROR CONTROLADO", exc,
        )

    # ---- OPERACIÓN 2: Cliente con correo inválido ----
    print("\n--- Operación 2: Cliente con correo inválido ---")
    entrada = {
        "identificador": "CLI-TEST-002",
        "nombre": "Pedro Ramírez",
        "identificacion": "87654321",
        "correo": "correo-invalido",
        "telefono": "3009876543",
    }
    try:
        cliente_service.registrar_cliente(
            identificador="CLI-TEST-002",
            nombre_completo=entrada["nombre"],
            numero_identificacion=entrada["identificacion"],
            correo_electronico=entrada["correo"],
            telefono=entrada["telefono"],
        )
        obtenido = "No se lanzó excepción (fallo del escenario)"
        _registrar_resultado(
            2, "Registrar cliente con correo inválido", entrada,
            "Debe lanzar ClienteInvalidoError", obtenido, "ERROR CONTROLADO",
        )
    except ClienteInvalidoError as exc:
        obtenido = f"ClienteInvalidoError: {exc}"
        _registrar_resultado(
            2, "Registrar cliente con correo inválido", entrada,
            "Debe lanzar ClienteInvalidoError", obtenido, "ERROR CONTROLADO", exc,
        )
        registrar_error_validacion(str(exc))
        registrar_excepcion(exc)

    # ---- OPERACIÓN 3: Cliente duplicado ----
    print("\n--- Operación 3: Cliente duplicado ---")
    entrada = {
        "identificador": "CLI-DUP-001",
        "nombre": "Otro Nombre",
        "identificacion": "12345678",
        "correo": "otro@correo.com",
        "telefono": "3001112223",
    }
    try:
        cliente_service.registrar_cliente(
            identificador="CLI-DUP-001",
            nombre_completo=entrada["nombre"],
            numero_identificacion=entrada["identificacion"],
            correo_electronico=entrada["correo"],
            telefono=entrada["telefono"],
        )
        obtenido = "No se lanzó excepción (fallo del escenario)"
        _registrar_resultado(
            3, "Registrar cliente duplicado", entrada,
            "Debe lanzar ClienteDuplicadoError", obtenido, "ERROR CONTROLADO",
        )
    except ClienteDuplicadoError as exc:
        obtenido = f"ClienteDuplicadoError: {exc}"
        _registrar_resultado(
            3, "Registrar cliente duplicado", entrada,
            "Debe lanzar ClienteDuplicadoError", obtenido, "ERROR CONTROLADO", exc,
        )
        registrar_error_validacion(str(exc))
        registrar_excepcion(exc)

    # ---- OPERACIÓN 4: Registrar otro cliente válido ----
    print("\n--- Operación 4: Registrar otro cliente válido ---")
    entrada = {
        "identificador": PRUEBA_CLIENTE_2,
        "nombre": "Ana López Torres",
        "identificacion": "11223344",
        "correo": "ana.lopez@correo.com",
        "telefono": "3012223344",
    }
    try:
        cliente = cliente_service.registrar_cliente(
            identificador=PRUEBA_CLIENTE_2,
            nombre_completo=entrada["nombre"],
            numero_identificacion=entrada["identificacion"],
            correo_electronico=entrada["correo"],
            telefono=entrada["telefono"],
        )
        obtenido = f"Cliente creado: {cliente.identificador} - {cliente.nombre_completo}"
        _registrar_resultado(
            4, "Registrar otro cliente válido", entrada,
            "Cliente registrado exitosamente", obtenido, "EXITOSA",
        )
        registrar_cliente(cliente.identificador, cliente.nombre_completo, "registrado")
    except Exception as exc:
        _registrar_resultado(
            4, "Registrar otro cliente válido", entrada,
            "Cliente registrado exitosamente",
            f"Error: {exc}", "ERROR CONTROLADO", exc,
        )

    # ---- OPERACIÓN 5: Crear servicio de reserva de sala ----
    print("\n--- Operación 5: Crear servicio de reserva de sala ---")
    entrada = {
        "tipo": "sala",
        "codigo": PRUEBA_SERVICIO_SALA,
        "nombre": "Sala de Conferencias A",
        "descripcion": "Sala para reuniones y conferencias",
        "precio_base": 50000,
        "capacidad": 20,
        "ubicacion": "Piso 3, Edificio Principal",
        "duracion": 2,
        "equipamiento": "Proyector, pizarra, sonido",
        "tarifa_por_hora": 40000,
    }
    try:
        servicio = servicio_service.registrar_servicio(
            tipo="sala", codigo=PRUEBA_SERVICIO_SALA, nombre=entrada["nombre"],
            descripcion=entrada["descripcion"], precio_base=entrada["precio_base"],
            disponible=True, capacidad=entrada["capacidad"],
            ubicacion=entrada["ubicacion"], duracion=entrada["duracion"],
            equipamiento=entrada["equipamiento"],
            tarifa_por_hora=entrada["tarifa_por_hora"],
        )
        obtenido = f"Servicio creado: {servicio.identificador} - {servicio.nombre}"
        _registrar_resultado(
            5, "Crear servicio de reserva de sala", entrada,
            "Servicio registrado exitosamente", obtenido, "EXITOSA",
        )
        registrar_servicio(servicio.identificador, servicio.nombre, "creado")
    except Exception as exc:
        _registrar_resultado(
            5, "Crear servicio de reserva de sala", entrada,
            "Servicio registrado exitosamente",
            f"Error: {exc}", "ERROR CONTROLADO", exc,
        )

    # ---- OPERACIÓN 6: Crear servicio de alquiler de equipos ----
    print("\n--- Operación 6: Crear servicio de alquiler de equipos ---")
    entrada = {
        "tipo": "equipo",
        "codigo": PRUEBA_SERVICIO_EQUIPO,
        "nombre": "Alquiler de Proyectores",
        "descripcion": "Alquiler de equipos de proyección",
        "precio_base": 30000,
        "nombre_equipo": "Proyector LCD 4000 lúmenes",
        "cantidad_disponible": 5,
        "precio_por_dia": 25000,
        "condiciones": "Entrega y recogida incluidas",
    }
    try:
        servicio = servicio_service.registrar_servicio(
            tipo="equipo", codigo=PRUEBA_SERVICIO_EQUIPO, nombre=entrada["nombre"],
            descripcion=entrada["descripcion"], precio_base=entrada["precio_base"],
            disponible=True, nombre_equipo=entrada["nombre_equipo"],
            cantidad_disponible=entrada["cantidad_disponible"],
            precio_por_dia=entrada["precio_por_dia"],
            condiciones_alquiler=entrada["condiciones"],
        )
        obtenido = f"Servicio creado: {servicio.identificador} - {servicio.nombre}"
        _registrar_resultado(
            6, "Crear servicio de alquiler de equipos", entrada,
            "Servicio registrado exitosamente", obtenido, "EXITOSA",
        )
        registrar_servicio(servicio.identificador, servicio.nombre, "creado")
    except Exception as exc:
        _registrar_resultado(
            6, "Crear servicio de alquiler de equipos", entrada,
            "Servicio registrado exitosamente",
            f"Error: {exc}", "ERROR CONTROLADO", exc,
        )

    # ---- OPERACIÓN 7: Crear servicio de asesoría especializada ----
    print("\n--- Operación 7: Crear servicio de asesoría especializada ---")
    entrada = {
        "tipo": "asesoria",
        "codigo": PRUEBA_SERVICIO_ASESORIA,
        "nombre": "Asesoría en Ingeniería de Software",
        "descripcion": "Asesoría especializada en arquitectura de software",
        "precio_base": 100000,
        "especialidad": "Ingeniería de Software",
        "profesional_asignado": "Carlos Mendoza",
        "duracion": 3,
        "tarifa_por_hora": 80000,
    }
    try:
        servicio = servicio_service.registrar_servicio(
            tipo="asesoria", codigo=PRUEBA_SERVICIO_ASESORIA,
            nombre=entrada["nombre"], descripcion=entrada["descripcion"],
            precio_base=entrada["precio_base"], disponible=True,
            especialidad=entrada["especialidad"],
            profesional_asignado=entrada["profesional_asignado"],
            duracion=entrada["duracion"],
            tarifa_por_hora=entrada["tarifa_por_hora"],
        )
        obtenido = f"Servicio creado: {servicio.identificador} - {servicio.nombre}"
        _registrar_resultado(
            7, "Crear servicio de asesoría especializada", entrada,
            "Servicio registrado exitosamente", obtenido, "EXITOSA",
        )
        registrar_servicio(servicio.identificador, servicio.nombre, "creado")
    except Exception as exc:
        _registrar_resultado(
            7, "Crear servicio de asesoría especializada", entrada,
            "Servicio registrado exitosamente",
            f"Error: {exc}", "ERROR CONTROLADO", exc,
        )

    # ---- OPERACIÓN 8: Servicio con precio negativo ----
    print("\n--- Operación 8: Servicio con precio negativo ---")
    entrada = {
        "tipo": "sala",
        "codigo": "SRV-SALA-NEG",
        "nombre": "Sala con precio inválido",
        "descripcion": "Prueba de precio negativo",
        "precio_base": -10000,
    }
    try:
        servicio_service.registrar_servicio(
            tipo="sala", codigo=entrada["codigo"], nombre=entrada["nombre"],
            descripcion=entrada["descripcion"], precio_base=entrada["precio_base"],
        )
        obtenido = "No se lanzó excepción (fallo del escenario)"
        _registrar_resultado(
            8, "Crear servicio con precio negativo", entrada,
            "Debe lanzar ServicioInvalidoError", obtenido, "ERROR CONTROLADO",
        )
    except ServicioInvalidoError as exc:
        obtenido = f"ServicioInvalidoError: {exc}"
        _registrar_resultado(
            8, "Crear servicio con precio negativo", entrada,
            "Debe lanzar ServicioInvalidoError", obtenido, "ERROR CONTROLADO", exc,
        )
        registrar_error_validacion(str(exc))
        registrar_excepcion(exc)

    # ---- OPERACIÓN 9: Calcular correctamente el costo de un servicio ----
    print("\n--- Operación 9: Calcular costo de un servicio ---")
    entrada = {
        "servicio": PRUEBA_SERVICIO_SALA,
        "cantidad": 1,
        "impuesto": 0,
        "descuento": 0,
    }
    try:
        costo = servicio_service.calcular_costo(
            servicio_codigo=PRUEBA_SERVICIO_SALA, cantidad=1,
            impuesto=0.0, descuento=0.0,
        )
        esperado = "Costo = tarifa_por_hora * duracion = 40000 * 2 = 80000"
        obtenido = f"Costo básico calculado: ${costo}"
        _registrar_resultado(
            9, "Calcular costo básico de servicio", entrada,
            esperado, obtenido, "EXITOSA",
        )
    except Exception as exc:
        _registrar_resultado(
            9, "Calcular costo básico de servicio", entrada,
            "Costo calculado correctamente",
            f"Error: {exc}", "ERROR CONTROLADO", exc,
        )

    print("\n   Variantes de cálculo de costo (polimorfismo + argumentos opcionales):")
    variantes = [
        ("Básico", {"cantidad": 1, "impuesto": 0.0, "descuento": 0.0}),
        ("Con impuesto 19%", {"cantidad": 1, "impuesto": 19.0, "descuento": 0.0}),
        ("Con descuento 10%", {"cantidad": 1, "impuesto": 0.0, "descuento": 10.0}),
        ("Con impuesto y descuento", {"cantidad": 1, "impuesto": 19.0, "descuento": 10.0}),
    ]
    for nombre_variante, args in variantes:
        try:
            costo_v = servicio_service.calcular_costo(
                servicio_codigo=PRUEBA_SERVICIO_SALA, **args,
            )
            print(f"      {nombre_variante}: ${costo_v}")
        except Exception as exc:
            print(f"      {nombre_variante}: Error - {exc}")

    # ---- OPERACIÓN 10: Calcular costo con parámetros incorrectos ----
    print("\n--- Operación 10: Calcular costo con parámetros incorrectos ---")
    entrada = {"servicio": "SRV-NO-EXISTE", "cantidad": 1, "impuesto": 0, "descuento": 0}
    try:
        servicio_service.calcular_costo(
            servicio_codigo="SRV-NO-EXISTE", cantidad=1, impuesto=0.0, descuento=0.0,
        )
        obtenido = "No se lanzó excepción (fallo del escenario)"
        _registrar_resultado(
            10, "Calcular costo con servicio inexistente", entrada,
            "Debe lanzar ParametroFaltanteError", obtenido, "ERROR CONTROLADO",
        )
    except ParametroFaltanteError as exc:
        obtenido = f"ParametroFaltanteError: {exc}"
        _registrar_resultado(
            10, "Calcular costo con servicio inexistente", entrada,
            "Debe lanzar ParametroFaltanteError", obtenido, "ERROR CONTROLADO", exc,
        )
        registrar_error_validacion(str(exc))
        registrar_excepcion(exc)

    # ---- OPERACIÓN 11: Crear una reserva válida ----
    print("\n--- Operación 11: Crear una reserva válida ---")
    cliente = cliente_service.buscar_por_id(PRUEBA_CLIENTE_1)
    servicio = servicio_service.buscar_por_codigo(PRUEBA_SERVICIO_SALA)
    entrada = {
        "id_reserva": PRUEBA_RESERVA_1,
        "cliente": PRUEBA_CLIENTE_1,
        "servicio": PRUEBA_SERVICIO_SALA,
        "fecha": "2026-11-20",
        "duracion": 2,
    }
    try:
        reserva = reserva_service.registrar_reserva(
            id_reserva=PRUEBA_RESERVA_1, cliente=cliente, servicio=servicio,
            fecha="2026-11-20", duracion=2,
        )
        obtenido = (f"Reserva creada: {reserva.identificador}, "
                    f"estado={reserva.estado}, costo=${reserva.costo}")
        _registrar_resultado(
            11, "Crear una reserva válida", entrada,
            "Reserva registrada en estado PENDIENTE", obtenido, "EXITOSA",
        )
        registrar_reserva(PRUEBA_RESERVA_1, PRUEBA_CLIENTE_1, PRUEBA_SERVICIO_SALA, "creada")
    except Exception as exc:
        _registrar_resultado(
            11, "Crear una reserva válida", entrada,
            "Reserva registrada en estado PENDIENTE",
            f"Error: {exc}", "ERROR CONTROLADO", exc,
        )

    # ---- OPERACIÓN 12: Confirmar una reserva ----
    print("\n--- Operación 12: Confirmar una reserva ---")
    entrada = {"id_reserva": PRUEBA_RESERVA_1}
    try:
        reserva_service.confirmar_reserva(PRUEBA_RESERVA_1)
        reserva = reserva_service.consultar_reserva(PRUEBA_RESERVA_1)
        obtenido = f"Reserva {PRUEBA_RESERVA_1} confirmada, estado={reserva.estado}"
        _registrar_resultado(
            12, "Confirmar una reserva", entrada,
            "Reserva pasada a estado CONFIRMADA", obtenido, "EXITOSA",
        )
        registrar_confirmacion_reserva(PRUEBA_RESERVA_1)
    except Exception as exc:
        _registrar_resultado(
            12, "Confirmar una reserva", entrada,
            "Reserva pasada a estado CONFIRMADA",
            f"Error: {exc}", "ERROR CONTROLADO", exc,
        )

    # ---- OPERACIÓN 13: Crear una reserva sin cliente ----
    print("\n--- Operación 13: Reserva sin cliente ---")
    servicio = servicio_service.buscar_por_codigo(PRUEBA_SERVICIO_SALA)
    entrada = {"id_reserva": "RES-SIN-CLIENTE", "cliente": None,
               "servicio": PRUEBA_SERVICIO_SALA}
    try:
        reserva_service.registrar_reserva(
            id_reserva="RES-SIN-CLIENTE", cliente=None, servicio=servicio,
            fecha="2026-11-20", duracion=2,
        )
        obtenido = "No se lanzó excepción (fallo del escenario)"
        _registrar_resultado(
            13, "Crear reserva sin cliente", entrada,
            "Debe lanzar ParametroFaltanteError", obtenido, "ERROR CONTROLADO",
        )
    except ParametroFaltanteError as exc:
        obtenido = f"ParametroFaltanteError: {exc}"
        _registrar_resultado(
            13, "Crear reserva sin cliente", entrada,
            "Debe lanzar ParametroFaltanteError", obtenido, "ERROR CONTROLADO", exc,
        )
        registrar_error_validacion(str(exc))
        registrar_excepcion(exc)

    # ---- OPERACIÓN 14: Reservar un servicio no disponible ----
    print("\n--- Operación 14: Servicio no disponible ---")
    try:
        servicio_no_disp = servicio_service.registrar_servicio(
            tipo="asesoria", codigo="SRV-NODISP-001",
            nombre="Asesoría No Disponible", descripcion="Prueba",
            precio_base=50000, disponible=False,
            especialidad="Prueba", profesional_asignado="Nadie",
            duracion=1, tarifa_por_hora=40000,
        )
        cliente = cliente_service.buscar_por_id(PRUEBA_CLIENTE_2)
        try:
            reserva_service.registrar_reserva(
                id_reserva="RES-NODISP-001", cliente=cliente,
                servicio=servicio_no_disp, fecha="2026-11-21", duracion=1,
            )
            obtenido = "No se lanzó excepción (fallo del escenario)"
            _registrar_resultado(
                14, "Reservar servicio no disponible", entrada,
                "Debe lanzar ServicioNoDisponibleError", obtenido,
                "ERROR CONTROLADO",
            )
        except ServicioNoDisponibleError as exc:
            obtenido = f"ServicioNoDisponibleError: {exc}"
            _registrar_resultado(
                14, "Reservar servicio no disponible", entrada,
                "Debe lanzar ServicioNoDisponibleError", obtenido,
                "ERROR CONTROLADO", exc,
            )
            registrar_error_validacion(str(exc))
            registrar_excepcion(exc)
    except Exception as exc:
        _registrar_resultado(
            14, "Reservar servicio no disponible", entrada,
            "Debe lanzar ServicioNoDisponibleError",
            f"Error preparando servicio: {exc}", "ERROR CONTROLADO", exc,
        )

    # ---- OPERACIÓN 15: Cancelar una reserva finalizada ----
    print("\n--- Operación 15: Cancelar reserva finalizada ---")
    cliente = cliente_service.buscar_por_id(PRUEBA_CLIENTE_1)
    servicio = servicio_service.buscar_por_codigo(PRUEBA_SERVICIO_ASESORIA)
    try:
        reserva_service.registrar_reserva(
            id_reserva=PRUEBA_RESERVA_2, cliente=cliente, servicio=servicio,
            fecha="2026-11-21", duracion=1,
        )
        reserva_service.confirmar_reserva(PRUEBA_RESERVA_2)
        reserva_service.finalizar_reserva(PRUEBA_RESERVA_2)
        try:
            reserva_service.cancelar_reserva(PRUEBA_RESERVA_2)
            obtenido = "No se lanzó excepción (fallo del escenario)"
            _registrar_resultado(
                15, "Cancelar reserva finalizada",
                {"id_reserva": PRUEBA_RESERVA_2},
                "Debe lanzar OperacionNoPermitidaError", obtenido,
                "ERROR CONTROLADO",
            )
        except OperacionNoPermitidaError as exc:
            obtenido = f"OperacionNoPermitidaError: {exc}"
            _registrar_resultado(
                15, "Cancelar reserva finalizada",
                {"id_reserva": PRUEBA_RESERVA_2},
                "Debe lanzar OperacionNoPermitidaError", obtenido,
                "ERROR CONTROLADO", exc,
            )
            registrar_error_validacion(str(exc))
            registrar_excepcion(exc)
    except Exception as exc:
        _registrar_resultado(
            15, "Cancelar reserva finalizada",
            {"id_reserva": PRUEBA_RESERVA_2},
            "Debe lanzar OperacionNoPermitidaError",
            f"Error preparando reserva: {exc}", "ERROR CONTROLADO", exc,
        )

    # ---- OPERACIÓN 16: Cancelar correctamente una reserva pendiente ----
    print("\n--- Operación 16: Cancelar reserva pendiente/confirmada ---")
    cliente = cliente_service.buscar_por_id(PRUEBA_CLIENTE_2)
    servicio = servicio_service.buscar_por_codigo(PRUEBA_SERVICIO_EQUIPO)
    try:
        reserva_service.registrar_reserva(
            id_reserva=PRUEBA_RESERVA_3, cliente=cliente, servicio=servicio,
            fecha="2026-11-22", duracion=3,
        )
        reserva_service.cancelar_reserva(PRUEBA_RESERVA_3)
        reserva = reserva_service.consultar_reserva(PRUEBA_RESERVA_3)
        obtenido = f"Reserva {PRUEBA_RESERVA_3} cancelada, estado={reserva.estado}"
        _registrar_resultado(
            16, "Cancelar reserva pendiente",
            {"id_reserva": PRUEBA_RESERVA_3},
            "Reserva pasada a estado CANCELADA", obtenido, "EXITOSA",
        )
        registrar_cancelacion_reserva(PRUEBA_RESERVA_3)
    except Exception as exc:
        _registrar_resultado(
            16, "Cancelar reserva pendiente",
            {"id_reserva": PRUEBA_RESERVA_3},
            "Reserva pasada a estado CANCELADA",
            f"Error: {exc}", "ERROR CONTROLADO", exc,
        )

    # ---- OPERACIÓN 17: Excepción encadenada (raise ... from) ----
    print("\n--- Operación 17: Excepción encadenada ---")
    entrada = {"operacion": "calcular_costo_con_causa"}
    try:
        try:
            servicio = servicio_service.buscar_por_codigo("SRV-INEXISTENTE-ENCADENADO")
            if servicio is None:
                raise ParametroFaltanteError(
                    "Servicio no encontrado: SRV-INEXISTENTE-ENCADENADO"
                )
        except ParametroFaltanteError as causa:
            raise CalculoCostoError(
                "No se pudo calcular el costo porque el servicio no existe"
            ) from causa
    except CalculoCostoError as exc:
        obtenido = (f"CalculoCostoError encadenado: {exc} | "
                    f"Causa: {exc.__cause__}")
        _registrar_resultado(
            17, "Excepción encadenada (raise ... from)", entrada,
            "Debe preservar la causa original", obtenido, "EXITOSA",
        )
        registrar_excepcion(exc, causa_original=exc.__cause__)
        registrar_error_validacion(str(exc))

    # ---- OPERACIÓN 18: Continuidad del sistema tras un error ----
    print("\n--- Operación 18: Continuidad del sistema tras un error ---")
    entrada = {"operacion": "continuidad"}
    operacion_fallo = None
    try:
        cliente_service.buscar_por_identificacion("ID-INEXISTENTE-CONTINUIDAD")
    except Exception as exc:
        operacion_fallo = exc
        print(f"   Error controlado (no detiene el sistema): {exc}")
        registrar_error_validacion(str(exc))
        registrar_excepcion(exc)
    try:
        clientes = cliente_service.listar_clientes()
        obtenido = (
            f"El sistema continuó. Clientes registrados: {len(clientes)}. "
            f"Error previo manejado: "
            f"{type(operacion_fallo).__name__ if operacion_fallo else 'ninguno'}"
        )
        _registrar_resultado(
            18, "Continuidad del sistema tras un error", entrada,
            "El sistema sigue procesando operaciones independientes",
            obtenido, "EXITOSA",
        )
        registrar_advertencia(
            "Se demostró continuidad del programa tras un error controlado."
        )
    except Exception as exc:
        _registrar_resultado(
            18, "Continuidad del sistema tras un error", entrada,
            "El sistema sigue procesando",
            f"Error: {exc}", "ERROR CONTROLADO", exc,
        )

    _mostrar_resumen()
    input("\nPresione Enter para volver al menú principal...")
