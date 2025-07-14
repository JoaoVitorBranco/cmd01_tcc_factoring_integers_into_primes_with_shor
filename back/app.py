from flask import Flask, request, jsonify
from flask_cors import CORS

from controller import Controller
from functions.order_finding_classical import OrderFindingClassical
from functions.order_finding_shor import OrderFindingShor

order_finding = OrderFindingShor()
controller = Controller(order_finding=order_finding)
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return {"mensagem": "API Flask funcionando!"}

@app.route('/api/factorize', methods=['GET'])
def factorize():
    number = request.args.get('number')
    if not number:
        return jsonify({"erro": "Parâmetro 'nome' é obrigatório"}), 400
    
    result, status_code = controller(number)
    
    if status_code == 200:
        return jsonify({"fatores": result}), status_code
    else:
        return jsonify({"erro": result}), status_code

@app.route('/api/microtesting', methods=['GET'])
def microtesting():
    from fractions import Fraction

    def continued_fraction(x, max_denominator):
        """Aproxima x como uma fração com denominador ≤ max_denominator"""
        frac = Fraction(x).limit_denominator(max_denominator)
        return frac.numerator, frac.denominator
    def test_continued_fraction(x, expected_p, expected_q, max_denominator=100):
        # Executa o algoritmo
        p, q = continued_fraction(x, max_denominator)

        # Validação
        if p == expected_p and q == expected_q:
            return(f"🟩 Teste PASSOU: {p}/{q} é a fração esperada para {x}")
        else:
            return(f"🟥 Teste FALHOU: Obtido {p}/{q}, mas esperado era {expected_p}/{expected_q}")

    p = request.args.get('p', 2, type=int)
    q = request.args.get('q', 15, type=int)
    decimal = request.args.get('decimal', 0.133333, type=float)

    return jsonify({"message": test_continued_fraction(decimal, p, q)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
