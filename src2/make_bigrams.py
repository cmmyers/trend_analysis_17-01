


#this contains the bulk of the language work
#assumes we are starting with a dataframe which we can then
#bigramify with a W2V4Trends object
from W2V4Trends import W2V4Trends
from gensim.models import Word2Vec
import pandas as pd
import string
from itertools import combinations


nltk_stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

basic_garments = ["dress", "pants", "shirt", "shoes", "bag"]

def coerce_to_datetime(series):
    series_2 = []
    for item in series:
        try:
            s = "{}, {}, {}".format(item[0], item[1], item[2])
            series_2.append(s)
        except TypeError:
            series_2.append('2008, 03, 01')
    series_2 = pd.Series(series_2)
    series_3 = pd.to_datetime(series_2)
    return series_3

def get_columns_for_nlp(df):
    '''
    reduce dataframe to the columns being used for this project'''

    columns = ['post_id', 'photo_desc', 'username', 'location', 'datetime']

    new_df = pd.DataFrame()
    for c in columns:
        new_df[c] = df[c]

    new_df['month'] = df['datetime'].dt.month
    new_df['quarter'] = df['datetime'].dt.quarter
    new_df['year'] = df['datetime'].dt.year
    make_tokens(new_df)

    return new_df

def make_tokens(df):
    '''remove punct, lowercase all, remove newline chars and then
    make a list (tokenization) of all terms in description field
    and place in a new column'''

    srs = df.photo_desc
    list_o_strings = []
    for item in df.photo_desc:
        item = str(item)
        item = item.translate(None, string.punctuation).lower().replace('\n', ' ').split()
        list_o_strings.append(item)
    df['tokenized_descs'] = list_o_strings

def ask_for_manual_stopwords():
    '''to remove descriptors such as 'cool' or 'new', which are not significant
    for finding trends'''
    cont = True
    boring_words = []
    while cont:
        new_word = raw_input("Please enter a base word or type DONE when done: ")
        if new_word.upper() == "DONE":
            cont == False
        else:
            boring_words.append(new_word)

    man_sw = manual_stopwords(boring_words)
    return man_sw

def manual_stopwords(boring_words, model):
    '''finds the 10 most similar 'boring' words for each word given, eg 'cool'
    would likely find 'neat', 'awesome', etc'''
    sw = []
    for word in boring_words:
        sw.append(collect_similar(word, model, 10))
    return set([item for l in man_sw for item in l])

def collect_similar(word, model, n_output):
    '''
    INPUT: word = a base vocabulary word
        model = a trained word2vec model (or path in the form Word2Vec.open('model_path'))
        n_output = the number of similar words to collect
                    the root word will also be included in this list

    RETURNS: a list of words
    '''

    most_sim = model.most_similar(word, topn=n_output)
    most_sim_list = [item[0] for item in most_sim]
    most_sim_list.append(word)

    return most_sim_list


def make_bigrams(text, root_word, stopwords=nltk_stopwords, root_word_first = False):
    '''
    INPUT: text = a list of word tokens
        root_word = the word to be bigramified

        root_word_first --> currently this function assumes the root word
        should be the second word in the phrase, eg 'dress' in 'sack dress'.
        I would like to add functionality for the root to be the first word
        so that we can search the nouns that go with a given adjective,
        eg 'wedge' in 'wedge sneakers'

    RETURNS: a modified list of word tokens
    '''

    new_text = []
    try:
        i=0
        while i < (len(text)-1):

            if text[i+1] != root_word:
                new_text.append(text[i])
                i+=1
            elif text[i] in stopwords:
                new_text.append(text[i])
                i+=1
            else:
                new_text.append('{}_{}'.format(text[i], text[i+1]))
                i+=2

        if text[-1] != root_word:
            new_text.append(text[-1])

    except IndexError:
        new_text.append('')

    return new_text


def bigrams_for_similar_garments(text_series, word, model, stopwords= nltk_stopwords, num_sim=10):
    '''
    INPUT: text_series => pandas series or list of [lists of word tokens]
        word = a root word
        model = a trained word2vec model or Word2Vec.open('model_path')

    RETURNS: a list of [lists of modified word tokens]
    '''

    root_words = collect_similar(word, model, num_sim)
    new_texts = []
    for text in text_series:
        for word in root_words:
            text = make_bigrams(text, word, stopwords)
        new_texts.append(text)
    return new_texts


def bigrams_for_all_garments(text_series, model, stopwords=nltk_stopwords, num_sim=10):
    '''
    INPUT: text_series => pandas series or list of [lists of word tokens]
        model = a trained word2vec model or Word2Vec.open('model_path')

    RETURNS: a list of [lists of modified word tokens]
    '''

    basic_garments = ["dress", "pants", "shirt", "shoes", "bag"]
    for garment in basic_garments:
        text_series = bigrams_for_similar_garments(text_series, garment, model, stopwords, num_sim)
    return text_series

