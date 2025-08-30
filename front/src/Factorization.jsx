import { useState } from "react"
import "bootstrap/dist/css/bootstrap.min.css"
import { MathJax, MathJaxContext } from "better-react-mathjax"
import "./App.css"

function Factorization() {
  const [numero, setNumero] = useState("")
  const [resultado, setResultado] = useState("")
  const [loading, setLoading] = useState(false)
  const [algoritmo, setAlgoritmo] = useState("shor")

  const API_URL = import.meta.env.VITE_API_URL

  const fatorar = async (e) => {
    e.preventDefault()
    if (!numero || parseInt(numero) <= 1) {
      setResultado("\\text{Informe um número maior que 1}")
      return
    }
    setLoading(true)
    setResultado("")
    try {
      const res = await fetch(
        `${API_URL}/api/factorize?number=${numero}&type_alg=${algoritmo}`
      )
      const data = await res.json()
      let latex = ""
      for (const [f, eX] of Object.entries(data.fatores)) {
        latex += `${f}^{${eX}} \\times `
      }
      setResultado(`\\text{Resultado:}\\quad ${latex.slice(0, -7)}`)
    } catch {
      setResultado("\\text{Erro ao consultar o backend}")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h1 className="page-title">Fatoração de Inteiros</h1>
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
            <option value="shor">Shor (Quântico)</option>
            <option value="fermat">Fermat (Clássico)</option>
            <option value="pollard">Pollard (Clássico)</option>
          </select>
        </div>
        <button type="submit" className="custom-button" disabled={loading}>
          {loading ? "Calculando..." : "Fatorar"}
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

export default Factorization
