import React, { useState } from "react"
import Clock from "./Clock"
import "./App.css"

function Visualization() {
  const [escala, setEscala] = useState("pequeno")
  const [isRunning, setIsRunning] = useState(false)
  const [resetSignal, setResetSignal] = useState(false)

  const handleStart = () => {
    setIsRunning(true)
    setResetSignal(false)
  }
  const handleReset = () => {
    setIsRunning(false)
    setResetSignal(true)
  }

  return (
    <div className="card">
      <h1 className="page-title">Comparação de Algoritmos de Fatoração</h1>
      <div className="controls">
        <button
          className="custom-button"
          onClick={handleStart}
          disabled={isRunning}
        >
          Iniciar
        </button>
        <button className="custom-button" onClick={handleReset}>
          Resetar
        </button>
        <select
          onChange={(e) => setEscala(e.target.value)}
          disabled={isRunning}
          className="form-select w-auto ms-2"
        >
          <option value="pequeno">Pequeno</option>
          <option value="medio">Médio</option>
          <option value="grande">Grande</option>
          <option value="enorme">Enorme</option>
        </select>
      </div>
      <div className="clocks">
        <Clock
          title="Shor (Quântico)"
          bigOh="O(log³ N)"
          tipoFuncao="shor"
          escala={escala}
          isRunning={isRunning}
          resetSignal={resetSignal}
          onFinish={() => {}}
        />
        <Clock
          title="Fermat (Clássico)"
          bigOh="O(√N)"
          tipoFuncao="fermat"
          escala={escala}
          isRunning={isRunning}
          resetSignal={resetSignal}
          onFinish={() => {}}
        />
        <Clock
          title="Pollard's Rho (Clássico)"
          bigOh="O(N¼)"
          tipoFuncao="pollard"
          escala={escala}
          isRunning={isRunning}
          resetSignal={resetSignal}
          onFinish={() => {}}
        />
      </div>
    </div>
  )
}

export default Visualization
