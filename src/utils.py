#################################################
# Utilities for TrendFinder
#
#################################################

from gensim.models import Word2Vec
import os
import pandas as pd

PARENT = '/Users/claremariemyers/Dropbox/that_fashion_app/'


def load_pickled_years_nobg(begin_yr, end_yr):
    '''Takes in a start year and end year.
        Fetches the pickled dataframes corresponding to those years and
        returns a dictionary of those dataframes'''

    years_dict = {}
    for year in xrange(begin_yr, end_yr + 1):
        print "now loading year {}".format(year)
        years_dict['df_for_{}_nobg'.format(str(year))] = \
            pd.read_pickle(PARENT + 'data/df_for_{}_nobg.pkl'.format(str(year)))

    return pd.concat([df for df in years_dict.values()])

def load_or_make_w2v_model(path, df):
    '''if the Word2Vec model exists at the filepath, open it. Otherwise, make a new one'''
    if os.path.isfile(path):
        print "loading pre-trained Word2Vec model"
        w2v_model = Word2Vec.load(path)
    else:
        print "creating new Word2Vec model"
        w2v_model = Word2Vec(df.tokenized_descs, sg=1)
        print "saving new Word2Vec model at {}".format(path)
        w2v_model.save(path)

    return w2v_model
