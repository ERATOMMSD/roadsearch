import random
import numpy as np
from abc import ABC, abstractmethod


class AbstractMutator(ABC):

    @abstractmethod
    def get_all(self):
        pass


class ListMutator(AbstractMutator):

    def __init__(self, generator):
        self.generator = generator
        self.min_length = 10

    def get_all(self):
        return [('extend test with 1 to 5 new values', self.extend),
                ('randomly remove 1 to 5 values', self.randomly_remove_kappas),
                ('remove 1 to 5 values from front', self.remove_from_front),
                ('remove 1 to 5 values from tail', self.remove_from_tail),
                ('randomly replace 1 to 5 values', self.random_replacement)]

    def remove_from_front(self, test):
        assert len(test) >= self.min_length
        return test[random.randint(1, 5):]

    def remove_from_tail(self, test):
        assert len(test) >= self.min_length
        return test[:-random.randint(1, 5)]

    def randomly_remove_kappas(self, test):
        assert len(test) >= self.min_length
        # number of test to be removed
        k = random.randint(1, 5)
        modified_test = test[:]
        while k > 0 and len(modified_test) > 5:
            # Randomly remove a kappa
            i = random.randint(0, len(modified_test) - 1)
            del modified_test[i]
            k -= 1
        return modified_test

    def extend(self, test):
        modified_test = test[:]
        for i in range(random.randint(1, 5)):
            # Randomly add a value
            modified_test.append(self.generator.get_value(modified_test))
        return modified_test

    def random_replacement(self, kappas):
        # Randomly replace values
        indexes = random.sample(range(len(kappas) - 1), random.randint(1, 5))
        modified_test = kappas[:]
        while indexes:
            i = indexes.pop()
            modified_test[i] = self.generator.get_value(modified_test[:i])
        return modified_test


class ValueAlterationMutator(AbstractMutator):

    def get_all(self):
        return [('alter the values by 0.9 ~ 1.1', self.random_alteration)]

    @staticmethod
    def random_alteration(test):

        modified = False

        while not modified:

            modified_test = []

            for k in test:
                if type(k) == float:
                    if random.random() < 0.1:
                        modified_test.append(k * np.random.uniform(0.90, 1.1))
                        modified = True
                    else:
                        modified_test.append(k)
                elif type(k) == tuple:
                    mk = []
                    for v in k:
                        if random.random() < 0.1:
                            mk.append(v * np.random.uniform(0.90, 1.1))
                            modified = True
                        else:
                            mk.append(v)
                    modified_test.append(tuple(mk))
                else:
                    raise NotImplemented("Method alteration is only implemented for floats or tuples of floats")

        return modified_test


class ValueAlterationMutatorKappaStep(AbstractMutator):

    def get_all(self):
        return [('alter the values by 0.9 ~ 1.1', self.random_alteration)]

    @staticmethod
    def random_alteration(test):
        modified = False

        while not modified:
            modified_test = []
            for k in test[:-1]:
                mk = []
                for v in k:
                    if random.random() < 0.1:
                        mk.append(v * np.random.uniform(0.9, 1.1))
                        modified = True
                    else:
                        mk.append(v)
                modified_test.append(tuple(mk))

            kappa, step = test[-1]
            if random.random() < 0.1:
                modified_kappa = kappa * np.random.uniform(0.9, 1.1)
                modified_test.append((modified_kappa, step))
                modified = True
            else:
                modified_test.append((kappa, step))

        return modified_test
