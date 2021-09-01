import pandas as pd
import os
import numpy as np
import time
import ast


def load_experiment(sub_dir):
    name = next(os.walk(f'./data/raw/simulations/{sub_dir}/experiments/'))[2][0]
    file_name = f'./data/raw/simulations/{sub_dir}/experiments/{name}'
    generator = sub_dir.split('_')[-1]
    df = pd.read_csv(file_name)
    return df


def transform_data(master):
    # transforming them back from str to arrays         
    master['road'] = master['road'].apply(lambda x: np.array(ast.literal_eval(x)))
    master['test'] = master['test'].apply(lambda x: np.array(ast.literal_eval(x)))
    master['last_pos'] = master['last_pos'].apply(lambda x: ast.literal_eval(x) if x is not np.nan else None)
    return master


def latexify(x):
    tex_name = {'cartesian': '$Cartesian_{\\mathit{Cat}}$', 
                'bezier': '$Cartesian_{\\mathit{Bez}}$',
                'theta': '$Theta$', 
                'theta+step': '$Theta_{\\mathit{Step}}$', 
                'kappa': '$Kappa$',
                'kappa+step': '$Kappa_{\\mathit{Step}}$'}
    return tex_name[x]


def aggregate_data():
    start = time.time()
    #ignoring hidden directories
    sub_directories = sorted([d for d in list(next(os.walk('./data/raw/simulations/'))[1]) if d[0] != '.'])

    master = pd.DataFrame()

    rename = {'DJGenerative': 'cartesian',
              'TheTicStep': 'theta+step',
              'TheTic': 'theta',
              'Frenetic': 'kappa',
              'FreneticStep': 'kappa+step',
              'Bezier': 'bezier'}
    
    
    rename_method = {'random' : 'random', 
                     'alter the values by 0.9 ~ 1.1': 'alteration', 
                     'reverse test': 'reverse',
                     'split and swap test': 'swap', 
                     'chromosome crossover': 'crossover'}
    
    count = 0

    #iterating each subfolder
    for i, sub_dir in enumerate(sub_directories):
        [exp, budget, map_size, representation] = sub_dir.split('_')
        df = load_experiment(sub_dir)
        df['budget'] = int(budget)
        df['map_size'] = int(map_size)
        df['representation'] = rename[representation]
        df['exp'] = int(exp[3:])
        master = master.append(df, ignore_index=True)
        count+=1
        
    master = transform_data(master)
    
    master.method = master.method.apply(lambda x: rename_method[x])
    
    print(f'Files aggregated in {time.time() - start} seconds.')
    return master


def load_data(reload=False):
    start = time.time()
    if reload or not os.path.isfile('./data/summary/data.json'):
        main = aggregate_data()
        main.to_json('./data/summary/data.json')
    else:    
        #re-loading the data for validation
        main = pd.read_json('./data/summary/data.json')
        main['road'] = main['road'].apply(np.array)
        main['test'] = main['test'].apply(np.array)
    print(f'Aggregated data loaded in {time.time()-start} seconds.')
    return main


def aggregate_data_by_representation(sub_folder):
    representations = ['bezier', 'catmull','kappa', 'kappa+step', 'theta', 'theta+step']
    
    data = pd.DataFrame()
    
    for rep in representations:
        rep_df = pd.read_json(f'./data/raw/{sub_folder}/{rep}.json')
        data = data.append(rep_df, ignore_index=True)
        
    return data


def load_crossover(reload=False):
    if reload or not os.path.isfile('./data/summary/crossover.json'):
        data = aggregate_data_by_representation('crossover')
        summary = data.drop(columns=['child','parent'])
        summary.to_json('./data/summary/crossover.json')
    else:
        summary = pd.read_json('./data/summary/crossover.json')
    
    return summary


def load_similarities(reload=False):
    if reload or not os.path.isfile('./data/summary/similarity_failures.json') or not os.path.isfile('./data/summary/similarity.json'):
        df = aggregate_data_by_representation(sub_folder='similarities')
        
        # creating summary pivot table for similarity
        pt = pd.pivot_table(df, values=['area', 'frechet', 'procrustes_frechet', 'pcm', 'procrustes_frechet_norm', 'frechet_norm'], index=['experiment'], columns=['representation'], aggfunc=np.mean, fill_value=0)
        mpt = pt.melt()
        mpt.columns = ['method', 'representation', 'value']
        mpt.to_json('./data/summary/similarity.json')
        
        # creating summary pivot table for similarity of failures
        ptf = pd.pivot_table(df[(df.outcome_1 =='FAIL') & (df.outcome_2 == 'FAIL')], values=['area', 'frechet', 'procrustes_frechet', 'pcm', 'procrustes_frechet_norm', 'frechet_norm'], index=['experiment'], columns=['representation'], aggfunc=np.mean)
        mptf = ptf.melt()
        mptf.columns = ['method', 'representation', 'value']
        mptf.to_json('./data/summary/similarity_failures.json')
    else:
        mpt = pd.read_json('./data/summary/similarity.json')
        mptf = pd.read_json('./data/summary/similarity_failures.json') 
    return mpt, mptf


def load_alteration_distances():
    distances = aggregate_data_by_representation(sub_folder='alterations')
    
    def parse(x):
        return {1.1: 10, 1.2: 20, 1.3: 30, 1.4: 40, 1.5: 50}[x]

    # separating alteration array into two columns
    distances['value'] = distances.alteration.apply(lambda x: parse(x) if type(x) == float else parse(x[0]) if x[0] != 1.0 else parse(x[1]))
    distances['type'] = distances.alteration.apply(lambda x: 'single' if type(x) == float else 'both' if x[0]==x[1] else 'first' if x[0] != 1.0 else 'second')
    
    lengths = {}
    for rep in distances.representation.unique():
        max_len = distances[distances.representation == rep].pos.max()
        lengths[rep] = max_len
        
    # adding additional columns to aggregate values
    distances['pos_percentage'] = distances['pos'] / distances['representation'].apply(lambda x: lengths[x])
    distances['bucket_5'] = pd.qcut(distances['pos_percentage'], q=5)
    distances['bucket_10'] = pd.qcut(distances['pos_percentage'], q=10)
    
    # only retrieving information of independent modifications
    distances = distances[~(distances.type=='both')]

    # skipping the first two control nodes since they are always placed along the y axis
    distances = distances[~((distances.pos<2) & (distances.representation.isin(['cartesian','bezier'])))]
    
    # adding latex naming
    distances['representationTex'] = distances.representation.apply(latexify)
    
    return distances
