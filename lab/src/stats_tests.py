import pandas as pd
import numpy as np 
from scipy.stats import mannwhitneyu
# null hypothesis: they are the same
# alternative: they are different 
from lab.src.utils.a12 import a12


def u_test_by_representations(subject, representations):
    test_df = pd.DataFrame(columns=representations)

    for rep_1 in representations:
        data = {'subject': rep_1}
        for rep_2 in representations:
            if rep_1 < rep_2:
                u_test = mannwhitneyu(subject[rep_1].dropna(), subject[rep_2].dropna())
                data[rep_2] = u_test.pvalue
            else:
                data[rep_2] = np.nan
        test_df = test_df.append(data, ignore_index=True)

    return test_df.set_index('subject')

def u_test_a12_by_representation(subject, representations, ci = 0.05):
    test_df = pd.DataFrame(columns=representations)

    for rep_1 in representations:
        data = {'subject': rep_1}
        for rep_2 in representations:
            if rep_1 != rep_2:
                u_test = mannwhitneyu(subject[rep_1].dropna(), subject[rep_2].dropna())
                if u_test.pvalue > ci:
                    data[rep_2] = '\same'
                else:
                    a12_res = a12(subject[rep_1].dropna(), subject[rep_2].dropna())
                    if a12_res > 0.5:
                        data[rep_2] = '\\better ({:.3g})'.format(a12_res)
                    else:
                        data[rep_2] = '\\worse ({:.3g})'.format(a12_res)
            else:
                data[rep_2] = '-'
                
        test_df = test_df.append(data, ignore_index=True)

    return test_df.set_index('subject')

def pretty_latex(test_df, cols=7):
    print(test_df.to_latex(na_rep='-', float_format="{:0.2g}".format, escape=False, index_names=False, column_format="c"*cols))