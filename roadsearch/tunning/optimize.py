#
#
#
#
# Base code borrowed from https://github.com/se2p/tool-competition-av/blob/main/competition.py
import traceback
import time
import os
import sys
import errno
import logging as log
import click
from sbst_beamng.code_pipeline.tests_generation import TestGenerationStatistic

OUTPUT_RESULTS_TO = 'results'


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def validate_map_size(ctx, param, value):
    if value < 100 or value > 1000:
        raise click.UsageError(
            'The provived value for ' + str(param) + ' is invalid. Choose an integer between 100 and 1000')
    else:
        return value


def validate_time_budget(ctx, param, value):
    if value <= 0:
        raise click.UsageError('The provived value for ' + str(param) + ' is invalid. Choose a positive integer')
    else:
        return value


def create_summary(result_folder, raw_data):
    if type(raw_data) is TestGenerationStatistic:
        summary_file = os.path.join(result_folder, "generation_stats.csv")
        csv_content = raw_data.as_csv()
        with open(summary_file, 'w') as output_file:
            output_file.write(csv_content)


def post_process(result_folder, the_executor):
    """
        This will be invoked after the generation is over. Whatever results is produced will be copied inside
        the result_folder
    """
    # Ensure the executor is stopped
    the_executor.close()

    log.info("Test Generation Statistics:")
    log.info(the_executor.get_stats())
    create_summary(result_folder, the_executor.get_stats())


def create_post_processing_hook(result_folder, executor):
    """
        Uses HighOrder functions to setup the post processing hooks that will be trigger ONLY AND ONLY IF the
        test generation has been killed by us, i.e., this will not trigger if the user presses Ctrl-C

    :param result_folder:
    :param executor:
    :return:
    """

    def _f():
        if executor.is_force_timeout():
            # The process killed itself because a timeout, so we need to ensure the post_process function
            # is called
            post_process(result_folder, executor)

    return _f


def log_exception(extype, value, trace):
    log.exception('Uncaught exception:', exc_info=(extype, value, trace))


def setup_logging(log_to, debug):
    # Disable annoyng messages from matplot lib.
    # See: https://stackoverflow.com/questions/56618739/matplotlib-throws-warning-message-because-of-findfont-python
    log.getLogger('matplotlib.font_manager').disabled = True

    term_handler = log.StreamHandler()
    log_handlers = [term_handler]
    start_msg = "Started test generation"

    if log_to is not None:
        file_handler = log.FileHandler(log_to, 'a', 'utf-8')
        log_handlers.append(file_handler)
        start_msg += " ".join(["writing to file: ", str(log_to)])

    log_level = log.DEBUG if debug else log.INFO

    log.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=log_level, handlers=log_handlers)

    sys.excepthook = log_exception

    log.info(start_msg)


