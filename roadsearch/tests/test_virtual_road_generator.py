import unittest

from sbst_beamng.code_pipeline.executors import MockExecutor
from roadsearch.generators.representations.theta_generator import ThetaGenerator, FixStepThetaGenerator
from roadsearch.generators.representations.cartesian_generator import CatmullRomGenerator
from roadsearch.generators.representations.kappa_generator import KappaGenerator, FixStepKappaGenerator
from roadsearch.generators.samples.base import TupleRoadGenerator

TIME_BUDGET = 20


class TestVirtualRoadGenerator(unittest.TestCase):

    def test_theta_generator(self):
        road_generator = TupleRoadGenerator(time_budget=TIME_BUDGET,
                                            executor=MockExecutor(time_budget=TIME_BUDGET*2, map_size=200),
                                            map_size=200,
                                            generator=ThetaGenerator(20),
                                            name='ThetaDefault',
                                            store_data=False)
        road_generator.start()

    def test_theta_fix_step_generator(self):
        road_generator = TupleRoadGenerator(time_budget=TIME_BUDGET,
                                            executor=MockExecutor(time_budget=TIME_BUDGET*2, map_size=200),
                                            map_size=200,
                                            generator=FixStepThetaGenerator(20),
                                            name='ThetaFixStepDefault',
                                            store_data=False)
        road_generator.start()

    def test_kappa_generator(self):
        road_generator = TupleRoadGenerator(time_budget=TIME_BUDGET,
                                            executor=MockExecutor(time_budget=TIME_BUDGET*2, map_size=200),
                                            map_size=200,
                                            generator=KappaGenerator(20),
                                            name='KappaDefault',
                                            store_data=False)
        road_generator.start()

    def test_kappa_fix_step_generator(self):
        road_generator = TupleRoadGenerator(time_budget=TIME_BUDGET,
                                            executor=MockExecutor(time_budget=TIME_BUDGET*2, map_size=200),
                                            map_size=200,
                                            generator=FixStepKappaGenerator(20),
                                            name='KappaFixStepDefault',
                                            store_data=False)
        road_generator.start()

    def test_catmull_rom_generator(self):
        road_generator = TupleRoadGenerator(time_budget=TIME_BUDGET,
                                            executor=MockExecutor(time_budget=TIME_BUDGET*2, map_size=200),
                                            map_size=200,
                                            generator=CatmullRomGenerator(20),
                                            name='CatmullRomDefault',
                                            store_data=False)
        road_generator.start()
