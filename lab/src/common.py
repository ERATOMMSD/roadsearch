import pandas as pd


def get_samples(main, representations, sample_size=None):
    if sample_size:
        sample = pd.DataFrame()
        for rep in representations:
            sample = sample.append(main[(main.representation == rep) & (main.outcome.isin(['PASS', 'FAIL'])) & (
                        main.method == 'random')].sample(sample_size))
    else:
        sample = main[(main.outcome.isin(['PASS', 'FAIL'])) & (main.method == 'random')]
    return sample
