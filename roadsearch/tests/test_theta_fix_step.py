import unittest
import math
from roadsearch.tests.abstract_test import AbstractTest, road_length
from roadsearch.generators.mutators.mutations import ListMutator, ValueAlterationMutator
from roadsearch.generators.exploiters.exploiters import SingleVariableExploiter
from roadsearch.generators.representations.theta_generator import FixStepThetaGenerator
import numpy as np

class FixStepThetaTest(AbstractTest):

    def test_all_mutations(self):
        generator = FixStepThetaGenerator(20)
        mutator = ListMutator(generator)
        kappas = generator.generate()
        for name, func in mutator.get_all():
            mutant = func(kappas)
            func(mutant)

    def test_exploiters_all_exploiters(self):
        generator = FixStepThetaGenerator(20)
        exploiter = SingleVariableExploiter()
        kappas = generator.generate()
        for name, func in exploiter.get_all():
            mutant = func(kappas)
            func(mutant)

    def test_random_replacement(self):
        length = 11
        generator = FixStepThetaGenerator(length)
        mutator = ListMutator(generator)
        example = generator.generate()
        self.size_does_not_change(length, example, mutator.random_replacement)

    def test_random_alteration(self):
        length = 11
        generator = FixStepThetaGenerator(length)
        mutator = ValueAlterationMutator()
        example = generator.generate()
        self.size_does_not_change(length, example, mutator.random_alteration)

    def test_randomly_remove(self):
        length = 15
        generator = FixStepThetaGenerator(length)
        mutator = ListMutator(generator)
        example = generator.generate()
        self.size_decreases_until_minimum_allowed(length=length,
                                                  min_length=mutator.min_length,
                                                  example=example,
                                                  function=mutator.randomly_remove_kappas,
                                                  is_tuple=False)

    def test_randomly_remove_front(self):
        length = 15
        generator = FixStepThetaGenerator(length)
        mutator = ListMutator(generator)
        example = generator.generate()
        self.size_decreases_until_minimum_allowed(length=length,
                                                  min_length=mutator.min_length,
                                                  example=example,
                                                  function=mutator.remove_from_front,
                                                  is_tuple=False)

    def test_randomly_remove_tail(self):
        length = 15
        generator = FixStepThetaGenerator(length)
        mutator = ListMutator(generator)
        example = generator.generate()
        self.size_decreases_until_minimum_allowed(length=length,
                                                  min_length=mutator.min_length,
                                                  example=example,
                                                  function=mutator.remove_from_tail,
                                                  is_tuple=False)

    def test_road_length(self):
        length = 180
        number_of_theta_values = 20
        step_size = length / number_of_theta_values
        generator = FixStepThetaGenerator(length=number_of_theta_values, step=step_size, variation=0, bound= np.pi/18, delta=np.pi/30)
        deltas = generator.generate()

        road = generator.to_cartesian(deltas)
        # with larger values of bounds this test shouldn't hold
        self.assertEqual(math.ceil(road_length(road)), length)


if __name__ == '__main__':
    unittest.main()
