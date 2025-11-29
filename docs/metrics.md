**Objetivo**: Definir métricas relevantes para el proyecto y documentar aspectos iniciales relacionados con la construcción de la imagen.

- **Tiempo de construcción (CI)**: tiempo promedio para `make build TAG=<version>` en el pipeline.
- **Tamaño de la imagen**: objetivo menor a 200MB comprimido (usar imágenes `slim`/alpine cuando sea viable).
- **Vulnerabilidades críticas**: número de vulnerabilidades de severidad CRITICAL/HIGH detectadas por escaneo (ej. `trivy`).

Notas sobre la imagen y el Makefile:

- Se añadió un `Dockerfile` multi-stage basado en `python:3.12-slim` y que crea un usuario no root `appuser`.
- El `Makefile` incorpora los targets `setup`, `test`, `build` y `scan`.
	- `make build TAG=v1.0.0` construye una imagen etiquetada (no usar `latest`).
	- `make scan` es un placeholder que usa `trivy` si está instalado; de lo contrario sugiere instalarlo.

# Métricas del Sprint 1

## 1. Resumen del Sprint
* **Estado:** Completado
* **Integrantes:** 3

## 2. Métricas de Proceso (Kanban)
| Métrica | Valor | Observación / Análisis |
| :--- | :--- | :--- |
| **Throughput** | **6 issues** | Al momento de la grabacion del video, se han completado 5 issues porque el ultimo issue incluye video |
| **Lead Time Promedio** | **12-13 horas** | A veces, se iniciaba en la noche y se terminaba en la mañana del dia siguiente, tambien considerar las otras responsabilidades de los integrantes |
| **WIP Máximo** | **3** | Se definió el maximo como 3 (un miembro del equipo trabajando en un issue a la vez), en la práctica, se llego a un máximo de 2 |
| **Builds** | **5 builds,3 fallidas** | Se descubrieron errores al construir, que tenian que ver con discrepancias en el nombre de la imagen docker y los puertos que usaba la app y el que estaba en el YAML, ultimas dos builds fueron exitosas |


## 3. Métricas de Propagación de Configuración (Sprint 2)
| Iteración | Tiempo (s) | Reinicio de Pod |
| :--- | :--- | :--- |
| 1 | 2.53 | Sí (Rolling Update) |
| 2 | 2.41 | Sí (Rolling Update) |
| 3 | 3.60 | Sí (Rolling Update) |
| 4 | 2.50 | Sí (Rolling Update) |
| 5 | 2.46 | Sí (Rolling Update) |

**Promedio**: 2.70 segundos

**Conclusiones**:
- La estrategia actual (Deployment con checksum) fuerza un reinicio de los pods.
- El tiempo promedio de propagación es de 2.70 segundos.
- Existe un breve tiempo de indisponibilidad o latencia durante el reinicio si no hay múltiples réplicas.

# Métricas del Sprint 1

## 1. Resumen del Sprint
* **Estado:** Completado
* **Integrantes:** 3

## 2. Métricas de Proceso (Kanban)
| Métrica | Valor | Observación / Análisis |
| :--- | :--- | :--- |
| **Throughput** | **7 issues** | Al momento de la grabacion del video, se han completado 5 issues porque el ultimo issue incluye video |
| **Lead Time Promedio** | **6-7 horas** | Los ultimos dias estuvo menos pesados, asi que pudimos enfocarnos mas |
| **WIP Máximo** | **3** | Se definió el maximo como 3 (un miembro del equipo trabajando en un issue a la vez), en la práctica, se llego a un máximo de 2 |
| **Builds** | **11 builds,9 fallidas** | Se descubrieron diversos errores al construir, en algunas versiones no funcionaban los scripts por un problema de terminadores de linea, otras por como funcionaba el tunnel, otras para corregir versiones de librerias que tenian vulnerabilidades |
| **Rotaciones por dia** | **15 rotaciones** | Invertidas en pruebas, revisiones |
| **Incidencias** | **10+** | Van desde fallo por el contexto que usaba docker, por librerias que no eran compatibles, scripts fallidos,... |
