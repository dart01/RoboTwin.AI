import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

export default function TelemetryCharts({ data }) {
  // Retornar vacío o un estado de carga si aún no hay suficientes datos
  if (!data || data.length === 0) {
    return (
      <div className="w-full text-center py-6 text-slate-500 font-mono text-xs">
        📈 Esperando acumulación de datos históricos...
      </div>
    );
  }

  // Formatear el timestamp de Supabase a algo legible (HH:MM:SS)
  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  // Mapeamos los datos de Supabase para las gráficas
  const chartData = data.map(item => ({
    ...item,
    timeLabel: formatTime(item.created_at)
  }));

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
      
      {/* GRÁFICA 1: COMPORTAMIENTO TÉRMICO */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-xl">
        <h3 className="text-sm font-bold text-slate-400 mb-4 uppercase tracking-wider font-mono">
          🌡️ Monitoreo Térmico de Motores
        </h3>
        <div className="w-full">
          {/* Se cambia height="100%" por height={220} para evitar el bug de colapso a 0px */}
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={chartData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="timeLabel" stroke="#475569" style={{ fontSize: '10px', fontFamily: 'monospace' }} />
              <YAxis domain={[20, 90]} stroke="#475569" style={{ fontSize: '10px', fontFamily: 'monospace' }} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                labelStyle={{ color: '#94a3b8', fontFamily: 'monospace' }}
              />
              <Legend wrapperStyle={{ fontSize: '11px', fontFamily: 'monospace', pt: 10 }} />
              <Line 
                type="monotone" 
                dataKey="motor_temperature" 
                name="Temp (°C)" 
                stroke="#f59e0b" 
                strokeWidth={2} 
                dot={false}
                activeDot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* GRÁFICA 2: DIAGNÓSTICO ELÉCTRICO Y MECÁNICO */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-xl">
        <h3 className="text-sm font-bold text-slate-400 mb-4 uppercase tracking-wider font-mono">
          ⚡ Potencia, Corriente y Torque
        </h3>
        <div className="w-full">
          {/* Se cambia height="100%" por height={220} para evitar el bug de colapso a 0px */}
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={chartData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="timeLabel" stroke="#475569" style={{ fontSize: '10px', fontFamily: 'monospace' }} />
              <YAxis stroke="#475569" style={{ fontSize: '10px', fontFamily: 'monospace' }} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                labelStyle={{ color: '#94a3b8', fontFamily: 'monospace' }}
              />
              <Legend wrapperStyle={{ fontSize: '11px', fontFamily: 'monospace' }} />
              <Line 
                type="monotone" 
                dataKey="current_amp" 
                name="Corriente (A)" 
                stroke="#06b6d4" 
                strokeWidth={2} 
                dot={false}
              />
              <Line 
                type="monotone" 
                dataKey="torque_nm" 
                name="Torque (Nm)" 
                stroke="#ec4899" 
                strokeWidth={1.5} 
                dot={false}
                strokeDasharray="4 4"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

    </div>
  );
}