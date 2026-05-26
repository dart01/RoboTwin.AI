import math
import random
import time
from datetime import datetime, timezone

import joblib
import pandas as pd
from supabase import Client, create_client

# ==============================================================================
# 1.  CONFIGURACIÓN DE CREDENCIALES DE SUPABASE
# ==============================================================================
# Reemplaza con tus datos reales de conexión
SUPABASE_URL = "https://nsnrbmszjifxikxyenvi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5zbnJibXN6amlmeGlreHllbnZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk3MTk4NDMsImV4cCI6MjA5NTI5NTg0M30.QhdyhsWiSUOOdDjcgCWc1sDsuDqu0RRrmIQDeC19tbs"

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
    print("✅ Inteligencia Artificial en línea y lista para la inferencia.")
except Exception as e:
    print(
        f"❌ Error al cargar 'anomaly_detector.joblib'. ¿Ejecutaste primero train_anomaly_detector.py? Detalle: {e}"
    )
    exit(1)


# ==============================================================================
# 3. BUCLE DE SIMULACIÓN E INFERENCIA EN TIEMPO REAL
# ==============================================================================
def run_live_simulation():
    print(
        "\n🚀 Transmitiendo telemetría en vivo a Supabase... Presiona Ctrl+C para detener."
    )
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
        # Creamos la estructura exacta que espera el Isolation Forest
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
            # Si el modelo aísla el dato, evaluamos umbrales de peligro mecánico o eléctrico
            if current > 10.0 or torque > 35.0:
                status = "FAILURE"
            else:
                status = "WARNING"

        # Imprimir logs informativos en la consola local
        print(
            f"🤖 J1:{j1}° | Temp:{temperature}°C | Torque:{torque}Nm | Amp:{current}A ──> [IA Veredicto: {status}]"
        )

        # --- CONSTRUCCIÓN DEL PAYLOAD (Satisface restricciones NOT NULL) ---
        payload = {
            "j1_angle": j1,
            "j2_angle": j2,
            "j3_angle": j3,
            "j4_angle": 0.0,  # Satisface la restricción NOT NULL de tu base de datos
            "j5_angle": 0.0,  # Protege contra futuras restricciones similares
            "j6_angle": 0.0,  # Protege contra futuras restricciones similares
            "motor_temperature": temperature,
            "torque_nm": torque,
            "current_amp": current,
            "status": status,
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),  # Formato UTC moderno sin advertencias
        }

        # --- TRANSMISIÓN POR WEBSOCKET / INSERT A SUPABASE ---
        try:
            supabase.table("robot_telemetry").insert(payload).execute()
        except Exception as e:
            print(f"❌ Error al transmitir a Supabase: {e}")

        # Frecuencia de muestreo (1 paquete por segundo)
        time.sleep(1)


if __name__ == "__main__":
    run_live_simulation()
