# json2jsonl.py
# Reads news articles from reorganized JSON file
# Creates new JSONL file out of that JSON data
# Cuts NUM_ARTICLES_PER_CATEGORY number of articles from top of each category.

import json
# import jsonlines
from collections import Counter
import re

# Count of Articles in Categories:
# {'Local': 70312, 'World': 62326, 'Sport': 27566, 'Tech': 12151, 'Misc': 4743, 'Media': 4379, 'Culture': 4359, 'Science': 2150, 'Health': 1254, 'Food': 574}

NUM_ARTICLES_PER_CATEGORY = 30 # 30 * 10(categories) = 300 articles
# Loading the JSON file:
with open('data/article_body_new.json') as json_file:
    print("Loading JSON file")
    data = json.load(json_file)
    outfile = open('data/output.jsonl', 'w')
    # Running through each article in the JSON file:
    categories = {'Local': 0, 'World': 0, 'Sport': 0, 'Tech': 0, 'Misc': 0, 'Media': 0, 'Culture': 0, 'Science': 0, 'Health': 0, 'Food': 0}
    for p in data:
        # Loading elements:
        article_id = p['article_id']
        article_body = p['article_body']
        article_category = p['article_category']
        if(categories[article_category] < NUM_ARTICLES_PER_CATEGORY):
            categories[article_category]+=1
            print("Article #", article_id, "Category: ", article_category)
            entry = {"text":article_body,"meta":{"source":"Daryo.uz","category":article_category,"article_id":article_id}}
            json.dump(entry, outfile)
            outfile.write('\n')
        else:
            print("Skipping...")

    outfile.close()
    print("New JSONL file saved.")
