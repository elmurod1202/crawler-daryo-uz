# split_sentences.py
# Reads news articles from chosen articles (jsonl file).
# Splits each article into sentences and saves in a new JSONL file with each sentence per line.

import json
# import jsonlines
from collections import Counter
import re
import nltk

# Some articles contain repetetive unwanted text, this method removes them.
# Example article: Foto: "Daryo" blah blah blah...
# Also these lines were removed afterwards:
        # Foto: Hyundai Ioniq 5 
        # Foto: \u201cDaryo\u201d 
        # Foto: \u201cDomashniy ochag\u201d 
        # Foto: \u201cKanvon\u201d FK 
        # Foto: unicef.org 
        # Foto: Hi-Tech.Mail.ru 
        # Foto: Global Look Press 
        # Foto: Getty Images 
        # Foto: Cosmopolitan 
        # Foto: \u201cXalq so\u2018zi online\u201d 
        # Foto: \u201cYandeks Dzen\u201d 
        # Foto: OKMK FK 
        # Foto: Oliy Majlis Senati axborot xizmati 
        # Foto: Freepik 
        # Foto: Reuters 
        # Foto: Twitter 
        # Foto: AdMe \u201c
        # Foto: AdMe 
        # Foto: Google Photos 
        # Foto: Instagram 
        # Foto: \u201cO\u2018zbekkino\u201d 
def clean_article(article_text):
    article_sentences = tokenizer.tokenize(article_text)
    foto_sentences = []
    min_len_sen = 100
    for sentence in article_sentences:
        if (sentence.startswith("Foto: ")):
            foto_sentences.append(sentence)
            if(len(sentence)< min_len_sen):
                min_len_sen = len(sentence)
    if(len(foto_sentences)>1):
        max_match = ""
        for i in range(7,min_len_sen):
            match = foto_sentences[1][:i]
            # print(match)
            max_count=len(foto_sentences)
            max=0
            for foto_sent in foto_sentences:
                if(foto_sent.startswith(match)):
                    max +=1
            if(max < max_count -1):
                print("Repeating rubbish found: ", max_match)
                return article_text.replace(max_match,"")
            else:
                max_match = match
        if(len(max_match)>0):
            return article_text
    else:
        return article_text


# Loading tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
outfile = open('data/daryo_sentences.jsonl', 'w')
# Loading the JSONL file:
count_count_sentences = 0
with open('data/chosen_articles.jsonl','r') as jsonl_file:
# with open('data/test.jsonl','r') as jsonl_file:
    # RUnning through each line:
    for line in jsonl_file:
        article = json.loads(line.strip())
        # Loading elements:
        article_text = article['text']
        article_meta = article['meta']

        # print("#############")
        article_text = clean_article(article_text)
        # print(article_text)
        #Tokenizing into sentences:
        article_sentences = tokenizer.tokenizer(sentence, truncation=True, padding=True)
        # article_sentences = nltk.tokenize.sent_tokenize(article_text)
        # Running through each sentence:
        count_sentence = 0
        for sentence in article_sentences:
            count_sentence += 1
            #Saving josnl file:
            article_meta["sentence"] = count_sentence
            entry = {"text":sentence,"meta":article_meta}
            json.dump(entry, outfile)
            outfile.write('\n')
            # print(count_sentence, ": ", sentence)
        print("############ Article:", article_meta)
        count_count_sentences += count_sentence
print("Total # of sentences in entire file: ", count_count_sentences)
jsonl_file.close()
outfile.close()