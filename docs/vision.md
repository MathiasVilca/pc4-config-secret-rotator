# Visión del Proyecto: Config & Secret Rotator en Kubernetes

## 1. Contexto
En este proyecto, se simula un escenario en el cual un equipo SRE (Site reliability engineers, o ingenieros de confiabilidad de sitio) debe practicar la rotación de configuración y secretos (cambiar o reemplazar estos) en un cluster local (Minikube) y ver como reaccionan los pods.  

## 2. Problema que resuelve
Por lo general, las apps tradicionales leen la configuración al inicio, lo cual puede ser un problema si se cambia alguna configuración importante o se vulnera algun secreto. En este caso, se tendría que reiniciar o redesplegar los pods para que usen los nuevos valores, lo cual es lento y repetitivo.  
  
Este proyecto busca resolver este problema, al crear una herramienta (el rotator) que pueda realizar estos rotaciones de valores y verificar su correcta propagación por la apliacación sin detener el servicio.

## 3. Objetivos Técnicos
- **App observable:** Se crea una app la cual exponga sus variables de configuración actuales via un endpoint `/config` para su verificación en tiempo real.
- **Infraestructura Resiliente:** Desplegar recursos en Kubernetes (Deployment, Service, ConfigMap, Secret) configurando correctamente sondeos de Liveness y Readiness (via Probes) para detectar fallos durante las rotaciones/actualizaciones.
- **Automatización de Rotacion:** Implementar scripts en Python (`rotate_config.py`, `rotate_secret.py`) y Bash capaces de cambiar los valores de configuracion y las apliquen al clúster automáticamente, sin necesidad de reinicios.
- **Pruebas de Humo:** Crear scripts de validación (`k8s-smoke.sh`) que confirmen si los nuevos valores están activos.

## 4. Objetivos de aprendizaje
- Comprender la mecánica de inyección de configuraciones en Kubernetes (configuración y seretos).
- Practicar la automatización de tareas de Kubernetes (kubectl) utilizando scripts externos (Python/Bash).
- Analizar el comportamiento de los Pods (reinicios, tiempos de propagación) ante cambios en los recursos montados.
- Aplicar principios de seguridad (Ej. No usar Root en contenedores y mínimo privilegio en la gestión de secretos).