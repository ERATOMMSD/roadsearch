import logging as log
import numpy as np
import pandas as pd
import optuna
import joblib
from optuna.samplers import TPESampler
from optuna import TrialPruned

import sys
sys.path.append('../../../')
from roadsearch.generators.samples.base import TupleRoadGenerator


class HyperParameterStudy:

    def __init__(self, space_labels, trials, trial_budget, map_size, executor, pruning_sample, config_to_generator):
        self.trials = trials
        self.trial_budget = trial_budget
        self.total_budget = trial_budget * trials
        self.map_size = map_size
        self.executor = executor
        self.space_labels = space_labels
        self.df = pd.DataFrame()
        # Number of samples to determine if the trial should be pruned
        self.pruning_sample = pruning_sample
        self.config_to_generator = config_to_generator

    def setup_generator(self, suggestion):
        config = dict(zip(self.parameters(), suggestion))
        generator, name = self.config_to_generator(config)
        road_generator = TupleRoadGenerator(time_budget=self.trial_budget, executor=self.executor,
                                            map_size=self.map_size, generator=generator, name=name)

        return road_generator

    def evaluate(self, suggestion) -> float:
        stats = None
        # default score in case of an error
        score = 2
        # Instantiate the test generator
        test_generator = self.setup_generator(suggestion)

        # Obtaining X initial samples to check if the configuration produces valid tests
        try:
            test_generator.sample_random(self.pruning_sample)
            stats = test_generator.stats
        except TimeoutError:
            log.info('Initial sampling produced time out error... Trial will be pruned.')
        except Exception:
            log.critical('Error during the initial sampling...')

        # if less than 20% of the samples are valid or no test passes the min_threshold for mutation
        if (not stats or stats['PASS'] + stats['FAIL'] < 0.2 * self.pruning_sample or
                np.min(test_generator.min_oob_distances) > test_generator.min_oobd_threshold):
            raise TrialPruned()
        try:
            # Resuming generation (previous samples and time spent count)
            test_generator.start()
            stats = test_generator.stats
            score = - stats['FAIL'] + np.mean(test_generator.min_oob_distances)
            log.info(f'Optimizer suggestion: {dict(zip(self.parameters(), suggestion))}')
        except TimeoutError:
            log.info("Time out error: One of the trials didn't finish within the expected time...")
        except Exception as e:
            log.critical('Test generation failed... last score will be yielded.')
            log.critical(e)
            import pdb
            pdb.set_trace()

        self.df = self.df.append({**dict(zip(self.parameters(), suggestion)), 'score': score}, ignore_index=True)

        return score

    def parameters(self):
        return sorted(self.space_labels.keys())

    def objective(self, trial):
        suggestion = []
        for p in self.parameters():
            low, upper, step = self.space_labels[p]
            if type(low) == int:
                s = trial.suggest_int(p, low, upper, step)
            else:
                s = trial.suggest_discrete_uniform(p, low, upper, step)
            suggestion.append(s)
        return self.evaluate(suggestion)

    def best_parameters(self):
        return list(self.df.iloc[self.df['score'].argmax()].loc[self.parameters()])

    def run_study(self, directory=None):
        study = optuna.create_study(direction='minimize', sampler=TPESampler())
        study.optimize(self.objective, n_trials=self.trials, timeout=self.total_budget)
        if directory:
            self.store_study(directory, study)
            self.store_df(directory)

    def store_study(self, directory, study):
        filename = '{:s}/study.pkl'.format(directory)
        joblib.dump(study, filename)

    def store_df(self, directory):
        filename = '{:s}/train.csv'.format(directory)
        log.info(f'Storing results in {filename}')
        self.df.to_csv(filename)
        return filename
