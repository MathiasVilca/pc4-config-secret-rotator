## Issues:

### [S1_IX_01] Configuración Inicial del Repositorio
**Descripción:**
_Crear estructura de carpetas, `.gitignore` y documento `docs/vision.md`._

**Criterios:**
- Estructura creada según Proyecto 9 , repositorio limpio

### [S1_I1_01] Desarrollo de App "Config-Reader"
**Historia de Usuario:**
_"Como desarrollador, quiero crear la lógica en Python para leer variables de entorno y archivos montados, exponiéndolos en un endpoint JSON."_

**Criterios de Aceptación:**
- `app/main.py` implementado con Flask/FastAPI.
- Endpoint `GET /config` muestra las variables cargadas.
- Endpoint `GET /health` devuelve 200 OK.
- Gestión de errores si faltan las variables (valores por defecto).
- Crear al menos un test unitario simple (ej. verificar que la función de carga de configuración retorna valores por defecto si no hay env vars) y configurarlo en make test

### [S1_I2_01] Hardening de Imagen y Automatización (Makefile)
**Historia de Usuario:**
_"Como ingeniero DevOps, quiero un Dockerfile seguro y un Makefile estandarizado para construir la imagen localmente."_

**Criterios de Aceptación:**
- Dockerfile multi-stage usando `python:3.12-slim` (o alpine).
- Usuario no root configurado explícitamente en la imagen.
- Makefile funcional con targets: `setup`, `build` (con tags, no latest), scan (placeholder) .
- Documentación inicial en `docs/metrics.md`.
- Implementar el target make scan en el Makefile.

### [S1_I3_01] Infraestructura como Código (K8s Base)

**Historia de Usuario:**
_"Como ingeniero de plataforma, quiero definir los recursos de K8s para desplegar la app con configuraciones inyectadas."_

**Criterios de Aceptación:**
- `k8s/namespace.yaml` (ns: config-rotator).
- `k8s/configmap.yaml` y `k8s/secret.yaml` con datos de prueba .
- `k8s/deployment.yaml` configurado para inyectar el CM y el Secret como variables de entorno o volúmenes.
- `k8s/service.yaml` (ClusterIP o NodePort).

### [S1_I3_02] Scripts de Despliegue y Smoke Test

**Historia de Usuario:**
_"Como SRE, quiero scripts para aplicar los cambios en K8s y verificar rápidamente que la app responde."_

**Criterios de Aceptación:**
- `scripts/k8s-apply.sh`: Aplica `namespace` -> `config/secrets` -> `app`.
- `scripts/k8s-smoke.sh`: Hace `curl` al service para validar respuesta.
- Los scripts tienen encabezado `set -euo pipefail` y comentarios en español .

### [S1_IX_02] Integración y Documentación Final Sprint 1

**Historia de Usuario:**
_"Como equipo, queremos integrar todas las partes, grabar el video de evidencia y cerrar las métricas del sprint."_

**Criterios de Aceptación:**
- La imagen construida por B corre con los manifiestos de C y el código de A.
- `docs/metrics.md` completado con datos del sprint .
- Video de Cierre Sprint 1 grabado y subido (mostrar tablero y ejecución).