def setup_default_directory():
    default_output_folder = os.path.join(get_script_path(), OUTPUT_RESULTS_TO)
    try:
        os.makedirs(default_output_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return default_output_folder


def setup_executor(beamng_home, beamng_user, executor, map_size, road_visualizer, time_budget):
    the_executor = None
    # Setup executor
    if executor == "mock":
        from sbst_beamng.code_pipeline.executors import MockExecutor
        the_executor = MockExecutor(time_budget=time_budget, map_size=map_size, road_visualizer=road_visualizer)
    elif executor == "beamng":
        # TODO Make sure this executor outputs the files in the results folder
        from sbst_beamng.code_pipeline.beamng_executor import BeamngExecutor
        the_executor = BeamngExecutor(beamng_home=beamng_home, beamng_user=beamng_user, time_budget=time_budget,
                                      map_size=map_size, road_visualizer=road_visualizer)
    return the_executor


def create_directory(default_output_folder, module_name, class_name=None):
    # Create the unique folder that will host the results of this execution using the test generator data and
    # a timestamp as id
    timestamp_id = time.time_ns() // 1000000
    result_folder = os.path.join(default_output_folder,
                                 "_".join([l for l in [str(module_name), str(class_name), str(timestamp_id)] if l]))
    try:
        os.makedirs(result_folder)
    except OSError:
        log.fatal("An error occurred during test generation")
        traceback.print_exc()
        sys.exit(2)
    log.info("Outputting results to " + result_folder)
    return result_folder


from roadsearch.tunning.generators_spaces import get_space_and_transformer

from sbst_beamng.code_pipeline.visualization import RoadTestVisualizer
from sbst_beamng.code_pipeline.test_generation_utils import register_exit_fun
from roadsearch.tunning.parameter_study import HyperParameterStudy


def validate_generator(ctx, param, value):
    valid_inputs = ['kappa', 'kappa_fix_step', 'theta', 'theta_fix_step', 'deepjanus', 'bezier']
    if value in valid_inputs:
        return value
    else:
        raise click.UsageError(f'The provided value for {param} is invalid. Available options: {valid_inputs}')


@click.command()
@click.option('--executor', type=click.Choice(['mock', 'beamng'], case_sensitive=False), default="mock",
              show_default='Mock Executor (meant for debugging)',
              help="The name of the executor to use. Currently we have 'mock' or 'beamng'.")
@click.option('--beamng-home', required=False, default=None, type=click.Path(exists=True),
              show_default='None',
              help="Customize BeamNG executor by specifying the home of the simulator.")
@click.option('--beamng-user', required=False, default=None, type=click.Path(exists=True),
              show_default='Currently Active User (~/BeamNG.research/)',
              help="Customize BeamNG executor by specifying the location of the folder "
                   "where levels, props, and other BeamNG-related data will be copied."
                   "** Use this to avoid spaces in URL/PATHS! **")
@click.option('--time-budget', required=True, type=int, callback=validate_time_budget,
              help="Overall budget for the generation and execution. Expressed in 'real-time'"
                   "seconds.")
@click.option('--map-size', type=int, default=200, callback=validate_map_size,
              show_default='200m, which leads to a 200x200m^2 squared map',
              help="The lenght of the size of the squared map where the road must fit."
                   "Expressed in meters.")
@click.option('--generator-name', required=True, type=str, callback=validate_generator,
              help="Name of the module where your test generator is located.")
# Visual Debugging
@click.option('--visualize-tests', required=False, is_flag=True, default=False,
              show_default='Disabled',
              help="Visualize the last generated test, i.e., the test sent for the execution. "
                   "Invalid tests are also visualized.")
# Logging options
@click.option('--log-to', required=False, type=click.Path(exists=False),
              help="Location of the log file. If not specified logs appear on the console")
@click.option('--debug', required=False, is_flag=True, default=False,
              show_default='Disabled',
              help="Activate debugging (results in more logging)")
@click.option('--trials', type=int, default=10, callback=validate_time_budget,
              show_default='By default the optimizer does 10 trials.',
              help="Number of trials done by the optimizer.")
@click.option('--pruning-sample', type=int, default=10, callback=validate_time_budget,
              show_default='By default the number of samples is 10.',
              help="Number of samples executed by the optimizer to check if the trial should be pruned.")
def optimize(executor, beamng_home, beamng_user, time_budget, map_size, generator_name,
             visualize_tests, log_to, debug, trials, pruning_sample):
    # Setup logging
    setup_logging(log_to, debug)

    road_visualizer = None
    # Setup visualization
    if visualize_tests:
        road_visualizer = RoadTestVisualizer(map_size=map_size)

    # Setup folder structure by ensuring that the basic folder structure is there.
    default_output_folder = setup_default_directory()

    result_folder = create_directory(default_output_folder, generator_name)

    # executor is being reused through the study (extra time just in case)
    the_executor = setup_executor(beamng_home, beamng_user, executor, map_size, road_visualizer, time_budget * trials * 2)

    config_to_generator, space_labels = get_space_and_transformer(generator_name)

    # Register the shutdown hook for post processing results
    register_exit_fun(create_post_processing_hook(result_folder, the_executor))

    study = HyperParameterStudy(space_labels=space_labels,
                                trials=trials,
                                trial_budget=time_budget,
                                pruning_sample=pruning_sample,
                                map_size=map_size,
                                executor=the_executor,
                                config_to_generator=config_to_generator)

    study.run_study(directory=default_output_folder)

    # We still need this here to post process the results if the execution takes the regular flow
    post_process(result_folder, the_executor)


if __name__ == '__main__':
    optimize()
