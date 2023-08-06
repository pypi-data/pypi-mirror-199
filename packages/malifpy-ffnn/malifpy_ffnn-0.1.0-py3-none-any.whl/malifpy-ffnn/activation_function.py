from __future__ import annotations

from abc import ABC, abstractmethod


class ActivationFunction(ABC):
    @abstractmethod
    def setup(self, **kwargs) -> None:
        pass

    @abstractmethod
    def __call__(self, weighted_input):
        pass

class SoftMax(ActivationFunction):
    def __init__(self) -> None:
        self.sum_of_weighted_sum: float

    def setup(self, **kwargs) -> SoftMax:
        self.sum_of_weighted_sum = kwargs["sum_of_weighted_sum"]
        return self

    def __call__(self, weighted_input):
        return weighted_input / self.sum_of_weighted_sum

