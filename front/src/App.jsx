import { useState } from 'react';
import './App.css';
import Latex from './Latex';

function App() {
  const [numero, setNumero] = useState('');
  const [resultado, setResultado] = useState('');
  const [loading, setLoading] = useState(false);

  const fatorar = async () => {
    if (!numero || parseInt(numero) <= 1) {
      setResultado('\\text{Informe um número maior que 1}');
      return;
    }
    setLoading(true);
    setResultado('');

    try {
      const response = await fetch(`http://192.168.0.63:5000/api/factorize?number=${numero}`);
      const data = await response.json();
      const fatores = data.fatores;
      let latex = '';
      for (const [fator, expoente] of Object.entries(fatores)) {
        latex += `${fator}^{${expoente}} \\times `;
      }
      latex = latex.slice(0, -7); // Remove o último " \\times "
      setResultado(`\\text{Resultado:}\\quad ${latex}`);
    } catch (error) {
      console.error(error);
      setResultado('\\text{Erro ao consultar o backend}');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Fatoração de Inteiros</h1>
      <input
        type="number"
        value={numero}
        onChange={(e) => setNumero(e.target.value)}
        placeholder="Digite um número inteiro"
      />
      <button onClick={fatorar} disabled={loading}>
        {loading ? 'Calculando...' : 'Fatorar'}
      </button>

      {loading && <div className="loader"></div>}

      {!loading && resultado && <Latex texString={resultado} />}
    </div>
  );
}

export default App;
