from flask import Flask, request, jsonify
from flask_cors import CORS

from controller_shor import ControllerShor
from controller_pollard import ControllerPollard
from controller_fermat import ControllerFermat
from functions.order_finding_classical import OrderFindingClassical
from functions.order_finding_shor import OrderFindingShor


order_finding = OrderFindingShor()
controller = ControllerShor(order_finding=order_finding, n_times_shor=1)
controller_classical = ControllerPollard()
controller_fermat = ControllerFermat()
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return {"mensagem": "API Flask funcionando!"}

@app.route('/api/factorize', methods=['GET'])
def factorize():
    number = request.args.get('number')
    type_alg = request.args.get('type_alg')
    if not number:
        return jsonify({"erro": "Parâmetro 'number' é obrigatório"}), 400
    
    LIMIT_NUMBER  = 60
    if not number.isdigit() or int(number) < 2 or int(number) > LIMIT_NUMBER:
        return jsonify({"erro": f"Parâmetro 'number' deve ser um inteiro entre 2 e {LIMIT_NUMBER}"}), 400
    
    if type_alg == None or type_alg == "shor":
        result, status_code = controller(number)
    elif type_alg != None and type_alg == "pollard":
        result, status_code = controller_classical(number)
    elif type_alg != None and type_alg == "fermat":
        result, status_code = controller_fermat(number)
    else:
        return jsonify({"erro": "Parâmetro 'type_algo' inválido"}), 400
        


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
