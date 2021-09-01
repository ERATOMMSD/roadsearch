import unittest
import math
from roadsearch.tests.abstract_test import AbstractTest, road_length
from roadsearch.generators.mutators.mutations import ValueAlterationMutator, ListMutator
from roadsearch.generators.exploiters.exploiters import SingleVariableExploiter
from roadsearch.generators.representations.kappa_generator import FixStepKappaGenerator


class FixStepKappaTest(AbstractTest):

    def test_all_mutations(self):
        generator = FixStepKappaGenerator(20)
        mutator = ValueAlterationMutator()
        kappas = generator.generate()
        for name, func in mutator.get_all():
            mutant = func(kappas)
            func(mutant)

    def test_exploiters_all_exploiters(self):
        generator = FixStepKappaGenerator(20)
        exploiter = SingleVariableExploiter()
        kappas = generator.generate()
        for name, func in exploiter.get_all():
            mutant = func(kappas)
            func(mutant)

    def test_random_replacement(self):
        length = 11
        generator = FixStepKappaGenerator(length)
        mutator = ListMutator(generator)
        example = generator.generate()
        self.size_does_not_change(length, example, mutator.random_replacement)

    def test_random_alteration(self):
        length = 11
        generator = FixStepKappaGenerator(length)
        mutator = ValueAlterationMutator()
        example = generator.generate()
        self.size_does_not_change(length, example, mutator.random_alteration)

    def test_randomly_remove(self):
        length = 15
        generator = FixStepKappaGenerator(length)
        mutator = ListMutator(generator)
        example = generator.generate()
        self.size_decreases_until_minimum_allowed(length=length,
                                                  min_length=mutator.min_length,
                                                  example=example,
                                                  function=mutator.randomly_remove_kappas,
                                                  is_tuple=False)

    def test_randomly_remove_front(self):
        length = 15
        generator = FixStepKappaGenerator(length)
        mutator = ListMutator(generator)
        example = generator.generate()
        self.size_decreases_until_minimum_allowed(length=length,
                                                  min_length=mutator.min_length,
                                                  example=example,
                                                  function=mutator.remove_from_front,
                                                  is_tuple=False)

    def test_randomly_remove_tail(self):
        length = 15
        generator = FixStepKappaGenerator(length)
        mutator = ListMutator(generator)
        example = generator.generate()
        self.size_decreases_until_minimum_allowed(length=length,
                                                  min_length=mutator.min_length,
                                                  example=example,
                                                  function=mutator.remove_from_tail,
                                                  is_tuple=False)

    def test_road_length(self):
        length = 180
        # when the number of kappa values is high enough the length is close to what we expect
        number_of_kappa_values = 40
        step_size = length / (number_of_kappa_values - 1)
        generator = FixStepKappaGenerator(length=number_of_kappa_values, step=step_size, variation=0)
        deltas = generator.generate()
        road = generator.to_cartesian(deltas)
        # with few number of kappa values or larger bounds this test shouldn't hold
        self.assertAlmostEqual(math.ceil(road_length(road)), length)


if __name__ == '__main__':
    unittest.main()
