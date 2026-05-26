# 🤖 Robotic Arm Digital Twin & AI Anomaly Detector

¡Bienvenido al Gemelo Digital del Brazo Robótico! Este proyecto es un ecosistema completo que simula la física, cinemática y variables eléctricas de un brazo robótico industrial en tiempo real. Los datos son analizados instantáneamente por una Inteligencia Artificial para predecir fallas mecánicas o eléctricas antes de que ocurran, todo visualizado en una interfaz web 3D interactiva de alta fidelidad.

🌐 **Enlace del Proyecto en Vivo:** https://robo-twin-ai.vercel.app/
▶️ **Backend Engine en la Nube:** https://dashboard.render.com/web/srv-d8afrf28qa3s73eq5im0/deploys/dep-d8aftogjs32c7397926g?r=2026-05-26%4002%3A00%3A06%7E2026-05-26%4002%3A10%3A09

---

## 💡 ¿Qué es y cómo funciona? (Explicación para humanos)

Imagina que tienes un robot real trabajando en una fábrica. Para saber si está bien, necesitarías estar junto a él revisando sus motores todo el día. 

Este proyecto crea un **"Avatar Virtual" (Gemelo Digital)** de ese robot en internet que se comporta exactamente como el real. El sistema funciona en tres pasos automáticos que ocurren en menos de un segundo:

1. **El Robot Habla:** El brazo robótico genera movimientos (ángulos) y reporta su estado de salud constante (temperatura del motor, cuánta fuerza hace y cuánta electricidad consume).
2. **El "Cerebro" (IA) Analiza:** Una Inteligencia Artificial actúa como un médico especialista en tiempo real. Lee esos signos vitales y, si detecta un comportamiento extraño (como un motor trabado o un cortocircuito), lanza una alerta instantánea de peligro.
3. **El Tablero Digital te Muestra Todo:** En la pantalla web ves un modelo en 3D interactivo que se mueve al mismo tiempo que el robot. Puedes rotar la cámara, hacer zoom, examinar las articulaciones y ver gráficas de su rendimiento en vivo desde tu computadora o celular, sin importar en qué parte del mundo estés.

---

## 🏗️ Arquitectura del Sistema

El proyecto está diseñado bajo una arquitectura desacoplada, escalable y distribuida en la nube:

```text
[ Simulador de Física y Cinemática (Python) ]
                  │
                  ▼
   [ Inferencia de IA (Isolation Forest) ]
                  │
                  ▼
    [ Base de Datos Realtime (Supabase) ] ◄── (WebSockets)
                  │
                  ▼
 [ Frontend 3D Interactivo (React + Three.js) ] ──► [ Servido en Vercel ]

 ```

## 🛠️ Tecnologías Utilizadas

💻 Frontend (Visualización e Interactividad)
* **React & Vite:** Es el motor principal de la interfaz web, elegido para que la página sea ultra rápida y cargue en un parpadeo.
* **Three.js / React Three Fiber:** Renderizado de gráficos 3D acelerados por hardware en el navegador (permite órbita, zoom y paneo del brazo).
* **Recharts:** Gráficos dinámicos para el monitoreo de telemetría en tiempo real.
* **Tailwind CSS:** Diseño de interfaz moderno, responsivo y estilo Dashboard Industrial.

### 🧠 Backend & Inteligencia Artificial
* **Python:** Lenguaje central para el procesamiento matemático y algorítmico.
* **FastAPI:** Framework de alto rendimiento utilizado para exponer el estado del servidor y facilitar el despliegue.
* **Scikit-Learn (Isolation Forest):** Modelo de IA no supervisado entrenado para la detección temprana de anomalías aislando patrones de datos atípicos.
* **Pandas:** Procesamiento y estructuración de los flujos de datos antes de la inferencia.
* **Joblib:** Serialización y carga eficiente del modelo de IA preentrenado.

### ☁️ Infraestructura y DevOps
* **Supabase (PostgreSQL):** Base de datos en la nube encargada de recibir las inserciones y esparcir los datos instantáneamente al frontend mediante canales Realtime (WebSockets).
* **Vercel:** Alojamiento y despliegue continuo de la aplicación cliente (Frontend).
* **Render:** Alojamiento del motor de simulación y procesamiento de IA corriendo de forma autónoma en segundo plano 24/7 mediante hilos de ejecución (threading).

---

## 📈 El Camino de Construcción (Paso a Paso)

Este proyecto fue desarrollado de forma incremental, siguiendo las mejores prácticas de la ingeniería de software y la mecatrónica:

1. **Fase 1: Modelado Matemático y Física:** Se codificaron las ecuaciones cinemáticas de las articulaciones principales (J1, J2, J3) y se diseñó un modelo de correlación física real donde el torque mecánico impacta directamente el consumo de corriente y la temperatura térmica.
2. **Fase 2: Entrenamiento del Modelo de IA:** Se generaron miles de registros de comportamiento operativo normal y se inyectaron fallas controladas (picos eléctricos y atascos mecánicos). Con estos datos se entrenó un modelo Isolation Forest, ideal para detectar anomalías sin necesidad de datos previamente etiquetados.
3. **Fase 3: Canalización de Datos (Pipeline):** Se integró el cliente de Supabase en el script de Python para enviar paquetes de datos en formato JSON cada segundo, garantizando que la base de datos soporte la carga continua.
4. **Fase 4: Desarrollo de la Interfaz 3D:** Se construyó la escena tridimensional en el navegador, acoplando los controles del mouse para la libertad de cámara y mapeando los ángulos de la base de datos directamente a las transformaciones geométricas del brazo robótico.
5. **Fase 5: Despliegue Global e Independencia:** Se migró toda la infraestructura de un entorno local a la nube. El backend fue adaptado con programación multihilo (threading) para mantener la simulación viva en Render mientras responde a las validaciones de salud de la plataforma, rompiendo la dependencia de una computadora física local.

---

## 🚀 Instalación y Ejecución Local

Si deseas clonar este proyecto y ejecutarlo en tu máquina local, sigue estos pasos:

### Prerrequisitos
* Node.js (v18 o superior)
* Python (v3.9 o superior)
* Una cuenta activa en Supabase

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/Robotic-arm-digital-twin.git](https://github.com/tu-usuario/Robotic-arm-digital-twin.git)
cd Robotic-arm-digital-twin
```
