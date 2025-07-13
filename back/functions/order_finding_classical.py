from functions.order_finding_interface import OrderFindingInterface

class OrderFindingClassical(OrderFindingInterface):
    def __call__(self, N: int, a: int) -> int:
        for r in range(1, 100):
            if pow(a, r, N) == 1:  # usa pow com mod otimizado
                return r
            
        return False