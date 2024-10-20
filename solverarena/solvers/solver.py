from abc import ABC, abstractmethod


class Solver(ABC):
    @abstractmethod
    def solve(self, mps_file, time_limit):
        pass

    @abstractmethod
    def get_results(self):
        pass
