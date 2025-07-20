import { useEffect, useRef, useState } from 'react';
import { InlineMath } from 'react-katex';
import './Clock.css';

function Clock({
  title, bigOh, tipoFuncao, escala,
  isRunning, resetSignal, onFinish
}) {
  const [percentual, setPercentual] = useState(0);
  const [finalizado, setFinalizado] = useState(false);
  const requestRef = useRef(null);
  const startTimeRef = useRef(null);
  const tempoTotalRef = useRef(0);

  const calcularTempoTotal = (escala, tipo) => {
    if (escala === 'pequeno') {
      return 0;
    }
    if (escala === 'medio') {
      if (tipo === 'shor') return 0;
      if (tipo === 'fermat') return 5000; // 5s
      if (tipo === 'pollard') return 3000; // 3s
    }
    if (escala === 'grande') {
      if (tipo === 'shor') return 0;
      if (tipo === 'fermat') return 3 * 24 * 3600 * 1000; // 3 dias em ms
      if (tipo === 'pollard') return 2 * 24 * 3600 * 1000; // 2 dias em ms
    }
    if (escala === 'enorme') {
      if (tipo === 'shor') return 8 * 3600 * 1000; // 8h em ms
      if (tipo === 'fermat') return 5000 * 365 * 24 * 3600 * 1000; // 5000 anos
      if (tipo === 'pollard') return 2000 * 365 * 24 * 3600 * 1000; // 2000 anos
    }
    return 1000;
  };

  useEffect(() => {
    if (isRunning && !finalizado && !resetSignal) {
      tempoTotalRef.current = calcularTempoTotal(escala, tipoFuncao);
      startTimeRef.current = performance.now();

      if (tempoTotalRef.current === 0) {
        setPercentual(100);
        setFinalizado(true);
        onFinish();
        return;
      }

      const animate = (time) => {
        const elapsed = time - startTimeRef.current;
        const progress = Math.min((elapsed / tempoTotalRef.current) * 100, 100);
        setPercentual(progress);

        if (progress < 100) {
          requestRef.current = requestAnimationFrame(animate);
        } else {
          setFinalizado(true);
          onFinish();
        }
      };

      requestRef.current = requestAnimationFrame(animate);
    }

    return () => cancelAnimationFrame(requestRef.current);
  }, [isRunning, resetSignal]);

  useEffect(() => {
    if (resetSignal) {
      setPercentual(0);
      setFinalizado(false);
    }
  }, [resetSignal]);

  const radius = 50;
  const circ = 2 * Math.PI * radius;
  const offset = circ * (1 - percentual / 100);

  return (
    <div className="clock-panel">
      <h3 className="clock-title">{title}</h3>
      <div className="clock-bigoh">Complexidade: <InlineMath math={bigOh} /></div>
      <div className="clock-circle">
        <svg width="120" height="120">
          <circle cx="60" cy="60" r={radius} fill="none" stroke="#e6e6e6" strokeWidth="10" />
          <circle cx="60" cy="60" r={radius} fill="none" stroke="#7e5bef" strokeWidth="10"
            strokeDasharray={circ} strokeDashoffset={offset} />
        </svg>
        <div className="clock-percent">{Math.round(percentual)}%</div>
      </div>
      <p className="estimated-time">
        Tempo estimado: {
          tempoTotalRef.current === 0 ? 'Instantâneo' :
          tempoTotalRef.current >= 1000 * 3600 * 24 * 365
            ? Math.round(tempoTotalRef.current / (1000 * 3600 * 24 * 365)) + " anos"
            : tempoTotalRef.current >= 1000 * 3600 * 24
              ? Math.round(tempoTotalRef.current / (1000 * 3600 * 24)) + " dias"
              : tempoTotalRef.current >= 1000 * 3600 
              ? Math.round(tempoTotalRef.current / (1000 * 3600)) + " horas"
              : (tempoTotalRef.current / 1000).toFixed(1) + "s"
        }
      </p>
      {finalizado && <p className="text-success">Finalizado!</p>}
    </div>
  );
}

export default Clock;
