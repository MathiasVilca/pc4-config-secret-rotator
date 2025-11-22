from fastapi import FastAPI
import os

app = FastAPI()

MIN_LENGTH_OFUSCATION = 6

@app.get("/")
def home():
    """
    Root del Config-Reader
    """
    return {"message": "Usted esta en el Config-Reader"}

@app.get("/health")
def health_check():
    """
    Si app esta viva, devuelve ok
    """
    return {"status": "ok"}

@app.get("/config")
def get_config():
    """
    Devuelve la configuración activa.
    Permite verificar si la rotación de ConfigMaps/Secrets funcionó.
    """

    #Obtencion de variables importantes (seran exportadas desde ConfigMap/Secret)
    app_mode = os.getenv("APP_MODE", "default")
    api_key = os.getenv("API_KEY", "default-api-key")

    #Nivel de detalle de los logs escritos por la app en consola
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    #Numero de intentos maximos para conectarse a un servicio externo luego de fallar
    try:
        max_retries = int(os.getenv("MAX_RETRIES", "3"))
        if(max_retries < 0):
            raise ValueError("MAX_RETRIES no puede ser negativo")
    except ValueError:
        max_retries = 5  # Fallback
        
    #Switch de backend, a que backend se conecta la app
    target_system = os.getenv("TARGET_SYSTEM", "legacy-db")

    #Ocultar secretos 
    if (len(api_key) < MIN_LENGTH_OFUSCATION):
        masked_key = "..."
    else:
        masked_key = api_key[:MIN_LENGTH_OFUSCATION//2] + "..." + api_key[-MIN_LENGTH_OFUSCATION//2:]

    return {
        "config":
        {
            "app_mode": app_mode,
            "log_level": log_level,
            "max_retries": max_retries,
            "target_system": target_system
        },
        "secrets":
        {
            "api_key_masked": masked_key
        },
        "meta":
        {
            "pod_name": os.getenv("HOSTNAME", "local")
        }
    }