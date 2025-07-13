from flask import Flask, request, jsonify

from controller import Controller
from functions.order_finding_classical import OrderFindingClassical

order_finding = OrderFindingClassical()
controller = Controller(order_finding=order_finding)
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
