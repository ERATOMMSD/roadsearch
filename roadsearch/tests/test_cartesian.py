import unittest
from roadsearch.tests.abstract_test import AbstractTest, road_length
from roadsearch.generators.mutators.mutations import ValueAlterationMutator
from roadsearch.generators.exploiters.exploiters import Exploiter
from roadsearch.generators.representations.cartesian_generator import CatmullRomGenerator, points_to_deltas


class CartesianTest(AbstractTest):

    def test_differences(self):
        generator = CatmullRomGenerator(20)
        road_1 = generator.generate()
        road_2 = generator.generate()
        self.assertNotEqual(road_1, road_2)

    def test_all_mutations(self):
        generator = CatmullRomGenerator(20)
        mutator = ValueAlterationMutator()
        kappas = generator.generate()
        for name, func in mutator.get_all():
            mutant = func(kappas)
            func(mutant)

    def test_exploiters_all_exploiters(self):
        generator = CatmullRomGenerator(20)
        exploiter = Exploiter()
        kappas = generator.generate()
        for name, func in exploiter.get_all():
            mutant = func(kappas)
            func(mutant)

    def test_road_to_cartesian(self):
        generator = CatmullRomGenerator(control_nodes=25, num_spline_nodes=20, seg_length=180/25, max_angle=75)
        deltas = generator.generate()
        road = generator.to_cartesian(deltas)
        self.assertEqual(road[0], deltas[0])
        self.assertEqual(deltas[0], points_to_deltas(road)[0])
        self.assertGreater(len(road), len(deltas))

    def test_road_length(self):
        length = 180
        control_nodes = 6
        seg_length = length / (control_nodes - 2)
        generator = CatmullRomGenerator(control_nodes=control_nodes, num_spline_nodes=5, seg_length=seg_length, max_angle=30)
        deltas = generator.generate()
        road = generator.to_cartesian(deltas)
        self.assertEqual(int(road_length(road)), length)


if __name__ == '__main__':
    unittest.main()
