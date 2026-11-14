"""
SOFTWARE FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas.

Punto de entrada de la aplicación de consola. Inicializa los servicios,
configura el registro de logs y presenta el menú principal al usuario.
"""

import sys
import traceback

from models.entidad import Entidad
from models.cliente import Cliente
from models.servicio import Servicio
from models.reserva_sala import ReservaSala
from models.alquiler_equipo import AlquilerEquipo
from models.asesoria import AsesoriaEspecializada
from models.reserva import Reserva

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

from services.cliente_service import ClienteService
from services.servicio_service import ServicioService
from services.reserva_service import ReservaService

from utils.logger import (
    configurar_logger,
    registrar_inicio_sistema,
    registrar_finalizacion_sistema,
    registrar_evento,
    registrar_advertencia,
    registrar_error_inesperado,
    registrar_excepcion,
    registrar_error_validacion,
)

from demo_operaciones import ejecutar_demostracion


# ---------------------------------------------------------------------------
# Instancias globales de los servicios de administración (capas de negocio)
# ---------------------------------------------------------------------------
cliente_service = ClienteService()
servicio_service = ServicioService()
reserva_service = ReservaService()


def mostrar_titulo():
    """Muestra el encabezado del sistema."""
    print("\n" + "=" * 60)
    print("           SOFTWARE FJ")
    print("  Sistema Integral de Gestión de Clientes, Servicios")
    print("                    y Reservas")
    print("=" * 60)


def pausa():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")


def leer_entero(mensaje, permitir_cero=False):
    """Lee un número entero del usuario con validación."""
    while True:
        try:
            valor = input(mensaje).strip()
            if valor == "":
                raise ParametroFaltanteError("Este campo es obligatorio.")
            return int(valor)
        except ValueError:
            print("Error: debe ingresar un número entero válido.")
        except ParametroFaltanteError as exc:
            print(f"Error: {exc}")


def leer_decimal(mensaje):
    """Lee un número decimal del usuario con validación."""
    while True:
        try:
            valor = input(mensaje).strip()
            if valor == "":
                raise ParametroFaltanteError("Este campo es obligatorio.")
            return float(valor)
        except ValueError:
            print("Error: debe ingresar un número decimal válido.")
        except ParametroFaltanteError as exc:
            print(f"Error: {exc}")


def leer_cadena(mensaje, obligatorio=True):
    """Lee una cadena de texto del usuario."""
    while True:
        valor = input(mensaje).strip()
        if obligatorio and valor == "":
            print("Error: este campo es obligatorio. No puede estar vacío.")
            continue
        return valor


# ---------------------------------------------------------------------------
# Módulo: Gestión de clientes
# ---------------------------------------------------------------------------
def menu_clientes():
    """Submenú de gestión de clientes."""
    while True:
        print("\n--- GESTIÓN DE CLIENTES ---")
        print("1. Registrar cliente")
        print("2. Buscar cliente por identificación")
        print("3. Listar todos los clientes")
        print("4. Actualizar cliente")
        print("5. Eliminar cliente")
        print("6. Volver al menú principal")
        opcion = leer_cadena("Seleccione una opción: ")

        if opcion == "1":
            _registrar_cliente_ui()
        elif opcion == "2":
            _buscar_cliente_ui()
        elif opcion == "3":
            _listar_clientes_ui()
        elif opcion == "4":
            _actualizar_cliente_ui()
        elif opcion == "5":
            _eliminar_cliente_ui()
        elif opcion == "6":
            break
        else:
            print("Opción no válida. Intente de nuevo.")


