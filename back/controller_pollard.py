from math import gcd
import random


class ControllerPollard:
    def __init__(self):
        pass

    def __call__(self, number: str) -> tuple[any, int]:
        N = int(number)
        fatores = []
        self._fatorar(N, fatores)

        primes_dict = {}
        for fator in fatores:
            primes_dict[fator] = primes_dict.get(fator, 0) + 1

        return (primes_dict, 200)

    def _is_prime(self, n):
        if n <= 3:
            return n > 1
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def _pollards_rho(self, n):
        if n % 2 == 0:
            return 2
        def f(x): return (x ** 2 + 1) % n
        x = random.randrange(2, n)
        y = x
        d = 1
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = gcd(abs(x - y), n)
        if d == n:
            return None
        return d

    def _fatorar(self, n, fatores):
        if n == 1:
            return
        if self._is_prime(n):
            fatores.append(n)
            return
        fator = None
        while fator is None:
            fator = self._pollards_rho(n)
        if not self._is_prime(fator):
            self._fatorar(fator, fatores)
        else:
            fatores.append(fator)
        self._fatorar(n // fator, fatores)
