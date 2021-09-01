from roadsearch.generators.representations.kappa_generator import FixStepKappaGenerator, KappaGenerator
from roadsearch.generators.representations.theta_generator import FixStepThetaGenerator, ThetaGenerator
from roadsearch.generators.representations.cartesian_generator import CatmullRomGenerator
from roadsearch.generators.representations.bezier_generator import BezierGenerator
from roadsearch.generators.samples.base import TupleRoadGenerator
import numpy as np

VARIATION = 0


# Generators that are represented with single variable arrays
class Frenetic(TupleRoadGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = FixStepKappaGenerator(
            length=25,
            variation=VARIATION,
            step=7.5,
            global_bound=0.07,
            local_bound=0.05
        )
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)


class FreneticStep(TupleRoadGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = KappaGenerator(
            length=28,
            variation=VARIATION,
            low_step=0.5,
            high_step=16.16,
            global_bound=0.08,
            local_bound=0.05
        )
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)


class TheTicStep(TupleRoadGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        step_mean = 9.47
        step_variance = 3.5
        generator = ThetaGenerator(
            length=19,
            variation=VARIATION,
            low_step=step_mean - step_variance,
            high_step=step_mean + step_variance,
            bound=np.pi/5,
            delta=np.pi/23
        )
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)


class TheTic(TupleRoadGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = FixStepThetaGenerator(
            length=36,
            variation=VARIATION,
            step=5,
            bound=np.pi/8,
            delta=np.pi/44
        )
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)


class DJGenerative(TupleRoadGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = CatmullRomGenerator(
            control_nodes=10,
            max_angle=50,
            seg_length=22.5,
            num_spline_nodes=10
        )
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)


class Bezier(TupleRoadGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = BezierGenerator(
            control_nodes=28,
            max_angle=40,
            seg_length=6.92,
            interpolation_nodes=9
        )
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)
