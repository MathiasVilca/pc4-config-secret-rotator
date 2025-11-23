**Objetivo**: Definir métricas relevantes para el proyecto y documentar aspectos iniciales relacionados con la construcción de la imagen.

- **Tiempo de construcción (CI)**: tiempo promedio para `make build TAG=<version>` en el pipeline.
- **Tamaño de la imagen**: objetivo menor a 200MB comprimido (usar imágenes `slim`/alpine cuando sea viable).
- **Vulnerabilidades críticas**: número de vulnerabilidades de severidad CRITICAL/HIGH detectadas por escaneo (ej. `trivy`).

Notas sobre la imagen y el Makefile:

- Se añadió un `Dockerfile` multi-stage basado en `python:3.12-slim` y que crea un usuario no root `appuser`.
- El `Makefile` incorpora los targets `setup`, `test`, `build` y `scan`.
	- `make build TAG=v1.0.0` construye una imagen etiquetada (no usar `latest`).
	- `make scan` es un placeholder que usa `trivy` si está instalado; de lo contrario sugiere instalarlo.


