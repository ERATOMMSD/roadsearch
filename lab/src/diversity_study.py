import pandas as pd
import itertools
import multiprocessing
from joblib import Parallel, delayed
from tqdm import tqdm
from data_utils import load_data
from similaritymeasures import pcm, area_between_two_curves
from utils.similarity import procrustes_frechet, simple_frechet, move_rotate
from utils.normalized_distance import normalized_distance_value


def similarity(k1, r1, o1, k2, r2, o2, experiment, representation):
    measures = [pcm,
                simple_frechet,
                area_between_two_curves,
                procrustes_frechet,
                lambda x, y: normalized_distance_value(simple_frechet(x, y), x, y),
                lambda x, y: normalized_distance_value(procrustes_frechet(x, y), x, y)
                ]

    stats = dict(zip(['pcm', 'frechet', 'area', 'procrustes_frechet', 'frechet_norm', 'procrustes_frechet_norm'],
                     list(map(lambda x: x(r1, r2), measures))))
    stats['representation'] = representation
    stats['experiment'] = experiment
    stats['id_1'] = k1
    stats['id_2'] = k2
    stats['outcome_1'] = o1
    stats['outcome_2'] = o2

    return stats


def extract_similarities(failed_only=True, rotate=True, frac=1.0, representations=None):
    df = load_data(force=False)

    if not representations:
        representations = df.representation.unique()

    all_jobs = []

    if rotate:
        df['road'] = df['road'].apply(move_rotate)

    for rep, exp in itertools.product(representations, df.exp.unique()):

        if failed_only:
            sample = df[(df['exp'] == exp) & (df['outcome'] == 'FAIL') & (df['representation'] == rep)][
                ['road', 'outcome']].transpose()
        else:
            sample = df[(df['exp'] == exp) & (df['outcome'].isin(['FAIL', 'PASS'])) & (df['representation'] == rep)][
                ['road', 'outcome']].transpose()

        if 0.0 < frac < 1.0:
            sample = sample.sample(frac=frac)

        all_jobs.extend([(k1, r1[0], r1[1], k2, r2[0], r2[1], exp, rep) for (k1, r1), (k2, r2) in
                         itertools.product(sample.items(), sample.items()) if k1 < k2])

    out = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(similarity)(*params) for params in tqdm(all_jobs))

    sdf = pd.DataFrame(out)

    return sdf


if __name__ == "__main__":
    res = extract_similarities(failed_only=False)
    res.to_json(f'./data/similarities.json')
