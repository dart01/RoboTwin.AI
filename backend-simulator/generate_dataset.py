import csv
import math
import random
from datetime import datetime, timedelta

# Configuración del Dataset
FILENAME = "robot_telemetry_dataset.csv"
TOTAL_RECORDS = 5000  # Cantidad de datos ideal para entrenar
NORMAL_RATIO = 0.90  # 90% datos normales, 10% anomalías


def generate_robot_data():
    print(
        f"⚙️ Iniciando generación de dataset mecatrónico ({TOTAL_RECORDS} registros)..."
    )

    # Tiempo inicial simulado (hace unos días atrás)
    current_sim_time = datetime.now() - timedelta(days=2)

    # Encabezados del CSV (idénticos a los campos de tu tabla en Supabase + la etiqueta para validar)
    headers = [
        "j1_angle",
        "j2_angle",
        "j3_angle",
        "motor_temperature",
        "torque_nm",
        "current_amp",
        "status",
        "created_at",
    ]

    with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        # Variables de estado internas del robot (para mantener continuidad térmica)
        base_temperature = 35.0

        for i in range(TOTAL_RECORDS):
            # Avanzar el tiempo simulado 2 segundos por cada registro
            current_sim_time += timedelta(seconds=2)
            timestamp_str = current_sim_time.isoformat()

            # Determinar si este registro será normal o una anomalía inducida
            is_normal = random.random() < NORMAL_RATIO

            # --- MODELADO DE MOVIMIENTO CINEMÁTICO (Física Base) ---
            # Movimiento armónico simple (ondas seno/coseno cruzadas) para simular rutina de trabajo
            t = i * 0.05
            j1 = round(60 * math.sin(t), 2)
            j2 = round(45 * math.cos(t * 0.8), 2)
            j3 = round(30 * math.sin(t * 1.2), 2)

            if is_normal:
                # --- OPERACIÓN NORMAL ---
                # El torque depende dinámicamente de la aceleración simulada por las ondas
                torque = round(
                    15.0 + 8.0 * math.sin(t * 2) + random.uniform(-1.5, 1.5), 2
                )

                # Relación física: La corriente es directamente proporcional al torque (I = k * tau)
                current = round((torque * 0.18) + random.uniform(0.1, 0.4), 2)

                # Termodinámica: La temperatura oscila según el esfuerzo eléctrico y disipación pasiva
                thermal_load = current * 1.2
                if base_temperature < 40.0 + thermal_load:
                    base_temperature += random.uniform(0.05, 0.15)
                else:
                    base_temperature -= random.uniform(0.05, 0.12)

                temperature = round(base_temperature, 2)
                status = "OPERATIONAL"

            else:
                # --- INYECCIÓN DE ANOMALÍAS (10% de probabilidad) ---
                anomaly_type = random.choice(
                    ["THERMAL", "MECHANICAL_JAM", "ELECTRICAL_SPIKE"]
                )

                if anomaly_type == "THERMAL":
                    # Falla de enfriamiento: temperatura sube de golpe de forma crítica
                    torque = round(12.0 + random.uniform(-1, 1), 2)
                    current = round((torque * 0.18) + random.uniform(0.1, 0.3), 2)
                    temperature = round(random.uniform(78.0, 95.0), 2)
                    status = "WARNING"

                elif anomaly_type == "MECHANICAL_JAM":
                    # Atasco: El brazo se frena, el torque y el amperaje se van a zona roja
                    j1, j2, j3 = j1 * 0.1, j2 * 0.1, j3 * 0.1  # Movimiento restringido
                    torque = round(random.uniform(35.0, 48.0), 2)  # Torque altísimo
                    current = round(random.uniform(7.5, 9.8), 2)  # Corriente saturada
                    temperature = round(base_temperature + random.uniform(5, 12), 2)
                    status = "FAILURE"

                elif anomaly_type == "ELECTRICAL_SPIKE":
                    # Corto transitorio: Pico de corriente destructivo sin torque asociado
                    torque = round(10.0 + random.uniform(-1, 1), 2)
                    current = round(
                        random.uniform(11.0, 14.5), 2
                    )  # Pico masivo de Amperios
                    temperature = round(base_temperature, 2)
                    status = "FAILURE"

            # Escribir fila en el archivo CSV
            writer.writerow(
                [j1, j2, j3, temperature, torque, current, status, timestamp_str]
            )

    print(f"🎉 ¡Dataset generado con éxito! Archivo guardado como: '{FILENAME}'")


if __name__ == "__main__":
    generate_robot_data()
