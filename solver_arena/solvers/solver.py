from abc import ABC, abstractmethod

class Solver(ABC):
    @abstractmethod
    def solve(self, mps_file):
        pass

    @abstractmethod
    def get_results(self):
        pass
