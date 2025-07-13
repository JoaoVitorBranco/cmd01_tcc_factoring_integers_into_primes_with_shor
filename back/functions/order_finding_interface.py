from abc import ABC, abstractmethod

class OrderFindingInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, N: int, a: int) -> int:
        pass
