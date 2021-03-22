# json2multiple_texts.py
# Reads news articles from reorganized(and cleaned) JSON file
# Saves each article in a separate text file.


import json
# from collections import Counter
import re

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
