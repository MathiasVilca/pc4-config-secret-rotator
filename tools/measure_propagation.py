import time
import subprocess
import requests
import yaml
import os
import signal

CONFIGMAP_PATH = "k8s/configmap.yaml"
URL = "http://localhost:8000/config"
ITERATIONS = 5

def start_port_forward():
    print("Iniciando port-forward...")
    # Kill any existing port-forward on 8000
    subprocess.run(["pkill", "-f", "kubectl port-forward.*8000"], check=False)
    
    proc = subprocess.Popen(
        ["kubectl", "port-forward", "svc/config-rotator-service", "-n", "config-rotator", "8000:80"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2) # Wait for it to be ready
    return proc

def update_configmap(mode_value):
    with open(CONFIGMAP_PATH, 'r') as f:
        config = yaml.safe_load(f)
    
    config['data']['APP_MODE'] = mode_value
    
    # Ensure values are strings
    for k, v in config['data'].items():
        config['data'][k] = str(v)

    with open(CONFIGMAP_PATH, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

def wait_for_config_update(target_mode):
    start_time = time.time()
    while True:
        try:
            response = requests.get(URL, timeout=2)
            if response.status_code == 200:
                data = response.json()
                current_mode = data.get("config", {}).get("app_mode")
                if current_mode == target_mode:
                    return time.time() - start_time
                else:
                    print(f"  Esperando... Actual: {current_mode}, Esperado: {target_mode}")
            else:
                print(f"  Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"  Error conectando: {e}")
        
        if time.time() - start_time > 120: # Timeout 2 mins
            raise TimeoutError("Timeout esperando actualizacion de config")
        time.sleep(1)

def main():
    pf_process = None
    results = []

    try:
        for i in range(1, ITERATIONS + 1):
            target_mode = f"measurement-run-{i}"
            print(f"\n--- Iteración {i}/{ITERATIONS}: Cambiando APP_MODE a '{target_mode}' ---")
            
            # 1. Update ConfigMap file
            update_configmap(target_mode)
            
            # 2. Apply changes (make deploy)
            start_time = time.time()
            print("Ejecutando make deploy...")
            subprocess.run(["make", "deploy"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            deploy_done_time = time.time()
            
            # Restart port-forward to ensure connection to new pods
            if pf_process:
                pf_process.terminate()
            pf_process = start_port_forward()

            # 3. Wait for propagation
            print("Esperando propagación...")
            propagation_time = wait_for_config_update(target_mode)
            
            # Total time
            total_time = (deploy_done_time - start_time) + propagation_time
            
            print(f"Detectado! Tiempo total: {total_time:.2f}s")
            results.append(total_time)
            
            # Wait a bit before next run
            time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("\nLimpiando...")
        if pf_process:
            pf_process.terminate()
        # Restore config
        update_configmap("default")
        subprocess.run(["make", "deploy"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if results:
        avg_time = sum(results) / len(results)
        print(f"\nResultados ({len(results)} iteraciones):")
        print(f"Tiempos: {[round(t, 2) for t in results]}")
        print(f"Promedio: {avg_time:.2f} segundos")
        
        # Write to metrics.md (append)
        with open("docs/metrics.md", "a") as f:
            f.write("\n## 3. Métricas de Propagación de Configuración (Sprint 2)\n")
            f.write("| Iteración | Tiempo (s) | Reinicio de Pod |\n")
            f.write("| :--- | :--- | :--- |\n")
            for idx, t in enumerate(results):
                f.write(f"| {idx+1} | {t:.2f} | Sí (Rolling Update) |\n")
            f.write(f"\n**Promedio**: {avg_time:.2f} segundos\n")
            f.write("\n**Conclusiones**:\n")
            f.write("- La estrategia actual (Deployment con checksum) fuerza un reinicio de los pods.\n")
            f.write(f"- El tiempo promedio de propagación es de {avg_time:.2f} segundos.\n")
            f.write("- Existe un breve tiempo de indisponibilidad o latencia durante el reinicio si no hay múltiples réplicas.\n")

if __name__ == "__main__":
    main()