def _registrar_cliente_ui():
    print("\n-- Registro de cliente --")
    try:
        identificador = leer_cadena("Identificador interno: ")
        nombre = leer_cadena("Nombre completo: ")
        identificacion = leer_cadena("Número de identificación: ")
        correo = leer_cadena("Correo electrónico: ")
        telefono = leer_cadena("Teléfono: ")
        estado = leer_cadena("Estado (ACTIVO/INACTIVO) [ACTIVO]: ") or "ACTIVO"

        # try/except: captura específica y general de seguridad
        try:
            cliente = cliente_service.registrar_cliente(
                identificador=identificador,
                nombre_completo=nombre,
                numero_identificacion=identificacion,
                correo_electronico=correo,
                telefono=telefono,
                estado=estado,
            )
        except (ClienteInvalidoError, ClienteDuplicadoError, ParametroFaltanteError) as exc:
            print(f"Error de validación: {exc}")
            return
        except SoftwareFJError as exc:
            print(f"Error del sistema: {exc}")
            return
        except Exception as exc:  # captura general de seguridad en el límite
            print(f"Error inesperado: {exc}")
            registrar_error_inesperado(f"Error inesperado en UI cliente: {exc}")
            traceback.print_exc()
            return
        else:
            # try/except/else: se ejecuta solo si no hubo excepción
            print(f"Cliente registrado exitosamente: {cliente}")
        finally:
            # try/except/finally: finalización garantizada
            print("-- Fin del intento de registro de cliente --")

    except Exception as exc:
        print(f"Error inesperado: {exc}")


def _buscar_cliente_ui():
    print("\n-- Buscar cliente --")
    identificacion = leer_cadena("Número de identificación: ")
    try:
        cliente = cliente_service.buscar_por_identificacion(identificacion)
        if cliente is None:
            print("No se encontró ningún cliente con esa identificación.")
        else:
            print(cliente)
    except Exception as exc:
        print(f"Error: {exc}")


def _listar_clientes_ui():
    print("\n-- Listado de clientes --")
    clientes = cliente_service.listar_clientes()
    if not clientes:
        print("No hay clientes registrados.")
        return
    for c in clientes:
        print(c)


def _actualizar_cliente_ui():
    print("\n-- Actualizar cliente --")
    identificador = leer_cadena("Identificador del cliente a actualizar: ")
    print("Deje en blanco los campos que no desee modificar.")
    nombre = leer_cadena("Nuevo nombre completo (opcional): ", obligatorio=False)
    correo = leer_cadena("Nuevo correo (opcional): ", obligatorio=False)
    telefono = leer_cadena("Nuevo teléfono (opcional): ", obligatorio=False)
    estado = leer_cadena("Nuevo estado ACTIVO/INACTIVO (opcional): ", obligatorio=False)

    cambios = {}
    if nombre != "":
        cambios["nombre_completo"] = nombre
    if correo != "":
        cambios["correo_electronico"] = correo
    if telefono != "":
        cambios["telefono"] = telefono
    if estado != "":
        cambios["estado"] = estado

    if not cambios:
        print("No se proporcionaron cambios.")
        return
    try:
        cliente_service.actualizar_cliente(identificador, **cambios)
        print("Cliente actualizado exitosamente.")
    except (ParametroFaltanteError, ClienteInvalidoError) as exc:
        print(f"Error: {exc}")
    except Exception as exc:
        print(f"Error inesperado: {exc}")


def _eliminar_cliente_ui():
    print("\n-- Eliminar cliente --")
    identificador = leer_cadena("Identificador del cliente a eliminar: ")
    confirmar = leer_cadena("¿Está seguro? (S/N): ")
    if confirmar.upper() != "S":
        print("Operación cancelada.")
        return
    try:
        cliente_service.eliminar_cliente(identificador)
        print("Cliente eliminado exitosamente.")
    except ParametroFaltanteError as exc:
        print(f"Error: {exc}")
    except Exception as exc:
        print(f"Error inesperado: {exc}")


