import { useState } from 'react';
import Visualization from './Visualization';
import Factorization from './Factorization';
import './App.css';

function App() {
  const [view, setView] = useState('visualization');

  return (
    <div className="app-container">
      <button
        className="switch-button"
        onClick={() =>
          setView(view === 'visualization' ? 'factorization' : 'visualization')
        }
        aria-label="Trocar de tela"
      >
        ↔
      </button>
      {view === 'visualization' ? <Visualization /> : <Factorization />}
    </div>
  );
}

export default App;