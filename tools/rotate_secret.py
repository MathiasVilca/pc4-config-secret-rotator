import yaml
import sys
from uuid import uuid4
import subprocess
SECRET_PATH="k8s/secret.yaml"

class DoubleQuoted(str):
    """Clase personalizada para obligar a PyYAML a usar comillas dobles"""
    pass

def double_quoted_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

yaml.add_representer(DoubleQuoted, double_quoted_representer)

def new_secret(config_dict):
    new_api_key=str(uuid4())
    config_dict["stringData"]["API_KEY"]=new_api_key
    pass   

try:
    with open(SECRET_PATH,mode='r') as f:
        config_dict=yaml.safe_load(f) #Carga configuracion de configmap
    print("Secretos cargados correctamente, generando nuevos secretos...")

    new_secret(config_dict)
    if 'stringData' in config_dict:
            for key, value in config_dict['stringData'].items():
                config_dict['stringData'][key] = DoubleQuoted(value)
    with open(SECRET_PATH,mode='w') as f:
        yaml.dump(config_dict,f,default_flow_style=False, sort_keys=False)
    
    print("Nuevos secretos guardados en archivo correctamente.")
    print("Aplicando cambios a kubernetes...")
    subprocess.run(["kubectl","apply","-f",SECRET_PATH],check=True)
    print("Cambios aplicados correctamente!")
    
    
except FileNotFoundError:
    # Esto se ejecuta si el archivo no se encuentra
    print(f"Error: No se encuentra el archivo en '{SECRET_PATH}'")
    sys.exit(1)

except subprocess.CalledProcessError:
    print("Error: Falló el comando 'kubectl'. Verifica que Minikube esté activo")
    sys.exit(1)

except Exception as e:
    print(f"Error desconocido: {e}")