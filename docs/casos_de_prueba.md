# Casos de Prueba – SOFTWARE FJ

## Resumen

Se ejecutaron 74 pruebas automatizadas con el módulo `unittest` de Python,
distribuidas en cuatro archivos de prueba. Todas las pruebas fueron
ejecutadas realmente y aprobadas.

## Archivos de prueba

| Archivo | Descripción |
|---------|-------------|
| `tests/test_clientes.py` | Clase abstracta Entidad, validaciones de clientes, duplicados, encapsulamiento. |
| `tests/test_servicios.py` | Clase abstracta Servicio, validaciones, polimorfismo, cálculos de costo, impuestos y descuentos. |
| `tests/test_reservas.py` | Creación, confirmación, cancelación, estados no permitidos, reservas por servicio. |
| `tests/test_excepciones.py` | Jerarquía de excepciones, try/except/else/finally, encadenamiento, continuidad, logs. |

## Requerimientos funcionales cubiertos

| Requisito | Pruebas asociadas | Estado |
|-----------|-------------------|--------|
| Clase abstracta Entidad | `test_entidad_no_se_puede_instanciar` | Aprobada |
| Clase abstracta Servicio | `test_servicio_no_se_puede_instanciar` | Aprobada |
| Validaciones de clientes | `test_nombre_vacio`, `test_correo_invalido`, `test_identificacion_invalida`, `test_telefono_invalido` | Aprobadas |
| Clientes duplicados | `test_registrar_cliente_duplicado_lanza_excepcion` | Aprobada |
| Validaciones de servicios | `test_servicio_con_precio_negativo`, `test_servicio_sin_nombre` | Aprobadas |
| Polimorfismo | `test_calcular_costo_polimorfico`, `test_describir_servicio_polimorfico` | Aprobadas |
| Cálculos de costos | `test_costo_basico_*`, `test_costo_con_impuesto`, `test_costo_con_descuento` | Aprobadas |
| Impuestos y descuentos | `test_costo_con_impuesto_y_descuento`, `test_descuento_mayor_a_100_lanza_excepcion` | Aprobadas |
| Creación de reservas | `test_crear_reserva_valida` | Aprobada |
| Confirmación de reservas | `test_confirmar_reserva_pasada_a_confirmada` | Aprobada |
| Cancelaciones | `test_cancelar_reserva_pasada_a_cancelada` | Aprobada |
| Estados no permitidos | `test_cancelar_reserva_finalizada_no_permitido`, etc. | Aprobadas |
| Excepciones personalizadas | Jerarquía y mensajes | Aprobadas |
| Encadenamiento de excepciones | `test_excepcion_encadenada_conserva_causa` | Aprobada |
| Registro de logs | `TestRegistroLogs` | Aprobadas |
| Continuidad ante errores | `TestContinuidadPrograma` | Aprobadas |

## Resultados

- Total de pruebas: 74
- Pruebas aprobadas: 74
- Pruebas fallidas: 0
- Cobertura: todos los requisitos funcionales obligatorios están cubiertos.

## Reproducibilidad

Las pruebas son independientes, utilizan datos aislados en cada prueba y no
dependen de un orden de ejecución específico. Se ejecutan con:

```
python -m unittest discover -s tests -v
```
