import { useState } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css'
import './App.css'
import { MathJax, MathJaxContext } from 'better-react-mathjax'

function App() {
  const [numero, setNumero] = useState('')
  const [resultado, setResultado] = useState('')
  const [loading, setLoading] = useState(false)
  const [algoritmo, setAlgoritmo] = useState('shor')

  const fatorar = async (e) => {
    e.preventDefault()
    if (!numero || parseInt(numero) <= 1) {
      setResultado('\\text{Informe um número maior que 1}')
      return
    }

    setLoading(true)
    setResultado('')

    try {
      const response = await fetch(
        `http://192.168.0.63:5000/api/factorize?number=${numero}&type_alg=${algoritmo}`
      )
      const data = await response.json()
      const fatores = data.fatores
      let latex = ''
      for (const [fator, expoente] of Object.entries(fatores)) {
        latex += `${fator}^{${expoente}} \\times `
      }
      latex = latex.slice(0, -7)
      setResultado(`\\text{Resultado:}\\quad ${latex}`)
    } catch (error) {
      console.error(error)
      setResultado('\\text{Erro ao consultar o backend}')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h2>Fatoração de Inteiros</h2>

      <form onSubmit={fatorar}>
        <div className="mb-3 text-start">
          <label className="form-label">Número:</label>
          <input
            type="number"
            className="form-control"
            value={numero}
            onChange={(e) => setNumero(e.target.value)}
            placeholder="Digite um número"
          />
        </div>

        <div className="mb-3 text-start">
          <label className="form-label">Algoritmo:</label>
          <select
            className="form-select"
            value={algoritmo}
            onChange={(e) => setAlgoritmo(e.target.value)}
          >
            <option value="shor">Shor</option>
            <option value="fermat">Fermat</option>
            <option value="pollard">Pollard</option>
          </select>
        </div>

        <button type="submit" className="w-100 custom-button" disabled={loading}>
          {loading ? 'Calculando...' : 'Fatorar'}
        </button>
      </form>

      <MathJaxContext>
        <div className="resultado text-center">
          {resultado && <MathJax dynamic>{`\\(${resultado}\\)`}</MathJax>}
        </div>
      </MathJaxContext>

      {loading && <div className="loader mx-auto my-3"></div>}
    </div>
  )
}

export default App
