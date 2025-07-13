from functions.order_finding_interface import OrderFindingInterface
import math
import random
from typing import Callable


def probabilistic_split(N: int, order_finding: Callable[[int, int], int]) -> tuple[int, int]:
  """
  Realiza a primeira etapa do algoritmo probabilístico para fatorar N.
  N deve ser um número composto ímpar que não seja potência de primo.
  """
  if N % 2 == 0 or N < 3:
    raise ValueError("N deve ser ímpar e composto, maior que 2.")

  set_N = list(range(2,N))
  a = random.choice(set_N)
  print(f"Estou na escolha probabilistica. Vou testar o: {a}")
  d = math.gcd(a, N) # calcula o maior divisor comum entre os 2 valores
  if d > 1: # significa que d é um divisor de N
    c = N // d # resultado da operação, que entrará na recursão do algorítmo principal
    print(f"Escolha probabilística encontrou {d} como divisor de {N}")
    return (d, c)
  else: # realizando o cálculo da ordem r de a, onde a ^ r = 1 mod N  (order finding problem)
    try:
      print("Entrando no order finding problem...")
      r = order_finding(N, a)
      print(f"Resultado: r = {r}")
      if not r: # não encontrou um valor válido para 'r'
        return False

      # Testa se 'r' é par
      if r % 2 == 1:
          return False
      a_r2 = a**(r//2)

      # Testa apenas a ** (r / 2) - 1 for igual a 'N'
      if a_r2 - 1 == N:
        return False

      # Testa se a primeira tentativa do novo 'a' é válida -> a ** (r / 2) - 1
      divisor_a_r2 = math.gcd(a_r2 - 1, N)
      if divisor_a_r2 > 1:
        print(f"Escolha probabilística encontrou um valor válido com a ** (r / 2) - 1 (a_novo, N): {(divisor_a_r2, N // divisor_a_r2)}")
        return (divisor_a_r2, N // divisor_a_r2)

      # Testa apenas a ** (r / 2) + 1 for igual a 'N'
      if a_r2 + 1 == N:
        return False

      # Testa se a segunda tentativa do novo 'a' é válida -> a ** (r / 2) + 1
      divisor_a_r2 = math.gcd(a_r2 + 1, N)
      if divisor_a_r2 > 1:
        print(f"Escolha probabilística encontrou um valor válido com a ** (r / 2) - 1 (a_novo, N): {(divisor_a_r2, N // divisor_a_r2)}")
        return (divisor_a_r2, N // divisor_a_r2)

      # Se não, o método falhou e deve-se encontrar um novo 'a' aleatório
      else:
        print("Falhou ;-;")
        return False

    except:
      return False

def is_prime(N: int) -> bool:
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

def is_perfect_power(N: int) -> tuple[bool, int, int]:
  """
  Tenta detectar se n é uma potência perfeita: s^j
  by: GPT, Chat
  """
  for j in range(2, int(math.log2(N)) + 2):
    s = round(N ** (1 / j))
    if s**j == N:
      return True, s, j
  return False, None, None

def factorize_integers(N: int, order_finding: Callable[[int, int], int]) -> list:
  # Validações iniciais que nem rodam o algoritmo
  if N <= 1:
    return []
  if is_prime(N):
    return [N]

  # Caso 1: número par
  if N % 2 == 0:
    return [2] + factorize_integers(N=N // 2, order_finding=order_finding)

  # Caso 2: potência perfeita
  is_power, s, j = is_perfect_power(N)
  if is_power:
    return factorize_integers(N=s, order_finding=order_finding) * j

  # Caso 3: entra na análise probabilística
  split = probabilistic_split(N, order_finding)
  if split:
    b, c = split
    return [b] + factorize_integers(N=c, order_finding=order_finding)

  else: # não encontrou nenhum valor, voltará ao algoritmo inicial
    print("Nenhuma escolha probabilística encontrou um valor válido... buscando novo valor...")
    return factorize_integers(N=N, order_finding=order_finding)

class Controller:
    def __init__(self, order_finding: OrderFindingInterface):
        self.order_finding = order_finding

    def __call__(self, number: str) -> tuple[any, int]:
        # Validação: é uma string numérica?
        if not isinstance(number, str) or not number.isdigit():
            return ("O número deve ser uma string contendo apenas dígitos", 400)
        
        # Conversão
        number = int(number)

        # Validação de valor
        if number <= 0:
            return ("O número deve ser positivo", 400)

        # Chamada da função de ordem
        result = factorize_integers(N=number, order_finding=self.order_finding)
        if result is False:
            return ("Não foi possível encontrar os primos", 404)
        
        return (result, 200)
