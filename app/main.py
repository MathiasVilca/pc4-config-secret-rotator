from fastapi import FastAPI
import os
import uvicorn

app = FastAPI()

DEFAULT_CONFIG = {
    "APP_MODE": "default",
    "LOG_LEVEL": "INFO",
    "MAX_RETRIES": 3,
    "TARGET_SYSTEM": "legacy-db",
    "API_KEY": "sin-secreto"
}
MIN_LENGTH_OFUSCATION = 6
VALID_LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

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
    app_mode = os.getenv("APP_MODE", DEFAULT_CONFIG["APP_MODE"])
    api_key = os.getenv("API_KEY", DEFAULT_CONFIG["API_KEY"])

    #Nivel de detalle de los logs escritos por la app en consola (restringido)
    raw_log_level = os.getenv("LOG_LEVEL", DEFAULT_CONFIG["LOG_LEVEL"]).upper()

    if raw_log_level in VALID_LOG_LEVELS:
        log_level = raw_log_level
        log_status = "Valid"
    else:
        #Se avisa del error
        log_level = "INFO" 
        log_status = f"Invalid value '{raw_log_level}' ignored. Using default."
    
    #Numero de intentos maximos para conectarse a un servicio externo luego de fallar
    try:
        max_retries = int(os.getenv("MAX_RETRIES", DEFAULT_CONFIG["MAX_RETRIES"]))
        if(max_retries < 0):
            raise ValueError("MAX_RETRIES no puede ser negativo")
    except ValueError:
        max_retries = 5  #si es invalido, se carga default
        
    #Switch de backend, a que backend se conecta la app
    target_system = os.getenv("TARGET_SYSTEM", DEFAULT_CONFIG["TARGET_SYSTEM"])

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
            "log_status": log_status,
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

if __name__ == "__main__":
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)