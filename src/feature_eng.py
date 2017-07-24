from gensim.models import Word2Vec
from nltk.corpus import stopwords
import pandas as pd
import string


def get_all_features(df, model):
    get_columns(df)
    make_bigrams(model, df)

def get_columns(df):
    '''
    Take in a dataframe (converted eg from Mongo or json) and prepare it for analysis
    '''
    columns = ['post_id', 'photo_desc', 'username', 'location', 'datetime']
    df = df[columns]

    df['month'] = df['datetime'].dt.month
    df['quarter'] = df['datetime'].dt.quarter
    df['year'] = df['datetime'].dt.year
    make_tokens(df)

def make_tokens(df):
    '''
    Remove punct, lowercase all words, remove newline chars.
    Then tokenize each description field.
    '''
    tokenized_descriptions = []

    for item in df.photo_desc:
        item = str(item)
        item = item.translate(None, string.punctuation)
        item = item.lower().replace('\n', ' ').split()
        tokenized_descriptions.append(item)

    df['tokenized_descs'] = tokenized_descs

def make_bigrams(model, df):
    print "Now creating bigrams"
    bg_maker = BigramMaker(model)
    bg_maker.bigrams_for_all_garments(df)
    return df

class BigramMaker():
    def __init__(self, model):
        self.model = model
        self.basic_garments = ["dress", "pants", "shirt", "shoes", "bag"]
        self.boring_words = ['cool', 'favorite', 'new', 'red', 'black', 'wearing', 'gorgeous']
        self.sws = set(stopwords.words('english') + self.addl_stopwords())

    def addl_stopwords(self):
        sw = []
        for word in self.boring_words:
            sw += self.collect_similar(word, 10)
        return sw

    def bigrams_for_all_garments(self, df):
        root_words = []
        for garment in self.basic_garments:
            root_words += self.collect_similar(garment)

        df['bigrammified_descs'] = \
            self.bigrams_for_list_of_words(df.tokenized_descs, set(root_words))

    def collect_similar(self, word, n_output=15):
        most_sim = self.model.most_similar(word, topn=n_output)
        most_sim_list = [item[0] for item in most_sim]
        most_sim_list.append(word)
        return most_sim_list

    def bigrams_for_list_of_words(self, text_series, root_words):

        new_text_series = []
        for text in text_series:
            new_text = []
            if len(text)>1:

                i=0
                while i < (len(text)-1):

                    if text[i+1] not in root_words:
                        new_text.append(text[i])
                        i+=1
                    elif text[i] in self.sws:
                        new_text.append(text[i])
                        i+=1
                    elif '_' in text[i]:
                        new_text.append(text[i])
                        i+=1
                    else:
                        new_text.append('{}_{}'.format(text[i], text[i+1]))
                        i+=2

                if text[-1] not in root_words:
                    new_text.append(text[-1])


            elif len(text) == 1:
                new_text = text
            else:
                new_text = ['no', 'description']

            new_text_series.append(new_text)

        return new_text_series

if __name__ == '__main__':
    pass
