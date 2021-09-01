from abc import ABC, abstractmethod
import random


class RoadGenerator(ABC):

    def __init__(self, length: int, variation: int = 0):
        self.length = length
        self.variation = variation

    def get_length(self):
        return self.length + random.randint(-self.variation, self.variation)

    def generate(self):
        """ Generates a test of x points using the function get_value(previous points).
        Returns:
            a list of delta values.
        """
        test_length = self.length + random.randint(-self.variation, self.variation)
        test = []
        for i in range(test_length):
            test.append(self.get_value(test[:i]))
        return test

    @abstractmethod
    def get_value(self, previous):
        pass

    @abstractmethod
    def to_cartesian(self, test):
        pass
