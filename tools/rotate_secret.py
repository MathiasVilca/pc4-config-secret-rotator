import yaml
import argparse
import sys
SECRET_PATH="k8s/secret.yaml"
VALID_LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

class DoubleQuoted(str):
    """Clase personalizada para obligar a PyYAML a usar comillas dobles"""
    pass

def double_quoted_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

yaml.add_representer(DoubleQuoted, double_quoted_representer)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Herramienta de Rotación de Configuración")
    
    parser.add_argument("--api_key", type=str, help="Define el API_KEY")
    
    return parser.parse_args()

def new_config(config_dict):
    args=parse_arguments()
    #print(args)
    if args.api_key:
        config_dict["stringData"]["API_KEY"]=args.api_key
    pass

try:
    with open(SECRET_PATH,mode='r') as f:
        config_dict=yaml.safe_load(f) #Carga configuracion de configmap

    print("Secretos cargados correctamente, cargando nuevos secretos...")

    new_config(config_dict)
    if 'data' in config_dict:
            for key, value in config_dict['data'].items():
                config_dict['data'][key] = DoubleQuoted(value)
    with open(SECRET_PATH,mode='w') as f:
        yaml.dump(config_dict,f,default_flow_style=False, sort_keys=False)
    
    print("Cambios guardados correctamente")
    
    
except FileNotFoundError:
    # Esto se ejecuta si el archivo no se encuentra
    print(f"Error: No se encuentra el archivo en '{SECRET_PATH}'")
    sys.exit(1)

except Exception as e:
    print(f"Error desconocido: {e}")