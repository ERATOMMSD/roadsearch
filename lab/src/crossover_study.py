import pandas as pd
import itertools
import multiprocessing
import random
import numpy as np

from joblib import Parallel, delayed
from tqdm import tqdm
from typing import List
from data_utils import load_data
from common import get_samples
from utils.similarity import procrustes_frechet, simple_frechet
from utils.transform_functions import transformation_function
from utils.normalized_distance import normalized_distance_value


def chromosome_crossover(parent_1: List, parent_2: List):
    """
        parent_1: list of test
        parent_2: list of test
        returns: a list of test of the length of the shortest list
    """
    child_1 = []
    child_2 = []
    for i in range(min(len(parent_1), len(parent_2))):
        if random.random() < 0.5:
            child_1.append(parent_1[i])
            child_2.append(parent_2[i])
        else:
            child_1.append(parent_2[i])
            child_2.append(parent_1[i])

    return [child_1, child_2]


def compare_children(parent_id_1, parent_test_1, parent_id_2, parent_test_2, representation, reproduction=5):
    transform = transformation_function(representation)

    data = []

    parents_road = list(map(lambda x: np.array(transform(x)), [parent_test_1, parent_test_2]))

    for i in range(reproduction):

        children = chromosome_crossover(parent_test_1, parent_test_2)
        children_road = list(map(lambda x: np.array(transform(x)), children))

        for child, parent in itertools.product(children_road, parents_road):
            frechet, procrustes = simple_frechet(parent, child), procrustes_frechet(parent, child)
            data.append({
                'representation': representation,
                'parent_id_1': parent_id_1,
                'parent_id_2': parent_id_2,
                'child': child,
                'parent': parent,
                'child_intent': i,
                'frechet': frechet,
                'procrustes_frechet': procrustes,
                'frechet_norm': normalized_distance_value(frechet, child, parent),
                'procrustes_frechet_norm': normalized_distance_value(procrustes, child, parent),
            })

    return data


def sample_crossover(sample_size=None, representations=None):
    main = load_data(force=False)

    if not representations:
        representations = main.representation.unique()

    sample = get_samples(main, representations, sample_size)

    all_jobs = []

    # iterating representations
    for rep in representations:
        rep_sample = sample[sample.representation == rep]['test']
        all_jobs.extend(
            [(k1, r1, k2, r2, rep) for (k1, r1), (k2, r2) in itertools.product(rep_sample.items(), rep_sample.items())
             if k1 < k2])

    out = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(compare_children)(*params) for params in tqdm(all_jobs))
    data = itertools.chain.from_iterable(out)

    distances = pd.DataFrame(data)
    return sample, distances


if __name__ == "__main__":
    sample, distances = sample_crossover()
    sample.to_json(f'./data/crossover_sample.json')
    distances.to_json(f'./data/crossover_distances.json')