# ---------------------------------------------------------------------------
# Módulo: Gestión de servicios
# ---------------------------------------------------------------------------
def menu_servicios():
    """Submenú de gestión de servicios."""
    while True:
        print("\n--- GESTIÓN DE SERVICIOS ---")
        print("1. Registrar servicio de reserva de sala")
        print("2. Registrar servicio de alquiler de equipos")
        print("3. Registrar servicio de asesoría especializada")
        print("4. Consultar servicio por código")
        print("5. Listar todos los servicios")
        print("6. Cambiar disponibilidad de un servicio")
        print("7. Calcular costo de un servicio (polimorfismo)")
        print("8. Volver al menú principal")
        opcion = leer_cadena("Seleccione una opción: ")

        if opcion == "1":
            _registrar_sala_ui()
        elif opcion == "2":
            _registrar_equipo_ui()
        elif opcion == "3":
            _registrar_asesoria_ui()
        elif opcion == "4":
            _consultar_servicio_ui()
        elif opcion == "5":
            _listar_servicios_ui()
        elif opcion == "6":
            _cambiar_disponibilidad_ui()
        elif opcion == "7":
            _calcular_costo_ui()
        elif opcion == "8":
            break
        else:
            print("Opción no válida. Intente de nuevo.")


def _registrar_sala_ui():
    print("\n-- Registro de servicio: Reserva de sala --")
    try:
        codigo = leer_cadena("Código: ")
        nombre = leer_cadena("Nombre: ")
        descripcion = leer_cadena("Descripción: ")
        precio_base = leer_decimal("Precio base: ")
        capacidad = leer_entero("Capacidad: ")
        ubicacion = leer_cadena("Ubicación: ")
        duracion = leer_entero("Duración (horas): ")
        equipamiento = leer_cadena("Equipamiento: ")
        tarifa_por_hora = leer_decimal("Tarifa por hora: ")
        disponible = leer_cadena("¿Disponible? (S/N) [S]: ").upper() != "N"

        try:
            servicio = servicio_service.registrar_servicio(
                tipo="sala",
                codigo=codigo,
                nombre=nombre,
                descripcion=descripcion,
                precio_base=precio_base,
                disponible=disponible,
                capacidad=capacidad,
                ubicacion=ubicacion,
                duracion=duracion,
                equipamiento=equipamiento,
                tarifa_por_hora=tarifa_por_hora,
            )
        except (ServicioInvalidoError, ParametroFaltanteError) as exc:
            print(f"Error de validación: {exc}")
            return
        except SoftwareFJError as exc:
            print(f"Error del sistema: {exc}")
            return
        except Exception as exc:
            print(f"Error inesperado: {exc}")
            return
        else:
            print(f"Servicio registrado exitosamente: {servicio}")
    except Exception as exc:
        print(f"Error inesperado: {exc}")


def _registrar_equipo_ui():
    print("\n-- Registro de servicio: Alquiler de equipo --")
    try:
        codigo = leer_cadena("Código: ")
        nombre = leer_cadena("Nombre: ")
        descripcion = leer_cadena("Descripción: ")
        precio_base = leer_decimal("Precio base: ")
        nombre_equipo = leer_cadena("Nombre del equipo: ")
        cantidad_disponible = leer_entero("Cantidad disponible: ")
        precio_por_dia = leer_decimal("Precio por día: ")
        condiciones = leer_cadena("Condiciones de alquiler: ")
        disponible = leer_cadena("¿Disponible? (S/N) [S]: ").upper() != "N"

        try:
            servicio = servicio_service.registrar_servicio(
                tipo="equipo",
                codigo=codigo,
                nombre=nombre,
                descripcion=descripcion,
                precio_base=precio_base,
                disponible=disponible,
                nombre_equipo=nombre_equipo,
                cantidad_disponible=cantidad_disponible,
                precio_por_dia=precio_por_dia,
                condiciones_alquiler=condiciones,
            )
        except (ServicioInvalidoError, ParametroFaltanteError) as exc:
            print(f"Error de validación: {exc}")
            return
        except SoftwareFJError as exc:
            print(f"Error del sistema: {exc}")
            return
        except Exception as exc:
            print(f"Error inesperado: {exc}")
            return
        else:
            print(f"Servicio registrado exitosamente: {servicio}")
    except Exception as exc:
        print(f"Error inesperado: {exc}")


