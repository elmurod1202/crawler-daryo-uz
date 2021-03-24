# json2multiple_texts.py
# Reads news articles from reorganized(and cleaned) JSON file
# Saves each 500 article in a separate text file.
# I could've saved each articlea as a separate text file, 
# but they are too small and one folder qould have hundreds of thousands of files, making it hard to work with them.


import json
# from collections import Counter
import re

# Loading the JSON file:
with open('data/article_body_new.json') as json_file:
    print("Loading JSON file")
    data = json.load(json_file)
    # Running through every 500 article in the JSON file:
    chunks = [data[x:x+500] for x in range(0, len(data), 500)]
    count_chunk = 0
    for chunk in chunks:
        article_file_name = "Article_"+str(count_chunk).zfill(6)+".txt"
        article_file = open('data/daryo_multiple_files/'+article_file_name,"w")
        for p in chunk:
            # Loading elements:
            # article_id = p['article_id']
            article_body = p['article_body']
            # article_category = p['article_category']
            article_file.write(article_body)
            article_file.write("\n")
        print("Saved: ", article_file_name)
        article_file.close()
        count_chunk+=500
        
print("Files saved.")
