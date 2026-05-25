import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest


def train_robot_model():
    print("🐼 1. Cargando el dataset con Pandas...")
    # Pandas lee el CSV y lo transforma en una tabla inteligente en memoria
    df = pd.read_csv("robot_telemetry_dataset.csv")

    print(f"✅ Dataset cargado con éxito. Total de registros: {len(df)}")

    print("\n📊 2. Selección de características (Feature Engineering)...")
    # Para entrenar la IA, solo nos interesan las variables físicas reales.
    # No queremos los ángulos (el robot se mueve normal) ni las estampas de tiempo.
    # Y lo más importante: ¡Ocultamos la columna 'status' para que el modelo no haga trampa!
    features = ["motor_temperature", "torque_nm", "current_amp"]

    X_train = df[features]

    print("Las variables físicas que la IA analizará son:")
    print(X_train.head())  # Muestra las primeras 5 filas ordenadas por Pandas

    print("\n🌲 3. Inicializando el modelo Isolation Forest...")
    # 'contamination=0.10' le dice a la IA que esperamos aproximadamente un 10% de anomalías en los datos.
    # 'random_state=42' es una semilla para que el entrenamiento sea replicable y dé el mismo resultado siempre.
    model = IsolationForest(contamination=0.10, random_state=42)

    print("🏋️‍♂️ 4. Entrenando el modelo (Buscando patrones anómalos)...")
    model.fit(X_train)

    print("\n💾 5. Guardando el cerebro de la IA...")
    # Guardamos el modelo entrenado en un archivo binario (.joblib)
    # Esto nos permitirá cargarlo en el script de simulación real en vivo sin volver a entrenar.
    model_filename = "anomaly_detector.joblib"
    joblib.dump(model, model_filename)

    print(f"🎉 ¡Éxito total! Modelo entrenado y exportado como '{model_filename}'")


if __name__ == "__main__":
    train_robot_model()
