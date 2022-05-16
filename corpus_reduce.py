# corpus_reduce.py
# Reads Daryo news corpus from JSON file.
# Randomly selects articles until it has the same number of tokens the Uzbek Wiki corpus has.


import json
# from collections import Counter
import re
import random

def count_words(line):
    return len(line.split())

# Count tokents in corpus:
# Uzwiki file name: uzwiki-single-text.txt
# Daryo big file name: corpus_daryo_reduced.txt
# Daryo small file name: corpus_daryo_small.txt
# count_tokens = 0
# with open('data/corpus_daryo_small.txt', 'r') as corpus_file:
#     count_line = 0
#     for line in corpus_file:
#         count_tokens += count_words(line.strip())
#         count_line += 1
#         if(count_line % 1000 == 0):
#             print("Line: ", count_line)
#     print("Total lines: ", count_line)
# print("Total tokens: ", count_tokens)

# exit(1)

# Loading the JSON file:
# with open('data/article_body_new.json') as json_file:  # Use this one if you want to include also articles chosen for annotation.
with open('data/article_body_new_rest.json') as json_file:
    # Loading Json file:
    print("Loading JSON file")
    data = json.load(json_file)
    
    # Making a dictionary out of articles (id, text):
    print("Making a dictionary out of articles (id, text)")
    articles = dict()
    for p in data:
        # Loading elements:
        article_id = p['article_id']
        article_body = p['article_body']
        # article_category = p['article_category']
        articles[article_id] = p
    
    #Obtaining article ids in a different set:
    print("Obtaining article ids in a different set")
    article_ids = list(articles.keys())
    
    # Shuffling ids:
    random.seed(2021) # Does this make sense?, Apparently, it DOES.
    random.shuffle(article_ids)

    #Reading articles in a shuffled order until needed tokens reached:
    print("Reading articles in a shuffled order until needed tokens reached")
    count_tokens = 0
    article_small = []
    token_count_uzwiki = 9714000
    corpus_text = open('data/corpus_daryo_small.txt', 'w')
    for article_id in article_ids:
        article = articles[article_id]
        article_body = article['article_body']
        count_tokens += count_words(article_body)
        article_small.append(article)
        corpus_text.write(article_body)
        corpus_text.write("\n")
        # check the token count:
        if(count_tokens >= token_count_uzwiki):
            print("Token count reached. Stopping here.")
            break
    corpus_text.close()
    
    # Saving small article corpus into new json file:
    print ("Saving new corpus:")
    with open('data/article_body_small.json',"w") as dst_file:
        json.dump(article_small,dst_file, indent=0)
    dst_file.close()


    # Things TODO:
    # run json2multiple_texts for the resulted json
    # copy resulting multiple files to mafalda
    # run build_dataset
    # tokenization?, ask David.
    # start training

        
print("Done!")
