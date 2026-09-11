import os
import sys
import subprocess

# Auto-detección y uso obligatorio del entorno virtual local (.venv)
current_dir = os.path.dirname(os.path.abspath(__file__))
venv_python = os.path.join(current_dir, ".venv", "Scripts", "python.exe")

if os.path.exists(venv_python) and os.path.abspath(sys.executable).lower() != os.path.abspath(venv_python).lower():
    print(f"[AUTO-VENV] Activando entorno virtual local: {venv_python}")
    result = subprocess.call([venv_python] + sys.argv)
    sys.exit(result)

import uvicorn

if __name__ == "__main__":
    # Asegurar que el directorio raíz del backend esté en sys.path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    # Solo activar reload en desarrollo si no hay variable PORT fijada por la plataforma cloud
    is_dev = os.getenv("PORT") is None and os.getenv("ENV", "development").lower() != "production"

    print(f"Iniciando Doblex SMU Backend (FastAPI) en http://{host}:{port} ...")
    uvicorn.run("app.main:app", host=host, port=port, reload=is_dev)
