import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid } from '@react-three/drei';
import RobotModel from './RobotModel';

export default function RobotCanvas({ joints }) {
  const status = joints?.status || 'OPERATIONAL';

  // Configuración dinámica del color de las líneas principales de la rejilla
  const getGridColor = () => {
    if (status === 'WARNING') return '#f59e0b';
    if (status === 'FAILURE') return '#ef4444';
    return '#06b6d4'; // Cyan operacional original
  };

  return (
    <div className="w-full h-[400px] bg-slate-950 rounded-xl border border-slate-800 overflow-hidden relative shadow-inner">
      <div className={`absolute top-3 left-3 z-10 border px-3 py-1 rounded text-xs font-mono font-bold transition-all duration-300 ${
        status === 'OPERATIONAL' ? 'bg-slate-900/80 border-slate-700 text-cyan-400' :
        status === 'WARNING' ? 'bg-amber-950/90 border-amber-500 text-amber-400 animate-pulse' :
        'bg-rose-950/90 border-rose-500 text-rose-400 animate-ping-once'
      }`}>
        SISTEMA: {status}
      </div>

      <Canvas shadows camera={{ position: [5, 4, 5], fov: 45 }}>
        <ambientLight intensity={0.6} />
        <pointLight position={[10, 10, 10]} intensity={1.5} castShadow />
        <directionalLight position={[-5, 8, -5]} intensity={0.5} castShadow />

        <RobotModel joints={joints} />

        <Grid
          position={[0, -2, 0]}
          args={[10, 10]}
          cellSize={0.5}
          cellThickness={0.5}
          cellColor="#27272a"
          sectionSize={2}
          sectionThickness={1}
          sectionColor={getGridColor()} // Color reactivo inyectado aquí
          fadeDistance={30}
        />

        <OrbitControls enablePan={true} enableZoom={true} minDistance={3} maxDistance={15} />
      </Canvas>
    </div>
  );
}