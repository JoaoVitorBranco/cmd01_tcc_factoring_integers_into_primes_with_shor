from functions.order_finding_interface import OrderFindingInterface
import math
import random
from typing import Callable, Tuple
from fractions import Fraction
import numpy as np
from math import gcd, log, floor
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, transpile
from qiskit.circuit.library import UnitaryGate, QFT
from qiskit.visualization import display

class OrderFindingShor(OrderFindingInterface):

    def _c_mod_mult_gate(self, b, N):
        """
        Retorna a versão controlada da porta modular que implementa |x⟩ → |b·x mod N⟩
        controlada por 1 qubit.

        Parâmetros:
        - b: inteiro multiplicador (coprimo de N)
        - N: inteiro módulo

        Retorna:
        - Uma UnitaryGate controlada (1 qubit de controle)
        """
        if gcd(b, N) > 1:
            raise ValueError(f"Erro: gcd({b}, {N}) > 1 — b e N devem ser coprimos.")

        n = floor(log(N - 1, 2)) + 1  # Número de qubits necessários para representar N
        U = np.zeros((2**n, 2**n))

        for x in range(N):
            U[b * x % N][x] = 1
        for x in range(N, 2**n):
            U[x][x] = 1  # Mapeia fora do domínio válido para identidade

        base_gate = UnitaryGate(U, label=f"{b}×mod{N}")
        controlled_gate = base_gate.control()  # Cria a versão com 1 qubit de controle

        return controlled_gate


    def _continued_fraction(self, x, max_denominator):
        """
        Aproxima x como uma fração com denominador ≤ max_denominator
        """
        frac = Fraction(x).limit_denominator(max_denominator)
        return frac.numerator, frac.denominator

    def _order_finding_circuit(self, N, a, m=None, view_circuit=False):
        if m is None:
        m = math.ceil(2 * log(N, 2)) + 1  # Número de qubits de controle
        n = floor(log(N - 1, 2)) + 1  # Número de qubits de dados (registrador modular)

        # Registradores
        q_control = QuantumRegister(m, 'ctrl')
        q_data = QuantumRegister(n, 'data')
        c_out = ClassicalRegister(m, 'c')
        qc = QuantumCircuit(q_control, q_data, c_out)

        # Estado inicial |1⟩ no registrador de dados
        qc.x(q_data[0])

        # Hadamard em todos os qubits de controle
        for i in range(m):
            qc.h(q_control[i])

        # Aplicar operações controladas: a^(2^i) mod N
        for i in range(m):
            exponent = 2 ** i
            mod_gate = self._c_mod_mult_gate(pow(a, exponent, N), N)
            qc.append(mod_gate, [q_control[i]] + list(q_data))

        # Aplicar QFT† no controle
        qft_dagger = QFT(num_qubits=m, inverse=True, do_swaps=True).decompose()
        qc.append(qft_dagger, q_control)

        # Medir o registrador de controle
        qc.measure(q_control, c_out)

        if view_circuit:
            display(qc.draw(output='mpl'))

        return qc

    def __call__(self, N: int, a: int, m = None, shots = 1) -> int:
        if m is None:
            m = math.ceil(2 * log(N, 2)) + 1  # Número de qubits de controle

        qc = self._order_finding_circuit(N=N, a=a, m=m, view_circuit=False)

        # === Simulação ===
        backend = Aer.get_backend('qasm_simulator')
        transpiled = transpile(qc, backend)
        job = backend.run(transpiled, shots=shots, memory=True)
        result = job.result()

        # === Obter leitura da memória ===
        readings =  result.get_counts()
        measured_bin = max(readings, key=readings.get) # Leitura mais significativa
        measured_int = int(measured_bin, 2)

        # === Calcular fase observada ===
        phase = measured_int / (2 ** m)

        # === Estimar r com frações contínuas ===
        print(f"Phase encontrada = {phase}, para N = {N} e a = {a}")
        r = self._continued_fraction(phase, N)[1]

        return r