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

