from functions.order_finding_interface import OrderFindingInterface
import math
from math import gcd
import random

class ControllerShor:
    def __init__(self, order_finding: OrderFindingInterface, n_times_shor: int = 10 ):
        self.order_finding = order_finding
        self.n_times_shor = n_times_shor

    def _run_order_finding(self, N, a):
      r = self.order_finding(N, a)
      print(f"Resultado: r = {r}")

      if r is False:
        print("Não foi possível encontrar um valor de 'r' válido")
        return (False, False)

      # Testa se realmente encontrou um valor de 'r' plausível
      if a ** r % N != 1:
        return (False, a) # Tentar novamente o algoritmo

      # Testa se 'r' é par
      if r % 2 != 0:
        print("'r' não é par")
        return (False, False) # deve trocar o valor de 'a'
      a_r2 = a**(r//2)
      
      chutes = [gcd(a_r2-1, N), gcd(a_r2+1, N)]
      print(f"Chutes de divisores (não podem ser 1 ou {N}): {chutes[0]} e {chutes[1]}")
      for chute in chutes:
          if chute not in [1,N] and (N % chute) == 0:
            retorno = (chute, N // chute)
            print(f"Escolha probabilística encontrou um valor válido com a ** (r / 2) +/- 1 (a_novo, N): {(chute, N // chute)}")
            return (chute, N // chute) # encontrou um divisor de N com a ** (r / 2) +/- 1 
      print(f"Continuando com novo valor de 'a': {chute[0]}")
      return (False, chute[0]) # continuar com novo valor de 'a'

    def _probabilistic_split(self, N: int, start_time=None, timeout=None) -> tuple[int, int]:
        import time
        if timeout is not None and start_time is not None and time.time() - start_time > timeout:
            raise TimeoutError("Tempo limite excedido para fatoração com Shor (30s)")
        if N % 2 == 0 or N < 3:
            raise ValueError("N deve ser ímpar e composto, maior que 2.")
        set_N = list(range(2,N))
        a = random.choice(set_N)
        print(f"Estou na escolha probabilistica. Vou testar o: a = {a} e N = {N}")
        d = math.gcd(a, N)
        if d > 1:
            c = N // d
            print(f"Escolha probabilística encontrou {d} como divisor de {N}")
            return (d, c)
        else:
            try:
                print(f"Entrando no order finding problem... rodando {self.n_times_shor} vezes")
                for _ in range(self.n_times_shor):
                    print(f"\nTentativa: {_ + 1}")
                    possible_divisor, possible_new_N = self._run_order_finding(N, a)
                    if possible_divisor != False and possible_new_N != False:
                        return (possible_divisor, possible_new_N)
                    elif possible_divisor == False and possible_new_N != False:
                        a = possible_new_N
                        print(f"Novo valor de 'a': {a}")
                    else:
                        print("'r' não é par, tentando novamente com novo valor de 'a'")
                        break
                print(f"Nenhuma das {self.n_times_shor} vezes encontrou-se um 'r' válido")
                return False
            except Exception as err:
                print(f"Aconteceu uma exceção: {err}")
                return False

    def _is_prime(self, N: int) -> bool:
      """ Teste simples de primalidade. """
      if N <= 1:
        return False
      if N <= 3:
        return True # 2 é primo
      if N % 2 == 0 or N % 3 == 0: # Validando se tal valor é múltiplo de 2 e 3
        return False
      for i in range(5, int(N**0.5) + 1, 6): # Realizando a fatorização
        if N % i == 0 or N % (i + 2) == 0:
          return False
      return True

    def _is_perfect_power(self, N: int) -> tuple[bool, int, int]:
      """
      Tenta detectar se n é uma potência perfeita: s^j
      by: GPT, Chat
      """
      for j in range(2, int(math.log2(N)) + 2):
        s = round(N ** (1 / j))
        if s**j == N:
          return True, s, j
      return False, None, None

    def _factorize_integers(self, N: int, start_time=None, timeout=None) -> list:
        import time
        if timeout is not None and start_time is not None and time.time() - start_time > timeout:
            raise TimeoutError("Tempo limite excedido para fatoração com Shor (30s)")
        if N <= 1:
            return []
        if self._is_prime(N):
            return [N]
        if N % 2 == 0:
            return [2] + self._factorize_integers(N=N // 2, start_time=start_time, timeout=timeout)
        is_power, s, j = self._is_perfect_power(N)
        if is_power:
            return self._factorize_integers(N=s, start_time=start_time, timeout=timeout) * j
        split = self._probabilistic_split(N=N, start_time=start_time, timeout=timeout)
        if split:
            b, c = split
            return [b] + self._factorize_integers(N=c, start_time=start_time, timeout=timeout)
        else:
            print("Nenhuma escolha probabilística encontrou um valor válido... buscando novo valor...")
            return self._factorize_integers(N=N, start_time=start_time, timeout=timeout)

    def __call__(self, number: str) -> tuple[any, int]:
        import time
        # Validação: é uma string numérica?
        if not isinstance(number, str) or not number.isdigit():
            return ("O número deve ser uma string contendo apenas dígitos", 400)
        number = int(number)
        if number <= 0:
            return ("O número deve ser positivo", 400)
        start_time = time.time()
        timeout = 30
        try:
            result = self._factorize_integers(N=number, start_time=start_time, timeout=timeout)
        except TimeoutError as e:
            return (str(e), 408)
        except Exception as e:
            return (f"Erro inesperado: {e}", 500)
        if result is False:
            return ("Não foi possível encontrar os primos", 404)
        if len(result) == 0:
            return ("Nenhum primo encontrado", 404)
        primes_set = set(result)
        primes_dict = {prime: result.count(prime) for prime in primes_set}
        return (primes_dict, 200)