def _registrar_asesoria_ui():
    print("\n-- Registro de servicio: Asesoría especializada --")
    try:
        codigo = leer_cadena("Código: ")
        nombre = leer_cadena("Nombre: ")
        descripcion = leer_cadena("Descripción: ")
        precio_base = leer_decimal("Precio base: ")
        especialidad = leer_cadena("Especialidad: ")
        profesional = leer_cadena("Profesional asignado: ")
        duracion = leer_entero("Duración (horas): ")
        tarifa_por_hora = leer_decimal("Tarifa por hora: ")
        disponible = leer_cadena("¿Disponible? (S/N) [S]: ").upper() != "N"

        try:
            servicio = servicio_service.registrar_servicio(
                tipo="asesoria",
                codigo=codigo,
                nombre=nombre,
                descripcion=descripcion,
                precio_base=precio_base,
                disponible=disponible,
                especialidad=especialidad,
                profesional_asignado=profesional,
                duracion=duracion,
                tarifa_por_hora=tarifa_por_hora,
            )
        except (ServicioInvalidoError, ParametroFaltanteError) as exc:
            print(f"Error de validación: {exc}")
            return
        except SoftwareFJError as exc:
            print(f"Error del sistema: {exc}")
            return
        except Exception as exc:
            print(f"Error inesperado: {exc}")
            return
        else:
            print(f"Servicio registrado exitosamente: {servicio}")
    except Exception as exc:
        print(f"Error inesperado: {exc}")


def _consultar_servicio_ui():
    print("\n-- Consultar servicio --")
    codigo = leer_cadena("Código del servicio: ")
    try:
        servicio = servicio_service.consultar_servicio(codigo)
        print(servicio)
        print(servicio.describir_servicio())
    except ParametroFaltanteError as exc:
        print(f"Error: {exc}")
    except Exception as exc:
        print(f"Error inesperado: {exc}")


def _listar_servicios_ui():
    print("\n-- Listado de servicios --")
    servicios = servicio_service.listar_servicios()
    if not servicios:
        print("No hay servicios registrados.")
        return
    for s in servicios:
        print(s)


def _cambiar_disponibilidad_ui():
    print("\n-- Cambiar disponibilidad --")
    codigo = leer_cadena("Código del servicio: ")
    valor = leer_cadena("¿Disponible? (S/N): ").upper()
    disponible = valor == "S"
    try:
        servicio_service.cambiar_disponibilidad(codigo, disponible)
        print("Disponibilidad actualizada.")
    except ParametroFaltanteError as exc:
        print(f"Error: {exc}")
    except Exception as exc:
        print(f"Error inesperado: {exc}")


def _calcular_costo_ui():
    print("\n-- Calcular costo de servicio (polimorfismo) --")
    codigo = leer_cadena("Código del servicio: ")
    cantidad = leer_entero("Cantidad: ", permitir_cero=True)
    impuesto = leer_decimal("Impuesto (%): ")
    descuento = leer_decimal("Descuento (%): ")
    try:
        costo = servicio_service.calcular_costo(
            servicio_codigo=codigo, cantidad=cantidad,
            impuesto=impuesto, descuento=descuento,
        )
        print(f"Costo calculado: ${costo}")
    except (ParametroFaltanteError, CalculoCostoError) as exc:
        print(f"Error: {exc}")
    except Exception as exc:
        print(f"Error inesperado: {exc}")


