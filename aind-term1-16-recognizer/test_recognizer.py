import os
import sys
import traceback

import math
import numpy as np
import pandas as pd

from asl_data import AslDb
from asl_utils import test_features_tryit

from my_recognizer import recognize
from asl_utils import show_errors
from my_model_selectors import SelectorConstant
from my_model_selectors import SelectorBIC
from my_model_selectors import SelectorDIC
from my_model_selectors import SelectorCV

from pathlib import Path
import pickle

def setup_features_ground(asl):
    asl.df['grnd-rx'] = asl.df['right-x'] - asl.df['nose-x']
    asl.df['grnd-ry'] = asl.df['right-y'] - asl.df['nose-y']
    asl.df['grnd-lx'] = asl.df['left-x'] - asl.df['nose-x']
    asl.df['grnd-ly'] = asl.df['left-y'] - asl.df['nose-y']
    return ['grnd-rx','grnd-ry','grnd-lx','grnd-ly']

def setup_features_norm(asl):
    df_means = asl.df.groupby('speaker').mean()
    df_std = asl.df.groupby('speaker').std()
    asl.df['right-x-mean'] = asl.df['speaker'].map(df_means['right-x'])
    asl.df['right-y-mean'] = asl.df['speaker'].map(df_means['right-y'])
    asl.df['left-x-mean']  = asl.df['speaker'].map(df_means['left-x'])
    asl.df['left-y-mean']  = asl.df['speaker'].map(df_means['left-y'])
    asl.df['norm-rx'] = (asl.df['right-x'] - asl.df['right-x-mean']) / asl.df['speaker'].map(df_std['right-x'])
    asl.df['norm-ry'] = (asl.df['right-y'] - asl.df['right-y-mean']) / asl.df['speaker'].map(df_std['right-y'])
    asl.df['norm-lx'] = (asl.df['left-x']  - asl.df['left-x-mean'])  / asl.df['speaker'].map(df_std['left-x'])
    asl.df['norm-ly'] = (asl.df['left-y']  - asl.df['left-y-mean'])  / asl.df['speaker'].map(df_std['left-y'])
    return ['norm-rx', 'norm-ry', 'norm-lx','norm-ly']

def setup_features_polar(asl):
    asl.df['polar-rr'] = np.sqrt(asl.df['grnd-rx']**2 + asl.df['grnd-ry']**2)
    asl.df['polar-rtheta'] = np.arctan2(asl.df['grnd-rx'], asl.df['grnd-ry'])
    asl.df['polar-lr'] = np.sqrt(asl.df['grnd-lx']**2 + asl.df['grnd-ly']**2)
    asl.df['polar-ltheta'] = np.arctan2(asl.df['grnd-lx'], asl.df['grnd-ly'])
    return ['polar-rr', 'polar-rtheta', 'polar-lr', 'polar-ltheta']

def setup_features_delta(asl):
    asl.df['delta-rx'] = asl.df['right-x'].diff().fillna(0)
    asl.df['delta-ry'] = asl.df['right-y'].diff().fillna(0)
    asl.df['delta-lx'] = asl.df['left-x'].diff().fillna(0)
    asl.df['delta-ly'] = asl.df['left-y'].diff().fillna(0)
    return ['delta-rx', 'delta-ry', 'delta-lx', 'delta-ly']

def train_all_words(features, model_selector):
    training = asl.build_training(features)
    sequences = training.get_all_sequences()
    Xlengths = training.get_all_Xlengths()
    model_dict = {}
    for word in training.words:
        model = model_selector(sequences, Xlengths, word, n_constant=3).select()
        model_dict[word] = model
    return model_dict

def get_models(features, model_selector, file):
    #print("> loading model {}".format(file))
    if Path(file).exists():
        with open(file, 'rb') as f:
            models = pickle.load(f)
            #print(">\tmodels loaded from {}".format(file))
            return models
    else:
        with open(file, 'wb') as f:
            models = train_all_words(features, model_selector)
            pickle.dump(models, f)
            #print(">\tmodels loaded and dumped to {}".format(file))
            return models 

if __name__ == "__main__":
    asl = AslDb()

    selectors = { 
        'constant': SelectorConstant, 
        'bic': SelectorBIC, 
        'dic': SelectorDIC, 
        'cv': SelectorCV 
    }
    
    features = { 
        'ground': setup_features_ground(asl), 
        'norm': setup_features_norm(asl), 
        'polar': setup_features_polar(asl), 
        'delta': setup_features_delta(asl) 
    }

    test_sets = {}
    for feature_k, feature_v in features.items():
        test_sets[feature_k] = asl.build_test(feature_v)
    
    selector_models = {}
    for selector_k,selector_v in selectors.items():
        for feature_k, feature_v in features.items():
            file_name = "model.{}.{}.pickle".format(selector_k, feature_k)
            if not selector_models.get(selector_k): selector_models[selector_k] = {}
            selector_models[selector_k][feature_k] = get_models(feature_v, selector_v, file_name)

    for selector_k, selector_v in selectors.items():
        for feature_k, feature_v in features.items():
            try:
                model = selector_models[selector_k][feature_k]
                print("testing {} model with feature {}".format(selector_k, feature_k))
                probabilities, guesses = recognize(model, test_sets[feature_k])
                show_errors(guesses, test_sets['ground'])
                print("-"*80)
                print("")
            except:
                pass