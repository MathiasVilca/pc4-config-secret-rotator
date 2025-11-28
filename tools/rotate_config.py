import yaml
import argparse
import subprocess
import sys
CONFIGMAP_PATH="k8s/configmap.yaml"
VALID_LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

class DoubleQuoted(str):
    """Clase personalizada para obligar a PyYAML a usar comillas dobles"""
    pass

def double_quoted_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

yaml.add_representer(DoubleQuoted, double_quoted_representer)
def positive_int(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' no es un número entero válido.")
    
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"'{value}' debe ser un entero positivo mayor a 0.")
    
    return ivalue

def parse_arguments():
    parser = argparse.ArgumentParser(description="Herramienta de Rotación de Configuración")
    
    parser.add_argument("--app_mode", type=str, help="Define el APP_MODE")
    parser.add_argument("--log_level", type=str, choices=VALID_LOG_LEVELS, help="Define el LOG_LEVEL")
    parser.add_argument("--max_retries", type=positive_int, help="Define MAX_RETRIES (>0)")
    parser.add_argument("--target_system", type=str, help="Define TARGET_SYSTEM")
    
    return parser.parse_args()

def new_config(config_dict):
    args=parse_arguments()
    #print(args)
    if args.app_mode:
        config_dict["data"]["APP_MODE"]=str(args.app_mode)
    if args.log_level:
        config_dict["data"]["LOG_LEVEL"]=args.log_level
    if args.max_retries:
        config_dict["data"]["MAX_RETRIES"]=str(args.max_retries)
    if args.target_system:
        config_dict["data"]["TARGET_SYSTEM"]=args.target_system
    pass

try:
    with open(CONFIGMAP_PATH,mode='r') as f:
        config_dict=yaml.safe_load(f) #Carga configuracion de configmap

    print("Datos cargados correctamente, Guardando nueva configuración en archivo...")

    new_config(config_dict)
    if 'data' in config_dict:
            for key, value in config_dict['data'].items():
                config_dict['data'][key] = DoubleQuoted(value)
    with open(CONFIGMAP_PATH,mode='w') as f:
        yaml.dump(config_dict,f,default_flow_style=False, sort_keys=False)
    
    print("Cambios guardados en archivo correctamente.")
    print("Aplicando cambios a kubernetes...")

    subprocess.run(["kubectl","apply","-f",CONFIGMAP_PATH],check=True)

    print("Cambios aplicados correctamente!")
    
    
except FileNotFoundError:
    # Esto se ejecuta si el archivo no se encuentra
    print(f"Error: No se encuentra el archivo en '{CONFIGMAP_PATH}'")
    sys.exit(1)

except subprocess.CalledProcessError:
    print("Error: Falló el comando 'kubectl'. Verifica que Minikube esté activo")
    sys.exit(1)

except Exception as e:
    print(f"Error desconocido: {e}")