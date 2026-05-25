import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';

export default function RobotModel({ joints }) {
  const j1Ref = useRef();
  const j2Ref = useRef();
  const j3Ref = useRef();
  const alertLightRef = useRef();

  const degToRad = (deg) => (deg * Math.PI) / 180;

  // Extraemos el estado actual del paquete de telemetría (Por defecto OPERATIONAL)
  const status = joints?.status || 'OPERATIONAL';

  // Función utilitaria para calcular colores de alerta dinámicos en los eslabones
  const getComponentColor = (defaultColor) => {
    if (status === 'WARNING') return '#f59e0b'; // Ámbar / Amarillo industrial
    if (status === 'FAILURE') return '#ef4444'; // Rojo crítico
    return defaultColor; // Cyan / Slate original
  };

  useFrame((state) => {
    if (!joints) return;

    // 1. Mover articulaciones
    if (j1Ref.current) j1Ref.current.rotation.y = degToRad(joints.j1_angle || 0);
    if (j2Ref.current) j2Ref.current.rotation.z = degToRad(joints.j2_angle || 0);
    if (j3Ref.current) j3Ref.current.rotation.z = degToRad(joints.j3_angle || 0);

    // 2. Efecto de parpadeo continuo en la luz si el sistema entra en FALLA
    if (alertLightRef.current && status === 'FAILURE') {
      // Usamos el tiempo transcurrido de Three.js para crear una onda seno de pulsación
      const elapsedTime = state.clock.getElapsedTime();
      alertLightRef.current.intensity = Math.sin(elapsedTime * 10) > 0 ? 2.5 : 0;
    } else if (alertLightRef.current && status === 'WARNING') {
      alertLightRef.current.intensity = 1.0; // Luz fija en advertencia
    } else if (alertLightRef.current) {
      alertLightRef.current.intensity = 0.2; // Luz tenue operacional
    }
  });

  return (
    <group position={[0, -2, 0]}>
      {/* --- ESTACIÓN BASE (Fija) --- */}
      <mesh castShadow receiveShadow>
        <cylinderGeometry args={[1.2, 1.5, 0.5, 32]} />
        <meshStandardMaterial color="#334155" roughness={0.4} />
      </mesh>

      {/* --- ARTICULACIÓN 1 (J1: Giro Horizontal) --- */}
      <group ref={j1Ref}>
        <mesh position={[0, 0.5, 0]} castShadow>
          <cylinderGeometry args={[0.8, 0.8, 0.6, 32]} />
          {/* El anillo base cambia de color si hay alertas */}
          <meshStandardMaterial color={getComponentColor('#06b6d4')} metalness={0.6} roughness={0.2} />
        </mesh>

        {/* --- ARTICULACIÓN 2 (J2: Hombro) --- */}
        <group ref={j2Ref} position={[0, 0.8, 0]}>
          <mesh rotation={[Math.PI / 2, 0, 0]} castShadow>
            <cylinderGeometry args={[0.3, 0.3, 0.8, 16]} />
            <meshStandardMaterial color="#475569" />
          </mesh>
          
          {/* Brazo principal */}
          <mesh position={[0, 1, 0]} castShadow>
            <boxGeometry args={[0.4, 2, 0.4]} />
            <meshStandardMaterial color="#f1f5f9" roughness={0.5} />
          </mesh>

          {/* --- ARTICULACIÓN 3 (J3: Codo) --- */}
          <group ref={j3Ref} position={[0, 2, 0]}>
            <mesh rotation={[Math.PI / 2, 0, 0]} castShadow>
              <cylinderGeometry args={[0.25, 0.25, 0.6, 16]} />
              <meshStandardMaterial color="#475569" />
            </mesh>

            {/* Antebrazo: Cambia a ámbar o rojo según la severidad */}
            <mesh position={[0, 0.8, 0]} castShadow>
              <boxGeometry args={[0.3, 1.6, 0.3]} />
              <meshStandardMaterial color={getComponentColor('#06b6d4')} metalness={0.3} />
            </mesh>
            
            {/* Actuador final / Luz piloto de Emergencia */}
            <mesh position={[0, 1.7, 0]}>
              <sphereGeometry args={[0.18, 16, 16]} />
              <meshStandardMaterial 
                color={status === 'OPERATIONAL' ? '#10b981' : getComponentColor('#ef4444')} 
                emissive={status === 'OPERATIONAL' ? '#10b981' : getComponentColor('#ef4444')} 
                emissiveIntensity={0.6} 
              />
            </mesh>

            {/* Luz física puntual que proyecta el color de la alerta sobre la estructura */}
            <pointLight 
              ref={alertLightRef} 
              position={[0, 1.7, 0]} 
              color={status === 'OPERATIONAL' ? '#10b981' : getComponentColor('#ef4444')} 
              distance={3} 
              intensity={0.5} 
            />
          </group>
        </group>
      </group>
    </group>
  );
}