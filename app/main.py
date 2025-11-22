from fastapi import FastAPI

app = FastAPI()


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
