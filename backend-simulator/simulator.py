import math
import os
import random

# 🆕 IMPORTACIONES COMPLETAS PARA FASTAPI Y DESPLIEGUE EN LA NUBE
import threading
import time
from datetime import datetime, timezone

import joblib
import pandas as pd
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import Client, create_client

# Inicializamos la aplicación FastAPI que escuchará las peticiones de Render
app = FastAPI(
    title="Robotic Arm Telemetry Simulator",
    description="Backend para el procesamiento de telemetría e inferencia de IA en tiempo real",
)

# ==============================================================================
# 1. CONFIGURACIÓN DE CREDENCIALES DE SUPABASE
# ==============================================================================
# Carga el archivo .env local si existe. En Render leerá las Variables de Entorno del Panel.
load_dotenv()

SUPABASE_URL = os.environ.get("VITE_SUPABASE_URL")
SUPABASE_KEY = os.environ.get("VITE_SUPABASE_ANON_KEY")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("📡 Conexión inicializada con Supabase.")
except Exception as e:
    print(f"❌ Error crítico al conectar con Supabase: {e}")
    exit(1)


# ==============================================================================
# 2. CARGA DEL MODELO DE INTELIGENCIA ARTIFICIAL
# ==============================================================================
print("🌲 Cargando modelo de detección de anomalías (Isolation Forest)...")
try:
    ai_model = joblib.load("anomaly_detector.joblib")
    print("✅  Inteligencia Artificial en línea y lista para la inferencia.")
except Exception as e:
    print(
        f"❌ Error al cargar 'anomaly_detector.joblib'. ¿Ejecutaste primero train_anomaly_detector.py? Detalle: {e}"
    )
    exit(1)


# ==============================================================================
# 3. BUCLE DE SIMULACIÓN E INFERENCIA EN TIEMPO REAL
# ==============================================================================
def run_live_simulation():
    """
    Esta función contiene tu bucle infinito original. Correrá de forma aislada
    en un hilo secundario (background thread) para no congelar a FastAPI.
    """
    print("\n🚀 Transmitiendo telemetría en vivo a Supabase en segundo plano...")
    iteration = 0
    base_temperature = 36.0

    while True:
        iteration += 1
        t = iteration * 0.1

        # --- GENERACIÓN DE CINEMÁTICA EN VIVO (J1, J2, J3) ---
        j1 = round(60 * math.sin(t), 2)
        j2 = round(45 * math.cos(t * 0.8), 2)
        j3 = round(30 * math.sin(t * 1.2), 2)

        # --- INDUCCIÓN ALEATORIA DE FALLAS (Cada 40 ciclos) ---
        test_anomaly = iteration % 40 == 0

        if not test_anomaly:
            # Comportamiento físico con correlación normal
            torque = round(15.0 + 8.0 * math.sin(t * 2) + random.uniform(-1.0, 1.0), 2)
            current = round((torque * 0.18) + random.uniform(0.1, 0.3), 2)

            thermal_load = current * 1.1
            if base_temperature < 42.0 + thermal_load:
                base_temperature += random.uniform(0.05, 0.15)
            else:
                base_temperature -= random.uniform(0.05, 0.12)
            temperature = round(base_temperature, 2)
        else:
            # Evento crítico para estresar al modelo y validar alertas visuales
            anomaly_type = random.choice(["JAM", "SPIKE"])
            print(f"\n🚨 [Simulador] Inyectando anomalía física: {anomaly_type}")

            if anomaly_type == "JAM":
                torque = round(42.50, 2)
                current = round(8.10, 2)
                temperature = round(base_temperature + 6.0, 2)
            else:
                torque = round(11.20, 2)
                current = round(13.80, 2)  # Cortocircuito / Pico masivo de corriente
                temperature = round(base_temperature, 2)

        # --- 🏋️‍♂️ INFERENCIA DE LA IA CON PANDAS ---
        live_data = pd.DataFrame(
            [
                {
                    "motor_temperature": temperature,
                    "torque_nm": torque,
                    "current_amp": current,
                }
            ]
        )

        # Predicción del modelo: 1 = Normal, -1 = Anomalía detectada
        prediction = ai_model.predict(live_data)[0]

        # --- CLASIFICACIÓN DE SEVERIDAD PARA EL FRONTEND ---
        if prediction == 1:
            status = "OPERATIONAL"
        else:
            if current > 10.0 or torque > 35.0:
                status = "FAILURE"
            else:
                status = "WARNING"

        # Imprimir logs informativos en la consola local / Render logs
        print(
            f"🤖 J1:{j1}° | Temp:{temperature}°C | Torque:{torque}Nm | Amp:{current}A ──> [IA Veredicto: {status}]"
        )

        # --- CONSTRUCCIÓN DEL PAYLOAD (Satisface restricciones NOT NULL) ---
        payload = {
            "j1_angle": j1,
            "j2_angle": j2,
            "j3_angle": j3,
            "j4_angle": 0.0,
            "j5_angle": 0.0,
            "j6_angle": 0.0,
            "motor_temperature": temperature,
            "torque_nm": torque,
            "current_amp": current,
            "status": status,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        # --- TRANSMISIÓN POR WEBSOCKET / INSERT A SUPABASE ---
        try:
            supabase.table("robot_telemetry").insert(payload).execute()
        except Exception as e:
            print(f"❌ Error al transmitir a Supabase: {e}")

        # Frecuencia de muestreo (1 paquete por segundo)
        time.sleep(1)


# ==============================================================================
# 4. CONFIGURACIÓN DE RUTAS Y EVENTOS DE FASTAPI (Para Render)
# ==============================================================================
@app.on_event("startup")
def start_background_simulation():
    """
    Este evento se dispara automáticamente en cuanto FastAPI arranca con éxito.
    Crea un hilo 'daemon' para que la simulación corra sola de fondo.
    """
    sim_thread = threading.Thread(target=run_live_simulation, daemon=True)
    sim_thread.start()
    print("🧵 Hilo secundario del simulador iniciado de manera segura.")


@app.get("/")
def health_check():
    """
    Ruta raíz. Render la consultará constantemente para verificar si el
    servidor está vivo. Al responder con un 200 OK, evitamos el error de 'Port Timeout'.
    """
    return {
        "status": "ONLINE",
        "service": "Robotic Arm Digital Twin - Physics & AI Engine",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ==============================================================================
# 5. EJECUCIÓN LOCAL
# ==============================================================================
if __name__ == "__main__":
    # Si ejecutas 'python simulator.py' localmente, levantará el servidor web en el puerto 8000
    # igual que lo hará Render en la nube, permitiéndote probar todo de forma exacta.
    print("🏠 Iniciando servidor local en el puerto 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
