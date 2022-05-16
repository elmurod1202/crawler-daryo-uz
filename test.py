import json
from collections import Counter
import re

# Loading article sentences in JSONL file into a list:
sentences = list()
with open('data/daryo_sentences.jsonl','r') as jsonl_file:
# with open('data/test.jsonl','r') as jsonl_file:
    # Loading lines into a list:
    for line in jsonl_file:
        sentences.append(json.loads(line.strip()))


#Loading uzwiki corpus:
# file = open("data/corpus/test.txt")
print("Loading corpus:")
# file = open("data/corpus/uzwiki-single-text.txt")
file = open("data/corpus/corpus_daryo_reduced.txt")
corpus = file.read()
file.close()

 
# Go through each article sentence if the line contains any:
count_sent = 0
count_found = 0
for sentence in sentences:
    count_sent += 1
    if(sentence['text'] in corpus):
        print(count_sent, ": Found: ", sentence)
        count_found += 1
    else:
        print(count_sent, ": ", count_found)
print("Done!")



# with open('data/article_body_new.json') as json_file:
#     print("Loading JSON file")
#     data = json.load(json_file)
#     for p in data:
#         # Loading elements:
#         article_id = p['article_id']
#         article_body = p['article_body']
#         article_category = p['article_category']
#         for finding in re.findall("Yanada ko.proq.*bo.ling",article_body):
#             print(finding)
#     print("Done!")
