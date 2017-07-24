##########################################################
# Generic web scraper to collect sequentially numbered
# user posts
# ########################################################

from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
from requests.exceptions import ConnectionError
import time


URL_ROOT = 'blank'
DB_PATH = 'mongodb://localhost:27017/'


def open_db(db_path):

    client = MongoClient(db_path)
    db_name = raw_input("Database name: ")
    collection = raw_input("Collection name: ")

    db = client[db_name]
    posts = db[collection]

    return posts

def get_posts(target_collection):

    '''
    this assumes that queries will be sequential numerical ids such that
    if URL_ROOT = www.mysite.com/posts/,
    individual pages are accessed as eg www.mysite.com/posts/103
    '''

    start = raw_input("Begin with id: ")
    end = raw_input("End with id: ")
    nums_list = xrange(int(start), int(end))

    ct = 0
    start_t = time.time()
    for i in nums_list:

        try:
            response = get_post(i)
            entry = clean_entry(response)
            target_collection.insert_one(entry)
        except ConnectionError:
            print "{} failed to respond".format(i)

        ct += 1

        if ct == 1:
            print "First page scraped!"
        if ct%100 == 0:
            end_t = time.time()
            print "Scraped {} pages".format(ct)
            print "Elapsed time {} seconds".format(end_t-start_t)

    print "Done!"

def get_post(query):
    url = URL_ROOT + query
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def clean_entry(soup):
    '''
    Search HTML tags for desired content and enter into a features dictionary.
    This will be specific to the site the information comes from so must be filled in by the user.
    '''

    fd = {}

    # #example:
    # desc = soup.find("div", {"id": "photo_description"})
    # if desc is not None:
    #     desc = desc.text
    #     fd['photo_desc'] = desc.encode('ascii', 'ignore')
    # else:
    #     fd['photo_desc'] = "No Description"

    return fd

if __name__ == '__main__':
    posts = open_db(DB_PATH)
    get_posts(posts)
