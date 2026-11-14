# Arquitectura de Software – SOFTWARE FJ

## Visión general

El sistema sigue una arquitectura en capas, modular y orientada a objetos,
diseñada para ser fácil de comprender, mantener y extender. Cada capa tiene
una responsabilidad bien definida y las dependencias fluyen de la interfaz
hacia los servicios y los modelos de dominio.

## Capas del sistema

### 1. Capa de presentación (interfaz de consola)
Ubicada en `main.py`. Presenta el menú principal y los submenús, recibe la
entrada del usuario, valida entradas básicas y muestra los resultados. No
contiene lógica de negocio.

### 2. Capa de demostración
Ubicada en `demo_operaciones.py`. Ejecuta 18 escenarios reproducibles
(correctos y controlados) para evidenciar el funcionamiento del sistema,
incluyendo manejo de excepciones, continuidad ante errores y encadenamiento.

### 3. Capa de servicios (lógica de negocio)
Ubicada en `services/`. Contiene:
- `ClienteService`: registro, búsqueda, listado, actualización y eliminación
  de clientes; validación de duplicados.
- `ServicioService`: registro, consulta, listado, cambio de disponibilidad y
  cálculo de costos mediante polimorfismo.
- `ReservaService`: registro, consulta, listado, confirmación, cancelación y
  finalización de reservas; validación de disponibilidad.

### 4. Capa de modelos (dominio)
Ubicada en `models/`. Define las entidades del sistema:
- `Entidad` (abstracta): identificador y fecha de creación.
- `Cliente`: datos personales encapsulados con validaciones.
- `Servicio` (abstracta): precio, disponibilidad y métodos abstractos.
- `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`: servicios
  especializados con polimorfismo.
- `Reserva`: ciclo de vida de reservas con estados.

### 5. Capa de excepciones
Ubicada en `exceptions/excepciones_personalizadas.py`. Jerarquía de 10
excepciones personalizadas que heredan de `SoftwareFJError`.

### 6. Capa de utilidades
Ubicada en `utils/`:
- `logger.py`: sistema de registros con rotación de archivo.
- `validaciones.py`: funciones de validación reutilizables.

## Relaciones principales

- `Cliente`, `Servicio` y `Reserva` heredan de `Entidad`.
- `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` heredan de
  `Servicio`.
- `Reserva` agrega un `Cliente` y un `Servicio`.
- Los servicios de administración (`*Service`) gestionan listas internas de
  las entidades correspondientes.
- Las excepciones personalizadas se lanzan desde modelos y servicios y son
  capturadas en la interfaz y en la demostración.

## Patrón de polimorfismo

Las operaciones se realizan sobre referencias de tipo `Servicio` que invocan
las implementaciones específicas de `calcular_costo`,
`describir_servicio` y `validar_parametros` de cada subclase concreta.

## Almacenamiento

Todas las entidades se gestionan en memoria mediante listas internas. El
único archivo de persistencia operativa es `logs/software_fj.log`, usado
exclusivamente para el registro de eventos y errores. No se utilizan bases
de datos.
