import pandas as pd
import numpy as np
import itertools
import multiprocessing

from joblib import Parallel, delayed
from tqdm import tqdm
from data_utils import load_data
from common import get_samples
from utils.similarity import procrustes_frechet, simple_frechet
from utils.transform_functions import transformation_function
from utils.relative_angle_distance import relative_angle_distance, normalized_relative_angle_distance
from utils.normalized_distance import normalized_distance_value


def modify_test(i, t, x, alt, rep):
    def alter_value(test, pos, val):
        altered_test = np.copy(test)
        altered_test[pos] = altered_test[pos] * val
        return altered_test

    tf = transformation_function(rep)

    t_road = np.array(tf(t))

    if t.ndim > 1:
        multipliers = [np.ones(2)] * 3 + np.array([(1.0, 0.0), (0.0, 1.0), (1.0, 1.0)]) * alt
    else:
        multipliers = [1.0 + alt]

    data = []
    for mult in multipliers:
        modified = alter_value(t, x, mult)
        modified_road = np.array(tf(modified))
        f, p, rad, nrad = simple_frechet(t_road, modified_road), \
                          procrustes_frechet(t_road, modified_road), \
                          relative_angle_distance(t_road, modified_road), \
                          normalized_relative_angle_distance(t_road, modified_road)

        data.append({'id': i,
                     'pos': x,
                     'alteration': mult,
                     'frechet': f,
                     'procrustes_frechet': p,
                     'frechet_norm': normalized_distance_value(f, t_road, modified_road),
                     'procrustes_frechet_norm': normalized_distance_value(p, t_road, modified_road),
                     'relative_angle_distance': rad,
                     'normalized_relative_angle_distance': nrad,
                     'representation': rep})
    return data


def sample_alterations(sample_size=None, alterations=None, representations=None):
    main = load_data(force=False)

    if not representations:
        representations = main.representation.unique()

    if not alterations:
        alterations = [0.1, 0.2, 0.3, 0.4, 0.5]

    sample = get_samples(main, representations, sample_size)

    all_jobs = []

    # iterating representations
    for rep in representations:
        # iterating samples
        for i, t in sample[sample.representation == rep].test.items():
            prod = list(itertools.product(range(t.shape[0]), alterations))
            all_jobs.extend([(i, t, x, alt, rep) for x, alt in prod])

    out = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(modify_test)(*params) for params in tqdm(all_jobs))
    data = itertools.chain.from_iterable(out)

    distances = pd.DataFrame(data)
    return sample, distances


if __name__ == "__main__":
    sample, distances = sample_alterations()
    sample.to_json(f'./data/alterations_sample.json')
    distances.to_json(f'./data/alterations_distances.json')
