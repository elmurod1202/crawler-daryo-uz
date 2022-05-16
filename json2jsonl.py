# json2jsonl.py
# Reads news articles from reorganized JSON file
# Cuts $NUM_ARTICLES_PER_CATEGORY number of articles from top of each category.
# Separates those chosen articles from the corpus, saving them in different files.


# Splits and saves chosen articles into sentences.
# import nltk.data

# tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
# fp = open("test.txt")
# data = fp.read()
# print '\n-----\n'.join(tokenizer.tokenize(data))

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
    corpus_text = open('data/corpus_daryo_reduced.txt', 'w')
    # Running through each article in the JSON file:
    categories = {'Local': 0, 'World': 0, 'Sport': 0, 'Tech': 0, 'Misc': 0, 'Media': 0, 'Culture': 0, 'Science': 0, 'Health': 0, 'Food': 0}
    chosen_article_ids = []
    article_body_new_rest = []
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
            chosen_article_ids.append(article_id)
        else:
            article_body_new_rest.append(p)
            corpus_text.write(article_body)
            corpus_text.write("\n")
            print("Skipping...")

    outfile.close()
    corpus_text.close()
    print("Total articles processed: ", len(data))

# Saving ID of chosen articles to a json file: 
with open('data/chosen_articles_ids.json',"w") as dst_file:
    #json.dump(chosen_article_ids,dst_file) # BTW, this does the same as belov line, just trying both.
    dst_file.write(json.dumps(chosen_article_ids))
dst_file.close()

# Saving rest of articles without chosen articles to a new json file: 
print ("Saving new corpus:")
with open('data/article_body_new_rest.json',"w") as dst_file:
    json.dump(article_body_new_rest,dst_file, indent=0)
dst_file.close()

print("Total articles saved to new json corpus: ", len(article_body_new_rest))
print("New JSONL file saved.")
