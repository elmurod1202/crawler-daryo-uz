import json
# from collections import Counter
import re
from string import punctuation

# Loading article sentences in JSONL file into a list:
sentences = list()
with open('data/daryo_sentences.jsonl','r') as jsonl_file:
# with open('data/test.jsonl','r') as jsonl_file:
    # Loading lines into a list:
    for line in jsonl_file:
        sentences.append(json.loads(line.strip()))

# Loading corpora in the laziest way that works:
#Loading uzwiki corpus:
# file = open("data/corpus/test.txt")
print("Loading Wiki corpus:")
file = open("data/corpus/uzwiki-single-text.txt")
corpus_wiki = file.read()
file.close()

#Loading daryo corpus:
# file = open("data/corpus/test.txt")
print("Loading Daryo corpus:")
file = open("data/corpus/corpus_daryo_reduced.txt")
corpus_daryo = file.read()
file.close()


sentences_clean = open('data/daryo_sentences_clean.jsonl', 'w')
sentences_unwanted = open('data/daryo_sentences_unwanted.jsonl', 'w')
# Go through each article sentence if the line contains any:
count_sent = 0
count_found = 0
for sentence_json in sentences:
    count_sent += 1
    sentence = sentence_json['text'].strip().strip(punctuation).strip()
    if((sentence in corpus_wiki) or (sentence in corpus_daryo)):
        print(count_sent, ": Found: ", sentence)
        count_found += 1
        json.dump(sentence_json, sentences_unwanted)
        sentences_unwanted.write('\n')
    else:
        print(count_sent, ": ", count_found)
        json.dump(sentence_json, sentences_clean)
        sentences_clean.write('\n')
sentences_clean.close()
sentences_unwanted.close()
print("Done!")


# Here is an old version that handles large corpus text files in a better way:
# But in my case such a big hassle was not necessary, apparently.
"""
import json
from collections import Counter
import re

def contains(sentence, line):
    if sentence in line:
        print("Found: ", sentence)
        return True
    else:
        return False

# Loading article sentences in JSONL file into a list:
sentences = list()
# with open('data/daryo_sentences.jsonl','r') as jsonl_file:
with open('data/test.jsonl','r') as jsonl_file:
    # Loading lines into a list:
    for line in jsonl_file:
        sentences.append(json.loads(line.strip()))
        print(json.loads(line.strip())['text'])

#Loading uzwiki corpus and going through each line:
count_line = 0
print("Going in with {} sentences.".format(len(sentences)))
# with open("data/corpus/uzwiki-single-text.txt","r") as corpus:
with open("data/corpus/test.txt","r") as corpus:
    for line in corpus:
        count_line += 1
        # Go through each article sentence if the line contains any:
        sentences = [sentence for sentence in sentences if not contains(sentence['text'], line)]
        print("Line: {}, Sentences left: {}".format(count_line, len(sentences)))

print("Came out with {} sentences.".format(len(sentences)))
# Initializing output list:
clean_sentences = sentences
# Saving it:
#....unfinished.

print("Done, lines in corpus: ",count_line)
"""