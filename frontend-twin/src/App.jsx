import { useEffect, useState } from 'react';
import { supabase } from './config/supabaseClient';
import RobotCanvas from './components/RobotCanvas';
import TelemetryCharts from './components/TelemetryCharts'; // Importación agregada

export default function App() {
  const [telemetry, setTelemetry] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    console.log("🔄 Conectando al canal de Supabase Realtime...");

    // Suscribirse a los inserts de la tabla 'robot_telemetry' de forma limpia
    const channel = supabase
      .channel('robot-live-data')
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'robot_telemetry' },
        (payload) => {
          console.log('🤖 Telemetría en vivo:', payload.new);
          
          // 1. Guardar el último dato para los valores numéricos y el 3D
          setTelemetry(payload.new);

          // 2. Acumular en el historial para las gráficas (Ventana deslizante de 20 datos)
          setHistory((prevHistory) => {
            const updatedHistory = [...prevHistory, payload.new];
            if (updatedHistory.length > 20) {
              updatedHistory.shift(); // Elimina el dato más viejo si supera los 20
            }
            return updatedHistory;
          });
        }
      )
      .subscribe((status) => {
        if (status === 'SUBSCRIBED') {
          setIsConnected(true);
          console.log('✅ Escuchando base de datos en tiempo real');
        } else {
          setIsConnected(false);
        }
      });

    // Limpieza al desmontar el componente
    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 flex flex-col items-center">
      <header className="mb-6 text-center w-full max-w-5xl">
        <h1 className="text-3xl font-extrabold text-cyan-400 tracking-widest">
          ROBOTIC ARM DIGITAL TWIN
        </h1>
        <p className="text-slate-400 text-sm mt-1">Hito 2: Monitoreo Cinemático y Analítico en Tiempo Real</p>
      </header>

      {/* Grid de distribución superior: Visor 3D y Telemetría Numérica */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl mb-6">
        
        {/* Columna Izquierda/Centro: Visor 3D */}
        <div className="md:col-span-2 flex flex-col gap-4">
          <RobotCanvas joints={telemetry} />
        </div>

        {/* Columna Derecha: Panel de Telemetría Numérica */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-2xl flex flex-col justify-between">
          <div>
            {/* Estado de la conexión */}
            <div className="flex items-center justify-between mb-6 border-b border-slate-800 pb-4">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Flujo de Datos:</span>
              <span className={`px-3 py-1 rounded-full text-xs font-bold flex items-center gap-2 ${
                isConnected ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
              }`}>
                <span className={`h-2 w-2 rounded-full ${isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400'}`}></span>
                {isConnected ? 'ONLINE' : 'OFFLINE'}
              </span>
            </div>

            {/* Datos */}
            {telemetry ? (
              <div className="space-y-4 font-mono text-xs">
                <div className="space-y-2 bg-slate-950 p-3 rounded border border-slate-800">
                  <p className="text-slate-400 font-bold border-b border-slate-800 pb-1 uppercase tracking-tight text-[10px]">Coordenadas Angulares</p>
                  <div className="flex justify-between"><span>J1 (Giro Base):</span> <span className="text-cyan-400 font-bold">{telemetry.j1_angle}°</span></div>
                  <div className="flex justify-between"><span>J2 (Hombro):</span> <span className="text-cyan-400 font-bold">{telemetry.j2_angle}°</span></div>
                  <div className="flex justify-between"><span>J3 (Codo):</span> <span className="text-cyan-400 font-bold">{telemetry.j3_angle}°</span></div>
                </div>

                <div className="space-y-2 bg-slate-950 p-3 rounded border border-slate-800">
                  <p className="text-slate-400 font-bold border-b border-slate-800 pb-1 uppercase tracking-tight text-[10px]">Variables Físicas</p>
                  <div className="flex justify-between"><span>Temperatura:</span> <span className="text-amber-400 font-bold">{telemetry.motor_temperature} °C</span></div>
                  <div className="flex justify-between"><span>Torque:</span> <span className="text-amber-400 font-bold">{telemetry.torque_nm} Nm</span></div>
                  <div className="flex justify-between"><span>Corriente:</span> <span className="text-amber-400 font-bold">{telemetry.current_amp} A</span></div>
                </div>
              </div>
            ) : (
              <p className="text-center text-slate-500 text-sm animate-pulse py-12">
                ⏳ Esperando primer paquete cinemático...
              </p>
            )}
          </div>

          {/* Estado de Alerta al fondo */}
          {telemetry && (
            <div className="mt-6 pt-4 border-t border-slate-800 flex justify-between items-center">
              <span className="text-xs text-slate-500">Estado del Sistema:</span>
              <span className={`font-bold text-xs px-2 py-1 rounded ${
                telemetry.status === 'OPERATIONAL' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' :
                telemetry.status === 'WARNING' ? 'bg-amber-950 text-amber-400 border border-amber-800' : 'bg-rose-950 text-rose-400 border border-rose-800'
              }`}>
                {telemetry.status}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Fila inferior completa para analíticas */}
      <div className="w-full max-w-5xl">
        <TelemetryCharts data={history} />
      </div>

    </div>
  );
}