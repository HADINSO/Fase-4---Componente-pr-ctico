# Guía de Publicación en GitHub – SOFTWARE FJ

Este documento instruye al estudiante (y al grupo) sobre cómo publicar el
proyecto en un repositorio GitHub. **No se inventan enlaces ni credenciales.**
El estudiante debe completar los campos que correspondan con su información
real.

## Paso 1: Crear una cuenta o ingresar a GitHub

Ingrese a https://github.com y inicie sesión con su cuenta personal. Si no
tiene cuenta, créela siguiendo el proceso de registro de GitHub.

**No solicite ni comparta contraseñas, tokens ni credenciales de GitHub.**

## Paso 2: Crear un repositorio

1. En GitHub, haga clic en el icono "+" (arriba a la derecha) y seleccione
   "New repository".
2. Nombre del repositorio: `Software-FJ-Fase-4-Programacion` (o el nombre
   acordado por el grupo).
3. Elija público o privado según lo acordado por el grupo.
4. No inicialice con README, .gitignore ni licencia (el proyecto ya los
   incluye).
5. Haga clic en "Create repository".
6. Copie el enlace del repositorio (por ejemplo:
   `https://github.com/USUARIO/Software-FJ-Fase-4-Programacion.git`).

## Paso 3: Preparar el proyecto localmente

Abra una terminal de comandos en la carpeta del proyecto:

```cmd
cd ENTREGA_FASE_4_JHON_DAVINSON_HINESTROZA\SOFTWARE_FJ
```

## Paso 4: Inicializar Git

```cmd
git init
```

## Paso 5: Añadir los archivos

```cmd
git add .
```

## Paso 6: Crear el primer commit

```cmd
git commit -m "Commit inicial: Fase 4 Programacion UNAD - SOFTWARE FJ"
```

**Nota:** El estudiante debe usar su propia identidad de Git (`git config
--global user.name` y `user.email`). No se inventan autores ni fechas.

## Paso 7: Configurar el repositorio remoto

Sustituya `ENLACE-DEL-REPOSITORIO` por el enlace real copiado en el Paso 2:

```cmd
git remote add origin ENLACE-DEL-REPOSITORIO
```

## Paso 8: Realizar push

```cmd
git branch -M main
git push -u origin main
```

## Paso 9: Verificar los archivos publicados

Ingrese al repositorio en GitHub y verifique que aparezcan todos los
archivos: código fuente, pruebas, documentación, README, .gitignore y la
carpeta logs.

## Paso 10: Copiar el enlace del repositorio

Copie el enlace final del repositorio y péguelo en el documento académico,
en la sección "Enlace del repositorio GitHub", y en el informe final.

## Importante sobre el trabajo colaborativo

- No invente commits, autores, fechas ni contribuciones de otros
  integrantes.
- No atribuya a JHON DAVINSON HINESTROZA MURILLO aportaciones realizadas
  por otras personas.
- El estudiante debe integrar sus cambios reales en el repositorio oficial
  del grupo y participar en las actividades colaborativas.
- Si no tiene acceso al repositorio grupal, deje el proyecto completamente
  preparado para integrarlo posteriormente.

## Datos pendientes por diligenciar (estudiante)

- [ ] Enlace del repositorio oficial del grupo.
- [ ] Nombre del tutor.
- [ ] Número de grupo.
- [ ] Verificación de aportes colaborativos.
- [ ] Subida del PDF académico al campus de la UNAD.
