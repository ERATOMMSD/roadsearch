from typing import Tuple
import numpy as np

from roadsearch.generators.representations.kappa_generator import KappaGenerator, FixStepKappaGenerator
from roadsearch.generators.representations.theta_generator import ThetaGenerator, FixStepThetaGenerator
from roadsearch.generators.representations.cartesian_generator import CatmullRomGenerator
from roadsearch.generators.representations.bezier_generator import BezierGenerator
from roadsearch.generators.representations.road_generator import RoadGenerator


class NoGeneratorFound(Exception):
    pass


def get_space_and_transformer(generator_type):
    # Using fix total length of map_size(200) - margin(10) * 2
    ROAD_LENGTH = 180

    if generator_type == 'kappa':

        kappa_space_labels = {'length': (10, 50, 1),
                              'step_variance': (0.5, 10.0, 0.5),
                              'global_bound': (0.01, 0.1, 0.01),
                              'local_bound': (0.01, 0.1, 0.01)}

        def config_to_kappa_generator(config) -> Tuple[RoadGenerator, str]:

            config['step_mean'] = ROAD_LENGTH / (config['length'] - 1)

            generator = KappaGenerator(length=config['length'],
                                       low_step=max(0.5, config['step_mean'] - config['step_variance']),
                                       high_step=config['step_mean'] + config['step_variance'],
                                       global_bound=config['global_bound'],
                                       local_bound=config['local_bound'])

            name = f"KappaGenerator_l{config['length']}_sm{config['step_mean']}_sv_{config['step_variance']}_gb{config['global_bound']}_lb{config['local_bound']}"

            return generator, name

        return config_to_kappa_generator, kappa_space_labels

    elif generator_type == 'kappa_fix_step':

        kappa_fix_start_space_labels = {'length': (10, 50, 1),
                                        'global_bound': (0.01, 0.1, 0.01),
                                        'local_bound': (0.01, 0.1, 0.01)}

        def config_to_kappa_fix_step_generator(config) -> Tuple[RoadGenerator, str]:

            config['step'] = ROAD_LENGTH / (config['length'] - 1)

            generator = FixStepKappaGenerator(length=config['length'],
                                              step=config['step'],
                                              global_bound=config['global_bound'],
                                              local_bound=config['local_bound'])

            name = f"FixStepKappaGenerator_l{config['length']}_s{config['step']}_gb{config['global_bound']}_lb{config['local_bound']}"

            return generator, name

        return config_to_kappa_fix_step_generator, kappa_fix_start_space_labels

    elif generator_type == 'theta':

        theta_space_labels = {'length': (10, 50, 1),
                              'step_variance': (0.5, 10.0, 0.5),
                              'bound': (1, 48, 1),
                              'delta': (1, 48, 1)}

        def config_to_theta_generator(config) -> Tuple[RoadGenerator, str]:

            config['step_mean'] = ROAD_LENGTH / config['length']

            generator = ThetaGenerator(length=config['length'],
                                       low_step=max(0.5, config['step_mean'] - config['step_variance']),
                                       high_step=config['step_mean'] + config['step_variance'],
                                       bound=np.pi / config['bound'],
                                       delta=np.pi / config['delta'])

            name = f"ThetaGenerator_l{config['length']}_sm{config['step_mean']}_sv_{config['step_variance']}_b{config['bound']}_d{config['delta']}"

            return generator, name

        return config_to_theta_generator, theta_space_labels

    elif generator_type == 'theta_fix_step':

        theta_fix_start_space_labels = {'length': (10, 50, 1),
                                        'bound': (1, 48, 1),
                                        'delta': (1, 48, 1)}

        def config_to_theta_fix_step_generator(config) -> Tuple[RoadGenerator, str]:

            config['step'] = ROAD_LENGTH / config['length']

            generator = FixStepThetaGenerator(length=config['length'],
                                              step=config['step'],
                                              bound=np.pi / config['bound'],
                                              delta=np.pi / config['delta'])

            name = f"FixStepThetaGenerator_l{config['length']}_s{config['step']}_b{config['bound']}_d{config['delta']}"

            return generator, name

        return config_to_theta_fix_step_generator, theta_fix_start_space_labels

    elif generator_type == 'deepjanus':

        deepjanus_space_labels = {'control_nodes': (10, 50, 1),
                                  'max_angle': (10, 90, 5),
                                  'num_spline_nodes': (5, 10, 1)}

        def config_to_deepjanus_generator(config) -> Tuple[RoadGenerator, str]:

            config['seg_length'] = ROAD_LENGTH / (config['control_nodes'] - 2)

            generator = CatmullRomGenerator(control_nodes=config['control_nodes'],
                                            max_angle=config['max_angle'],
                                            seg_length=config['seg_length'],
                                            num_spline_nodes=config['num_spline_nodes'])

            name = f"DeepJanusGenerator_c{config['control_nodes']}_ma{config['max_angle']}_sl{config['seg_length']}_spl{config['num_spline_nodes']}"

            return generator, name

        return config_to_deepjanus_generator, deepjanus_space_labels

    elif generator_type == 'bezier':

        bezier_space_labels = {'control_nodes': (10, 50, 1),
                               'max_angle': (10, 90, 5),
                               'interpolation_nodes': (5, 10, 1)}

        def config_to_bezier_generator(config) -> Tuple[RoadGenerator, str]:

            config['seg_length'] = ROAD_LENGTH / (config['control_nodes'] - 2)

            generator = BezierGenerator(control_nodes=config['control_nodes'],
                                        max_angle=config['max_angle'],
                                        seg_length=config['seg_length'],
                                        interpolation_nodes=config['interpolation_nodes'])

            name = f"BezierGenerator_c{config['control_nodes']}_ma{config['max_angle']}_sl{config['seg_length']}_int{config['interpolation_nodes']}"

            return generator, name

        return config_to_bezier_generator, bezier_space_labels

    else:
        raise NoGeneratorFound(
            "The only generators available are kappa, kappa_fix_step, theta, theta_fix_step, and deepjanus.")
