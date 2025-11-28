
Los issues se dividieron la siguiente manera:  
- **Integrante 1 (App Developer):** Se encarga de la carpeta `app/` y la lógica de lectura de configs.
- **Integrante 2 (DevOps & Container):** Se encarga de Dockerfile, Makefile y `docs/`.
- **Integrante 3 (Cloud Engineer / K8s):** Se encarga de `k8s/` y los scripts de despliegue en `scripts/`.

En caso alguno necesite ayuda de otro, se mostrará en la sección de responsables

Video: https://drive.google.com/drive/folders/13nDrEWGKe7c7yv9Cl8mCa7CKhaBxXFba

## Issues:

### [S2_I1_01] Desarrollo de Herramientas de Rotación (Python)
**Historia de Usuario:**
_"Como SRE, quiero scripts en Python que generen nuevas configuraciones y secretos aleatorios para automatizar el cambio de credenciales sin intervención manual."_

**Criterios de Aceptación:**

- [x] Implementar `tools/rotate_config.py` que modifique `configmap.yaml` (ej. cambiar `APP_MODE`, `LOG_LEVEL`, etc).
- [x] Implementar `tools/rotate_secret.py` que genere un nuevo secreto aleatorio (ej. UUID o Hash) en `secret.yaml`.
- [x] Los scripts deben guardar los cambios en los archivos YAML locales.
- [x] Los scripts deben aplicar los cambios al clúster automáticamente usando subprocess para llamar a `kubectl apply -f ...` .

**Responsable(s):** Mathias Vilca

### [S2_I1_02] Actualizar documentos de repositorio
**Historia de Usuario:**
_Como equipo, queremos tener los documentos claros para facilitar la revisión_
**Criterios de Aceptación:**
- [x] Actualizar `docs/risk_register.md` con ciertos riesgos ya mitigados.
- [ ] Redactar `docs/sprint_backlog_sprint2.md` con informacion del segundo sprint

**Responsable(s):** Mathias Vilca

### [S2_I2_01] Orquestación de Rotación y Pruebas
**Historia de Usuario:**

_"Como DevOps, quiero scripts Bash que unan la generación de secretos con la validación inmediata para confirmar que el sistema sigue funcionando tras la rotación."_

**Criterios de Aceptación:**

- [ ] Crear script `scripts/k8s-rotate-config.sh` que orqueste el flujo completo de configuración.
- [ ] Crear script `scripts/k8s-rotate-secret.sh` que orqueste el flujo completo de secretos.
- [ ] Los scripts Bash deben llamar primero a las herramientas Python (`tools/rotate_*.py`).
- [ ] Inmediatamente después, deben ejecutar `scripts/k8s-smoke.sh` para validar el endpoint `/config` y confirmar el cambio.

**Responsable(s):** Dery Gonzales Cruz

### [S2_I3_01] Estrategias de Actualización en K8s
**Historia de Usuario:**
_"Como Operador, quiero controlar cómo Kubernetes aplica los cambios (rolling update vs recreate) para asegurar que los Pods tomen la nueva configuración."_

**Criterios de Aceptación:**

- [ ] Modificar `k8s/deployment.yaml` para definir la estrategia de actualización.
- [ ] Investigar e implementar el patrón de "Checksum Annotations" (o similar) para forzar el reinicio del Pod cuando cambie el ConfigMap/Secret.
- [ ] Configurar correctamente `envFrom` para la inyección de variables.
- [ ] Verificar que al aplicar un cambio en el ConfigMap, Kubernetes inicie el proceso de Rollout del nuevo Pod.

**Responsable(s):** Christian Hermoza

### [S2_I3_02] Ejecución de Experimentos y Métricas
**Historia de Usuario:**
_"Como SRE, quiero medir cuánto tarda un cambio de config en ser visible en la app para establecer una línea base de rendimiento y seguridad."_
**Criterios de Aceptación:**
- [ ] Realizar al menos 5 rotaciones para obtener un tiempo promedio confiable..
- [ ] Registrar en `docs/metrics.md`: ¿Se reinició el pod automáticamente? (Sí/No).
- [ ] Registrar en `docs/metrics.md`: Tiempo de propagación en segundos (desde el `apply` hasta que `/config` cambia).
- [ ] Registrar en `docs/metrics.md`: Tasa de error (si hubo downtime o errores 500).
- [ ] Redactar conclusiones breves sobre los hallazgos en el mismo documento.

**Responsable(s):** Christian Hermoza

### [S2_IX_01] Video de Cierre y Entrega Final

**Historia de Usuario:**
`"Como equipo, queremos demostrar la capacidad de rotación segura y entregar el proyecto final cumpliendo con todos los requisitos del curso."`
**Criterios de Aceptación:**
- [ ] Grabar Video 2 (duración 7-10 min).
- [ ] Mostrar en el video: Evolución del tablero Kanban (Backlog -> Done).
- [ ] Demostración técnica: Ejecutar `make rotate-config` (o el script bash) y mostrar en vivo cómo cambia el valor en el navegador.
- [ ] Explicación de las métricas de seguridad obtenidas.
- [ ] Repositorio limpio, con `README.md` actualizado y código comentado en español.

**Responsable(s):** Todo el equipo