# ---------------------------------------------------------------------------
# Módulo: Gestión de reservas
# ---------------------------------------------------------------------------
def menu_reservas():
    """Submenú de gestión de reservas."""
    while True:
        print("\n--- GESTIÓN DE RESERVAS ---")
        print("1. Registrar reserva")
        print("2. Consultar reserva")
        print("3. Listar todas las reservas")
        print("4. Confirmar reserva")
        print("5. Cancelar reserva")
        print("6. Finalizar reserva")
        print("7. Volver al menú principal")
        opcion = leer_cadena("Seleccione una opción: ")

        if opcion == "1":
            _registrar_reserva_ui()
        elif opcion == "2":
            _consultar_reserva_ui()
        elif opcion == "3":
            _listar_reservas_ui()
        elif opcion == "4":
            _confirmar_reserva_ui()
        elif opcion == "5":
            _cancelar_reserva_ui()
        elif opcion == "6":
            _finalizar_reserva_ui()
        elif opcion == "7":
            break
        else:
            print("Opción no válida. Intente de nuevo.")


def _registrar_reserva_ui():
    print("\n-- Registro de reserva --")
    id_reserva = leer_cadena("Identificador de reserva: ")
    id_cliente = leer_cadena("Identificador de cliente: ")
    id_servicio = leer_cadena("Código de servicio: ")
    fecha = leer_cadena("Fecha (YYYY-MM-DD): ")
    duracion = leer_entero("Duración (horas): ")

    cliente = cliente_service.buscar_por_id(id_cliente)
    servicio = servicio_service.buscar_por_codigo(id_servicio)

    if cliente is None:
        print("Error: no se encontró el cliente especificado.")
        return
    if servicio is None:
        print("Error: no se encontró el servicio especificado.")
        return

    try:
        reserva = reserva_service.registrar_reserva(
            id_reserva=id_reserva,
            cliente=cliente,
            servicio=servicio,
            fecha=fecha,
            duracion=duracion,
        )
        print(f"Reserva registrada exitosamente: {reserva}")
    except (ReservaInvalidaError, OperacionNoPermitidaError,
            ParametroFaltanteError, ServicioNoDisponibleError) as exc:
        print(f"Error: {exc}")
    except Exception as exc:
        print(f"Error inesperado: {exc}")


def _consultar_reserva_ui():
    print("\n-- Consultar reserva --")
    id_reserva = leer_cadena("Identificador de reserva: ")
    try:
        reserva = reserva_service.consultar_reserva(id_reserva)
        detalles = reserva.consultar_detalles()
        for clave, valor in detalles.items():
            print(f"{clave}: {valor}")
    except ReservaNoEncontradaError as exc:
        print(f"Error: {exc}")
    except Exception as exc:
        print(f"Error inesperado: {exc}")


def _listar_reservas_ui():
    print("\n-- Listado de reservas --")
    reservas = reserva_service.listar_reservas()
    if not reservas:
        print("No hay reservas registradas.")
        return
    for r in reservas:
        print(r)


def _confirmar_reserva_ui():
    print("\n-- Confirmar reserva --")
    id_reserva = leer_cadena("Identificador de reserva: ")
    try:
        reserva_service.confirmar_reserva(id_reserva)
        print("Reserva confirmada exitosamente.")
    except (ReservaNoEncontradaError, OperacionNoPermitidaError) as exc:
        print(f"Error: {exc}")
    except Exception as exc:
        print(f"Error inesperado: {exc}")


def _cancelar_reserva_ui():
    print("\n-- Cancelar reserva --")
    id_reserva = leer_cadena("Identificador de reserva: ")
    try:
        reserva_service.cancelar_reserva(id_reserva)
        print("Reserva cancelada exitosamente.")
    except (ReservaNoEncontradaError, OperacionNoPermitidaError) as exc:
        print(f"Error: {exc}")
    except Exception as exc:
        print(f"Error inesperado: {exc}")


def _finalizar_reserva_ui():
    print("\n-- Finalizar reserva --")
    id_reserva = leer_cadena("Identificador de reserva: ")
    try:
        reserva_service.finalizar_reserva(id_reserva)
        print("Reserva finalizada exitosamente.")
    except (ReservaNoEncontradaError, OperacionNoPermitidaError) as exc:
        print(f"Error: {exc}")
    except Exception as exc:
        print(f"Error inesperado: {exc}")


