from roadsearch.generators.virtual_road_generator import VirtualRoadsGenerator
from roadsearch.generators.representations.kappa_generator import KappaGenerator, FixStepKappaGenerator
from roadsearch.generators.representations.theta_generator import FixStepThetaGenerator, ThetaGenerator
from roadsearch.generators.representations.cartesian_generator import CatmullRomGenerator
from roadsearch.generators.mutators.mutations import ValueAlterationMutator, ValueAlterationMutatorKappaStep
from roadsearch.generators.exploiters.exploiters import SingleVariableExploiter, Exploiter
from roadsearch.generators.crossovers.crossovers import Crossover
import numpy as np

# Crossover setup
CROSS_FREQ = 30
CROSS_SIZE = 20

# Step sizes: distance between two nodes
FIX_STEP = 10.0
LOW_STEP = 5.0
HIGH_STEP = 15.0

# Number of nodes and variation in the length of the random generation
LENGTH = 20
VARIATION = 0

# Bounds for theta generation
BOUND = np.pi/6
DELTA = np.pi/8


# Generators that are represented with single variable arrays
class Frenetic(VirtualRoadsGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = FixStepKappaGenerator(length=LENGTH, variation=VARIATION, step=FIX_STEP)
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size,
                         random_budget=time_budget*0.1,
                         strict_father=False,
                         generator=generator,
                         mutator=ValueAlterationMutator(),
                         exploiter=SingleVariableExploiter(),
                         crossover=Crossover(size=CROSS_SIZE, frequency=CROSS_FREQ))


class TheTic(VirtualRoadsGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = FixStepThetaGenerator(length=LENGTH, variation=VARIATION, step=FIX_STEP, bound=BOUND, delta=DELTA)
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size,
                         random_budget=time_budget*0.1,
                         strict_father=False,
                         generator=generator,
                         mutator=ValueAlterationMutator(),
                         exploiter=SingleVariableExploiter(),
                         crossover=Crossover(size=CROSS_SIZE, frequency=CROSS_FREQ))

# Generators based on representations modelled with tuple arrays


class TupleRoadGenerator(VirtualRoadsGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None, generator=None, name=None, store_data=True):
        self.name = name

        if isinstance(generator, KappaGenerator):
            # Using special mutator for kappa+step generator because the last step is not used
            mutator = ValueAlterationMutatorKappaStep()
        else:
            mutator = ValueAlterationMutator()

        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size,
                         random_budget=time_budget*0.1,
                         strict_father=False,
                         generator=generator,
                         mutator=mutator,
                         exploiter=Exploiter(),
                         crossover=Crossover(size=CROSS_SIZE, frequency=CROSS_FREQ),
                         store_data=store_data)

    # Quick hack to rename the generator when creating custom configurations
    def get_name(self):
        if self.name:
            return self.name
        else:
            return super().get_name()


class FreneticStep(TupleRoadGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = KappaGenerator(length=LENGTH, variation=VARIATION, low_step=LOW_STEP, high_step=HIGH_STEP)
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)


class TheTicStep(VirtualRoadsGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = ThetaGenerator(length=LENGTH, variation=VARIATION, low_step=LOW_STEP, high_step=HIGH_STEP, bound=BOUND, delta=DELTA)
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)


class DJGenerative(VirtualRoadsGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = CatmullRomGenerator(control_nodes=10, max_angle=50, seg_length=30, num_spline_nodes=20)
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)


# Generators that are purely random

class RandomGenerator(VirtualRoadsGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None, generator=None):
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size,
                         random_budget=time_budget,
                         strict_father=False,
                         generator=generator)


class RandomFrenetic(RandomGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = FixStepKappaGenerator(length=LENGTH, variation=VARIATION, step=FIX_STEP)
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)


class RandomFreneticStep(RandomGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = KappaGenerator(length=LENGTH, variation=VARIATION, low_step=LOW_STEP, high_step=HIGH_STEP)
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)


class RandomTheTic(RandomGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = FixStepThetaGenerator(length=LENGTH, variation=VARIATION, step=FIX_STEP, bound=BOUND, delta=DELTA)
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)


class RandomTheTicStep(RandomGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = ThetaGenerator(length=LENGTH, variation=VARIATION, low_step=LOW_STEP, high_step=HIGH_STEP, bound=BOUND, delta=DELTA)
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)


class RandomDJGenerator(RandomGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        generator = CatmullRomGenerator(control_nodes=LENGTH, variation=VARIATION)
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, generator=generator)
