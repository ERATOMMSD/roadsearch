import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
from lab.src.data_utils import latexify

sns.set_palette("muted")

distance_ndpf = 'distance ($d_{\mathrm{NDPF}}$)'


def plot_by_outcome(main, outcomes, x_label=""):
    main['repTeX'] = main.representation.apply(latexify)
    pt = pd.pivot_table(main[main.outcome.isin(outcomes)], values='test', index=['exp'], columns=['repTeX'], aggfunc='count', fill_value=0)
    fig, ax = plt.subplots(figsize=(8,2))
    sns.boxplot(ax=ax, data=pt, orient="h")
    ax.set_xlabel(x_label)
    ax.set_ylabel('')
    plt.tight_layout(pad=0.4, w_pad=0.6, h_pad=1.0)
    return fig


def plot_failures_by_method(main):
    outcomes = ['FAIL']
    main['repTeX'] = main.representation.apply(latexify)
    pt = pd.pivot_table(main[main.outcome.isin(outcomes)], values='test', index=['repTeX', 'exp', 'method'], aggfunc='count', fill_value=0)
    # filling with zero the cases with no data and reseting the index to transform multiindex into columns
    data = pt.unstack().fillna(0.0).stack().reset_index()
    fig = sns.catplot(data=data, x='method', y='test', hue='repTeX', kind='box', height=3.0, aspect=3.0, showfliers=False, legend_out=False)
    plt.ylabel('# failures')
    plt.xlabel('generator type')
    ax = fig.axes[0][0]
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles[0:], labels=labels[0:])
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    return fig


def plot_distances(distances, metric="procrustes_frechet_norm"):
    fig, ax = plt.subplots(figsize=(8,2))
    distances['repTeX'] = distances.representation.apply(latexify)
    _ = sns.boxplot(ax=ax, data=distances, y="repTeX", x=metric, showfliers=False)
    ylabel = metric
    if metric == "procrustes_frechet_norm":
        ylabel = distance_ndpf
    ax.set_xlabel(ylabel)
    ax.set_ylabel('')
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    return fig


def plot_similarity(data, metric = 'procrustes_frechet_norm', outliers = False, xlim=None):
    fig, ax = plt.subplots(figsize=(8,2))
    data['repTeX'] = data.representation.apply(latexify)
    sns.boxplot(ax=ax, data=data[(data.method==metric)], y='repTeX', x='value')    
    ax.set_xlabel('diversity')
    ax.set_ylabel('')
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    if xlim:
        plt.xlim(xlim)
    return fig


def plot_positions(distances, cols=2, size_h = 2.5, size_w = 6):
    
    decorators = {'theta+step': lambda x: '$\Delta_{\Theta}$' if x == 'first' else 'segment length',
                  'theta': lambda x: '$\Delta_{\Theta}$', 
                  'kappa': lambda x: '$\kappa$',
                  'kappa+step': lambda x: '$\kappa$' if x == 'first' else 'segment length', 
                  'bezier': lambda x: '$\Delta_{x}$' if x == 'first' else '$\Delta_{y}$', 
                  'cartesian': lambda x: '$\Delta_{x}$' if x == 'first' else '$\Delta_{y}$'}
    
    def plot_subgraph(axs, r, c, distances, rep, alt_value=10):
        
        if len(axs.shape) == 1:
            ax = axs[r]
        else:
            ax = axs[r][c]

        ax.set_title(f'{latexify(rep)}')

        data = distances[(distances.representation==rep) & (distances.value==alt_value)]

        x = list(map(int, data.pos.unique()))

        ax = sns.boxplot(ax=ax, data=data, x="pos", y="procrustes_frechet_norm", hue="type", showfliers=False, palette='muted')        

        # reducing the frquency of ticklabels to only even numbers
        modified_ticks = []
        for i, label in enumerate(ax.get_xticklabels()):
            if i % 2 != 0:
                modified_ticks.append('')
            else:
                modified_ticks.append(str(i))
        ax.set_xticklabels(modified_ticks)
        ax.set_ylabel(distance_ndpf)
        ax.set_xlabel('position of alteration')
        
        ax.legend(loc='upper right', borderaxespad=0, prop={'size':12})

        # renaming the legend to specific representation names
        for text in ax.get_legend().get_texts():
            text.set_text(decorators[rep](text.get_text()))
            #text.set_fontweight(100)
        
  
    
    rows = int(len(distances.representation.unique()) / cols)
 
    fig, axs = plt.subplots(rows, cols, figsize=(size_w*cols,size_h*rows))

    for i, rep in enumerate(distances.representation.unique()):
        plot_subgraph(axs, i//cols, i%cols, distances, rep)

    plt.subplots_adjust(wspace=0.1, hspace=0.5)
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    
    return fig


def plot_alterations_by_value(distances, plot_trends=False):

    fig = sns.catplot(data=distances, x="value", y="procrustes_frechet_norm", kind='box', hue='representationTex', height=3, aspect=2.5, showfliers=False, legend_out=False, palette="muted")

    if plot_trends:
        dotted_3 = (0, (1, 3))
        dotted_5 = (0, (1, 5))

        linestyles=[dotted_3, dotted_3, dotted_3, dotted_5, dotted_3, dotted_5]

        for rep, color, marker, linestyle in zip(data.representation.unique(), sns.color_palette("dark"), ['x','x','x','.','x','.'], linestyles):
            plt.plot(['10','20','30','40','50'], data[(data.representation==rep)].groupby('value').mean()['procrustes_frechet_norm'].values, linestyle=linestyle, label=rep, c=color, marker=marker, alpha=1.0, linewidth=3.0) # mec or mfc for different dot color
    plt.xlabel('alteration (%)')
    plt.ylabel(distance_ndpf)
    plt.legend()
    return fig
