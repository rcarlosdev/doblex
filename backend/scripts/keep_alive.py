"""
Script local de Keep-Alive para mantener despierto el backend en PandaStack.
Realiza un ping HTTP periodico al endpoint de salud (/health) para evitar que
la plataforma suspenda el contenedor por inactividad.

Uso:
    python scripts/keep_alive.py
    python scripts/keep_alive.py --interval 300 --url https://...
"""

import sys
import time
import argparse
import urllib.request
import urllib.error
from datetime import datetime

DEFAULT_URL = "https://9139fedc-2572-4d1e-960d-eff6769ffe32.pandastack.ai/health"
DEFAULT_INTERVAL_SECONDS = 300  # 5 minutos

def ping(url: str) -> tuple[bool, int, str, float]:
    start_time = time.time()
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Doblex-KeepAlive-Worker/1.0",
            "Accept": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            elapsed_ms = (time.time() - start_time) * 1000
            status_code = response.getcode()
            body = response.read().decode("utf-8", errors="replace").strip()
            return True, status_code, body, elapsed_ms
    except urllib.error.HTTPError as e:
        elapsed_ms = (time.time() - start_time) * 1000
        return False, e.code, str(e), elapsed_ms
    except Exception as e:
        elapsed_ms = (time.time() - start_time) * 1000
        return False, 0, str(e), elapsed_ms

def main():
    parser = argparse.ArgumentParser(description="Doblex Backend Keep-Alive Service")
    parser.add_argument("--url", default=DEFAULT_URL, help=f"URL objetivo para ping (defecto: {DEFAULT_URL})")
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL_SECONDS, help="Intervalo en segundos entre cada ping (defecto: 300s = 5m)")
    args = parser.parse_args()

    url = args.url
    interval = args.interval

    print("=" * 65)
    print("   DOBLEX SMU - SERVICIO LOCAL DE KEEP-ALIVE PARA BACKEND")
    print("=" * 65)
    print(f" Target URL : {url}")
    print(f" Intervalo  : Cada {interval} segundos ({interval / 60:.1f} minutos)")
    print(" Presione Ctrl + C para detener el servicio en cualquier momento.\n")

    iteration = 1
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [Intento #{iteration}] Enviando ping...", end=" ", flush=True)

        success, code, msg, elapsed = ping(url)

        if success:
            print(f"OK (Status: {code} | Tiempo: {elapsed:.0f}ms)")
        else:
            print(f"FALLO (Status: {code} | Error: {msg} | Tiempo: {elapsed:.0f}ms)")

        iteration += 1

        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[INFO] Servicio de Keep-Alive detenido por el usuario. ¡Hasta luego!")
            sys.exit(0)

if __name__ == "__main__":
    main()