def get_bigrams(term, model):

    bigrams = []

    for item in model.most_similar(term, topn=10000):
        if '_' in item[0]:
            item = item[0].split('_')
            bigrams.append('{} {}'.format(item[0], item[1]))

    return bigrams

def make_yearly_dfs(dfs, start_yr, end_yr):
    yearly_dfs = {}
    for year in xrange(start_yr, end_yr):
        print 'Creating df for {}'.format(year)
        all_entries_this_year = []

        for df in dfs:
            year_mask = df['year'] == int(year)
            df_year = df.loc[year_mask]
            all_entries_this_year.append(df_year)


        yearly_dfs['df_for_{}'.format(str(year))] =  pd.concat(all_entries_this_year)

    return yearly_dfs

def pickle_years(dict):
    for k, v in dict.iteritems():
        v.to_pickle('data/{}.pkl'.format(str(k)))

def save_yearly_models(dict):
    for k, v in dict.iteritems():
        v.save('models/{}.txt'.format(k))

def load_pickled_years(begin_yr, end_yr):
    years_dict = {}
    for year in xrange(begin_yr, end_yr + 1):
        years_dict['df_for_{}'.format(str(year))] = \
            pd.read_pickle('../data/df_for_{}.pkl'.format(str(year)))

    return years_dict

def return_best_bigrams(dict):
    top_sim_bigrams_dict = {}
    for name, model in dict.iteritems():
        top_sim_bigrams = []
        year = name.split('_')[-1]
        for garment in basic_garments:
            top_sim_bigrams += get_bigrams(garment, model)[:50]
        top_sim_bigrams_dict['sim_bigrams_{}'.format(year)] = top_sim_bigrams
    return top_sim_bigrams_dict




if __name__ == '__main__':
    #run from parent folder
    paths = ['data/masterA-1128.pkl', 'data/masterB-1128.pkl', 'data/masterC-1128.pkl']
    dfs = []
    for path in paths:
        print 'Reading in {}'.format(path)
        df = pd.read_pickle(path)
        df = get_columns_for_nlp(df)
        dfs.append(df)

    #master_df = pd.concat(dfs)
    #print 'Concantenation complete. Pickling master df'
    #master_df.to_pickle('master_df_all_yrs.pkl')

    #print 'loading master df'
    #master_df = pd.read_pickle('master_df_all_yrs.pkl')

    yearly_dfs_x = make_yearly_dfs(dfs, 2009, 2013)
    yearly_df_y = make_yearly_dfs(dfs, 2013, 2014)
    #for future use
    print 'Pickling yearly dfs'
    pickle_years(yearly_dfs_x)
    pickle_years(yearly_df_y)

    yearly_dfs_x = load_pickled_years()


    x_slices_to_combine = [v for k, v in yearly_dfs_x.iteritems()]
    X_slice_df = pd.concat(x_slices_to_combine)
    y_df = yearly_df_y['df_for_2013']

    # print 'Creating W2V model for yrs 2009-2012'
    # model_2009_2012 = Word2Vec(X_slice_df.tokenized_descs)
    # model_2009_2012.save('models/model_2009_2012.txt')

    print 'Loading W2V model for yrs 2009-2012'
    model_2009_2012 = Word2Vec.load('models/model_2009_2012.txt')

    model_2009_2012 = W2V4Trends(model_2009_2012)
    model_2009_2012.update_stopwords()

    bg_models = {}
    for name, yr_df in yearly_dfs_x.iteritems():
        year = name.split('_')[-1]
        print 'Bigramifying text for {}'.format(year)
        yr_df['bigramified_text'] = model_2009_2012.bigrams_for_all_garments(yr_df.tokenized_descs)
        print 'Making model for {}'.format(year)
        bg_models['bg_model_for_{}'.format(year)] = Word2Vec(yr_df.bigramified_text)

    print 'Pickling yearly bigram models for yrs 2009-2012'
    save_yearly_models(bg_models)

    best_bigrams = return_best_bigrams(bg_models)

    union_2009_2011 = set(best_bigrams['sim_bigrams_2009'] + \
        best_bigrams['sim_bigrams_2010'] + best_bigrams['sim_bigrams_2011'])
    only_2012 = set(best_bigrams['sim_bigrams_2012']) - union_2009_2011
    print only_2012

    trend_dict_2012 = {}
    for trend in only_2012:
        trend_dict_2012[trend] = Trend(trend)
        print trend
        print trend_dict_2012[trend].get_tfm_tpm(X_slice_df, 'photo_desc', 1, 2009, 48)[1]
        print '\n'
