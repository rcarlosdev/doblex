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
    
    print("Iniciando Doblex SMU Backend (FastAPI) en http://127.0.0.1:8000 ...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