# ---------------------------------------------------------------------------
# Módulo: Consultar información
# ---------------------------------------------------------------------------
def menu_consultar_informacion():
    """Menú de consultas generales del sistema."""
    while True:
        print("\n--- CONSULTAR INFORMACIÓN ---")
        print("1. Clientes registrados")
        print("2. Servicios registrados")
        print("3. Reservas registradas")
        print("4. Reservas por estado")
        print("5. Volver al menú principal")
        opcion = leer_cadena("Seleccione una opción: ")

        if opcion == "1":
            _listar_clientes_ui()
        elif opcion == "2":
            _listar_servicios_ui()
        elif opcion == "3":
            _listar_reservas_ui()
        elif opcion == "4":
            estado = leer_cadena("Estado (PENDIENTE/CONFIRMADA/CANCELADA/FINALIZADA): ")
            reservas = reserva_service.reservas_por_estado(estado)
            if not reservas:
                print("No hay reservas con ese estado.")
            else:
                for r in reservas:
                    print(r)
        elif opcion == "5":
            break
        else:
            print("Opción no válida. Intente de nuevo.")


# ---------------------------------------------------------------------------
# Módulo: Estadísticas
# ---------------------------------------------------------------------------
def menu_estadisticas():
    """Muestra estadísticas del sistema."""
    print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
    print(f"Clientes registrados: {cliente_service.total_clientes()}")
    print(f"Servicios registrados: {servicio_service.total_servicios()}")
    print(f"Reservas registradas: {reserva_service.total_reservas()}")
    print("Reservas por estado:")
    for estado in Reserva.ESTADOS_PERMITIDOS:
        cantidad = len(reserva_service.reservas_por_estado(estado))
        print(f"  {estado}: {cantidad}")


# ---------------------------------------------------------------------------
# Módulo: Registro de eventos
# ---------------------------------------------------------------------------
def menu_registro_eventos():
    """Muestra el contenido del archivo de logs."""
    print("\n--- REGISTRO DE EVENTOS (LOGS) ---")
    import os
    from utils.logger import LOG_FILE
    if not os.path.exists(LOG_FILE):
        print("No existe aún un archivo de logs.")
        return
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
        if not lineas:
            print("El archivo de logs está vacío.")
            return
        print(f"Últimos {min(30, len(lineas))} registros:")
        for linea in lineas[-30:]:
            print(linea.rstrip())
    except Exception as exc:
        print(f"Error al leer el log: {exc}")


# ---------------------------------------------------------------------------
# Menú principal
# ---------------------------------------------------------------------------
def menu_principal():
    """Bucle del menú principal."""
    while True:
        mostrar_titulo()
        print("1. Gestión de clientes.")
        print("2. Gestión de servicios.")
        print("3. Gestión de reservas.")
        print("4. Consultar información.")
        print("5. Ejecutar demostración de operaciones.")
        print("6. Consultar estadísticas.")
        print("7. Consultar registro de eventos.")
        print("8. Salir.")
        opcion = leer_cadena("Seleccione una opción: ")

        if opcion == "1":
            menu_clientes()
        elif opcion == "2":
            menu_servicios()
        elif opcion == "3":
            menu_reservas()
        elif opcion == "4":
            menu_consultar_informacion()
        elif opcion == "5":
            ejecutar_demostracion(
                cliente_service, servicio_service, reserva_service
            )
        elif opcion == "6":
            menu_estadisticas()
        elif opcion == "7":
            menu_registro_eventos()
        elif opcion == "8":
            print("Saliendo del sistema SOFTWARE FJ. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


def main():
    """Función principal de entrada."""
    configurar_logger()
    registrar_inicio_sistema()
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nEjecución interrumpida por el usuario.")
    except Exception as exc:
        registrar_error_inesperado(f"Error crítico no controlado: {exc}")
        print(f"Error crítico: {exc}")
        traceback.print_exc()
    finally:
        registrar_finalizacion_sistema()


if __name__ == "__main__":
    main()
