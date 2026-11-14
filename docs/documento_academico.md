# Documento Académico – Fase 4 Programación UNAD (213023)

**Universidad:** Universidad Nacional Abierta y a Distancia (UNAD)  
**Vicerrectoría:** Vicerrectoría Académica y de Investigación  
**Curso:** Programación  
**Código:** 213023  
**Actividad:** Fase 4 – Componente práctico  
**Estudiante:** JHON DAVINSON HINESTROZA MURILLO  
**Proyecto:** Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ  
**Tutor:** [CAMPO POR COMPLETAR]  
**Grupo:** [CAMPO POR COMPLETAR]  
**Fecha:** noviembre de 2026  

---

## PORTADA

UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA – UNAD

Vicerrectoría Académica y de Investigación

Curso: Programación

Código: 213023

Fase 4 – Componente práctico

Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ

Presentado por: JHON DAVINSON HINESTROZA MURILLO

Tutor: [CAMPO POR COMPLETAR]

Grupo: [CAMPO POR COMPLETAR]

Fecha: noviembre de 2026.

---

## INTRODUCCIÓN

La presente actividad corresponde al componente práctico de la Fase 4 del
curso Programación (código 213023) de la Universidad Nacional Abierta y a
Distancia (UNAD). El contexto de la actividad consiste en el desarrollo de
un sistema integral orientado a objetos para una empresa ficticia denominada
SOFTWARE FJ, la cual ofrece tres categorías principales de servicios:
reservas de salas, alquiler de equipos y asesorías especializadas.

La programación orientada a objetos es un paradigma fundamental en la
ingeniería de software moderna, pues permite modelar problemas del mundo real
mediante entidades que encapsulan datos y comportamiento. La aplicación de
principios como la abstracción, la herencia, el polimorfismo y el
encapsulamiento facilita la construcción de sistemas modulares, extensibles y
mantenibles. En este proyecto se diseña una arquitectura donde cada entidad
del dominio (cliente, servicio, reserva) está representada por una clase, y
donde las relaciones entre estas entidades modelan los procesos de negocio de
la empresa.

El manejo de excepciones resulta indispensable en cualquier sistema de
gestión, dado que las operaciones pueden fallar por datos inválidos, registros
duplicados, servicios no disponibles o estados inconsistentes. Un manejo
adecuado de los errores permite que el sistema identifique, registre y gestione
las fallas sin interrumpir innecesariamente la ejecución, garantizando la
robustez y la continuidad del servicio. En este trabajo se implementan
excepciones personalizadas, bloques try/except, try/except/else,
try/exceptions/finally, encadenamiento de excepciones con raise ... from, y
propagación controlada de errores.

El sistema Software FJ permite gestionar clientes, servicios y reservas
utilizando exclusivamente estructuras de datos en memoria, objetos, listas y
archivos de registro (logs). Está expresamente prohibido el uso de motores de
bases de datos, por lo que la persistencia se limita al registro de eventos y
errores mediante un sistema de logs implementado con el módulo logging de
Python, incluyendo rotación de archivos.

Las tecnologías utilizadas son Python 3 (biblioteca estándar), el módulo
logging para los registros, el módulo abc para clases abstractas y unittest
para las pruebas automatizadas. No se requieren frameworks externos ni
servicios de almacenamiento externo.

El alcance del proyecto abarca el diseño e implementación de la arquitectura
orientada a objetos, la validación rigurosa de datos, las excepciones
personalizadas, el registro de errores, una interfaz de consola funcional, un
módulo de demostración con dieciocho escenarios, pruebas automatizadas y la
documentación académica y técnica completa.

---

## ENLACE DEL REPOSITORIO GITHUB

[PEGAR AQUÍ EL ENLACE DEL REPOSITORIO OFICIAL DEL GRUPO]

El estudiante debe copiar en este espacio el enlace real del repositorio
público o privado creado en GitHub, siguiendo la guía contenida en
docs/guia_github.md. Este campo debe diligenciarse antes de la entrega final;
no se debe inventar una URL.

---

## CONCLUSIONES

1. La aplicación de los principios de programación orientada a objetos (abstracción,
   herencia, polimorfismo y encapsulamiento) permitió construir una arquitectura
   modular donde clientes, servicios y reservas están claramente modelados y
   relacionados, facilitando la comprensión y extensión del sistema.

2. Las excepciones personalizadas resultaron esenciales para comunicar errores de
   negocio de forma clara y específica, diferenciando entre clientes inválidos,
   servicios no disponibles, reservas no permitidas y fallas en el cálculo de
   costos, sin mezclar errores de validación con errores inesperados del sistema.

3. El registro de errores mediante el módulo logging de Python, con rotación de
   archivos y niveles DEBUG, INFO, WARNING, ERROR y CRITICAL, brinda trazabilidad
   de todos los eventos y errores del sistema, lo cual es fundamental para el
   mantenimiento y la auditoría del software.

4. Los resultados de las pruebas automatizadas (74 pruebas, todas aprobadas)
   evidencian que el sistema cumple los requisitos funcionales obligatorios,
   incluyendo clases abstractas, validaciones, polimorfismo, cálculos de costo,
   estados de reserva, excepciones personalizadas, encadenamiento y continuidad
   ante errores.

5. Durante el desarrollo se aprendió a simular la sobrecarga de métodos en
   Python mediante parámetros opcionales con valores predeterminados, a aplicar
   encadenamiento de excepciones para conservar la causa original de un error, y
   a garantizar que un error en una operación no detenga el procesamiento de
   operaciones independientes.

---

## REFERENCIAS BIBLIOGRÁFICAS

Van Rossum, G., & Drake, F. L. (2024). *El tutorial de Python*. Python Software
Foundation. https://docs.python.org/es/3.12/tutorial/errors.html

Cuevas Álvarez, A. (2016). *Python 3: curso práctico*. RA-MA Editorial.

Zambrano, J. P. (2025). *Introducción al uso de GitHub* [Objeto virtual de
información]. Repositorio Institucional UNAD.
https://repository.unad.edu.co/handle/10596/75876

Silva, F. D. (2025). *Basics of using GitHub* [Objeto virtual de información].
Repositorio Institucional UNAD.
https://repository.unad.edu.co/handle/10596/75882

Romano, F., Baka, B., & Phillips, D. (2019). *Getting Started with Python:
Understand Key Data Structures and Use Python in Object-oriented Programming*.
Packt Publishing.
