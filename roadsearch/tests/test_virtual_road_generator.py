import unittest

import sys
sys.path.append('../../sbst_beamng/')

from code_pipeline.executors import MockExecutor
from roadsearch.generators.representations.theta_generator import ThetaGenerator, FixStepThetaGenerator
from roadsearch.generators.representations.cartesian_generator import CatmullRomGenerator
from roadsearch.generators.representations.kappa_generator import KappaGenerator, FixStepKappaGenerator
from roadsearch.generators.samples.base import TupleRoadGenerator

TIME_BUDGET = 20

RESULTS_DIR = './results/'


class TestVirtualRoadGenerator(unittest.TestCase):

    def setUp(self) -> None:
        import os
        if not os.path.exists(RESULTS_DIR):
            os.mkdir(RESULTS_DIR)

    def tearDown(self) -> None:
        import os
        for file in os.listdir(RESULTS_DIR):
            path_file = os.path.join(RESULTS_DIR, file)
            os.remove(path_file)
        os.rmdir(RESULTS_DIR)

    def test_theta_generator(self):
        road_generator = TupleRoadGenerator(time_budget=TIME_BUDGET,
                                            executor=MockExecutor(time_budget=TIME_BUDGET*2, map_size=200, result_folder='./results'),
                                            map_size=200,
                                            generator=ThetaGenerator(20),
                                            name='ThetaDefault',
                                            store_data=False)
        road_generator.start()

    def test_theta_fix_step_generator(self):
        road_generator = TupleRoadGenerator(time_budget=TIME_BUDGET,
                                            executor=MockExecutor(time_budget=TIME_BUDGET*2, map_size=200, result_folder='./results'),
                                            map_size=200,
                                            generator=FixStepThetaGenerator(20),
                                            name='ThetaFixStepDefault',
                                            store_data=False)
        road_generator.start()

    def test_kappa_generator(self):
        road_generator = TupleRoadGenerator(time_budget=TIME_BUDGET,
                                            executor=MockExecutor(time_budget=TIME_BUDGET*2, map_size=200, result_folder='./results'),
                                            map_size=200,
                                            generator=KappaGenerator(20),
                                            name='KappaDefault',
                                            store_data=False)
        road_generator.start()

    def test_kappa_fix_step_generator(self):
        road_generator = TupleRoadGenerator(time_budget=TIME_BUDGET,
                                            executor=MockExecutor(time_budget=TIME_BUDGET*2, map_size=200, result_folder='./results'),
                                            map_size=200,
                                            generator=FixStepKappaGenerator(20),
                                            name='KappaFixStepDefault',
                                            store_data=False)
        road_generator.start()

    def test_catmull_rom_generator(self):
        road_generator = TupleRoadGenerator(time_budget=TIME_BUDGET,
                                            executor=MockExecutor(time_budget=TIME_BUDGET*2, map_size=200, result_folder='./results'),
                                            map_size=200,
                                            generator=CatmullRomGenerator(20),
                                            name='CatmullRomDefault',
                                            store_data=False)
        road_generator.start()
