##################################################
# Loads and bigrammifies data for range of years.
# Loads or creates W2V model.
##################################################

import pandas as pd
from TrendDF import TrendDF
from utils import load_pickled_years_nobg, load_or_make_w2v_model
from feature_eng import make_bigrams


MODEL_PATH = '../models/model_2009_2012_2.pkl'

def create_TrendDF(begin_yr, end_yr):
    '''
        INPUT: begin_yr => min year to explore
               end_yr => max year to explore
    '''
    cont = 'Y'

    if begin_yr < 2009:
        print "starting year must be 2009 or later"
        return
    if begin_yr == 2013 or end_yr == 2013:
        print '''
                are you sure you want to continue?
                2013 is current validation yr '''
        cont = raw_input("Enter Y to continue. Press any other key to quit")
    if begin_yr == 2014 or end_yr == 2014:
        print '''
                are you sure you want to continue?
                2014 is current test yr '''
        cont = raw_input("Enter Y to continue. Press any other key to quit")
    if end_yr > 2014:
        print "You're not allowed to look at 2015 or later yet, sorry."
        return

    if cont.upper() == 'Y':
        df = load_pickled_years_nobg(begin_yr, end_yr)
        model = load_or_make_w2v_model(MODEL_PATH, df)
        df = make_bigrams(model, df)
        return TrendDF(df), model




if __name__ == '__main__':
    #dfX_train, model = create_TrendDF(2009,2012)
    print '''
    create or load W2V model and build fashion vocabulary:
    `df, model = create_TrendDF(start_year, end_year)`
    '''
