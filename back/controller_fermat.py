import math


class ControllerFermat:
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

    def _fermat_factor(self, n):
        a = math.isqrt(n)
        if a * a < n:
            a += 1
        b2 = a * a - n
        while not self._is_square(b2):
            a += 1
            b2 = a * a - n
        b = math.isqrt(b2)
        return a - b, a + b

    def _is_square(self, n):
        root = math.isqrt(n)
        return root * root == n

    def _fatorar(self, n, fatores):
        if n == 1:
            return
        if self._is_prime(n):
            fatores.append(n)
            return
        fator1, fator2 = self._fermat_factor(n)
        if fator1 == 1 or fator2 == 1:
            fatores.append(max(fator1, fator2))
            return
        self._fatorar(fator1, fatores)
        self._fatorar(fator2, fatores)
