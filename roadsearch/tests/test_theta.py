import unittest
from roadsearch.tests.abstract_test import AbstractTest
from roadsearch.generators.mutators.mutations import ListMutator, ValueAlterationMutator
from roadsearch.generators.exploiters.exploiters import FirstVariableExploiter
from roadsearch.generators.representations.theta_generator import ThetaGenerator


class ThetaTest(AbstractTest):

    def test_all_mutations(self):
        generator = ThetaGenerator(20)
        mutator = ListMutator(generator)
        kappas = generator.generate()
        for name, func in mutator.get_all():
            mutant = func(kappas)
            func(mutant)

    def test_exploiters_all_exploiters(self):
        generator = ThetaGenerator(20)
        exploiter = FirstVariableExploiter()
        kappas = generator.generate()
        for name, func in exploiter.get_all():
            mutant = func(kappas)
            func(mutant)

    def test_random_replacement(self):
        length = 11
        generator = ThetaGenerator(length)
        mutator = ListMutator(generator)
        example = generator.generate()
        self.size_does_not_change(length, example, mutator.random_replacement, is_tuple=True)

    def test_random_alteration(self):
        length = 11
        generator = ThetaGenerator(length)
        mutator = ValueAlterationMutator()
        example = generator.generate()
        self.size_does_not_change(length, example, mutator.random_alteration, is_tuple=True)

    def test_randomly_remove(self):
        length = 15
        generator = ThetaGenerator(length)
        mutator = ListMutator(generator)
        example = generator.generate()
        self.size_decreases_until_minimum_allowed(length=length,
                                                  min_length=mutator.min_length,
                                                  example=example,
                                                  function=mutator.randomly_remove_kappas,
                                                  is_tuple=True)

    def test_randomly_remove_front(self):
        length = 15
        generator = ThetaGenerator(length)
        mutator = ListMutator(generator)
        example = generator.generate()
        self.size_decreases_until_minimum_allowed(length=length,
                                                  min_length=mutator.min_length,
                                                  example=example,
                                                  function=mutator.remove_from_front,
                                                  is_tuple=True)

    def test_randomly_remove_tail(self):
        length = 15
        generator = ThetaGenerator(length)
        mutator = ListMutator(generator)
        example = generator.generate()
        self.size_decreases_until_minimum_allowed(length=length,
                                                  min_length=mutator.min_length,
                                                  example=example,
                                                  function=mutator.remove_from_tail,
                                                  is_tuple=True)


if __name__ == '__main__':
    unittest.main()
