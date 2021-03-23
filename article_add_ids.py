# article_add_ids.py
# Reads news articles from scraped JSON file
# Simplifies it by assigning strings to elements instead of lists
# Adds each line an id element to keep them identical for later referrals.
# Adds the article title as the first sentence of the article actual text(body). Useful for future annotations.
# Cleans the article from common repititions and multiple spaces.
# Recategorizes them, English equivalents, also merging some small ones into their bigger ancestor.


import json
from collections import Counter
import re

FOLLOW_REPITITION = Counter()

def clean_article(article):
    global FOLLOW_REPITITION

    #  "Follow on Telegram" repititiion:
    for repetition in re.findall("Yanada ko.proq.*bo.ling", article):
        article = article.replace(repetition,"")
        FOLLOW_REPITITION.update([repetition])
    for repetition in re.findall("Diqqat..diqqat.*Daryo.*Telegram.*lishingiz mumkin.", article):
        article = article.replace(repetition,"")
        FOLLOW_REPITITION.update([repetition])
    for repetition in re.findall("\“Daryo\”ning Telegram’dagi rasmiy kanali — @toshqindaryo’ga a’zo bo‘ling!", article):
        article = article.replace(repetition,"")
        FOLLOW_REPITITION.update([repetition])

    #  "Mavzu" repititiion:
    article = article.replace(" Mavzuga doir:","")
    article = article.replace(" Mavzuga doir :","")

    #  "Reklama" repititiion:
    article = article.replace("Reklama huquqi asosida","")

    #  "Instagram" repititiion:
    article = article.replace(" \n\t\t   \n\t\t\t  \n\t\t\t  \n\t\t\t\t \n\t\t\t\t \n\t\t\t  \n\t\t   \n\t\t   \n\t\t   \n\t\t\t  \n\t\t\t\t \n\t\t\t\t    \n\t\t\t\t\t   \n\t\t\t\t\t\t  \n\t\t\t\t\t   \n\t\t\t\t    \n\t\t\t\t \n\t\t\t  \n\t\t   \n\t\t   \n\t\t\t   View this post on Instagram \n\t\t   \n\t\t   \n\t\t   \n\t\t\t  \n\t\t\t\t \n\t\t\t\t \n\t\t\t\t \n\t\t\t  \n\t\t\t  \n\t\t\t\t \n\t\t\t\t \n\t\t\t  \n\t\t\t  \n\t\t\t\t \n\t\t\t\t \n\t\t\t\t \n\t\t\t  \n\t\t   \n\t\t   \n\t\t\t  \n\t\t\t  \n\t\t   \n\t   ","")

    #  "Foto" repititiion:
    article = article.replace("(foto)","")
    article = article.replace("(Foto)","")

    #  "Video" repititiion:
    article = article.replace("(video)","")
    article = article.replace("(Video)","")

    #  Multiple whitespaces into one:
    article = ' '.join(article.split())
    
    return article

# Count of Categories before recategorization:
# {'Mahalliy': 70312, 'Dunyo': 58469, 'Sport': 27415, 'Texnologiyalar': 6000, 'Avto': 5080, 'Madaniyat': 4359, 'Qo‘ziqorin': 3854, 'Foto': 3167, 'Shou-biznes': 1702, 'Kino': 1607, 'Ilm-fan': 1092, 'Gadjetlar': 1071, 'Maslahatlar': 1035, 'Salomatlik': 857, 'Koinot': 766, 'Retseptlar': 545, 'Musiqa': 346, 'Moda': 320, 'Go‘zallik': 278, 'Kitob': 248, 'Media': 186, 'San’at': 161, 'Osiyo kubogi-2015': 140, 'Lifestyle': 124, 'Farzand': 107, 'Reklama': 105, 'Ingliz tilini o‘rganamiz!': 58, 'Karyera': 57, 'Teatr': 57, 'Mehridaryo': 48, 'Kolumnistlar': 44, 'Arxitektura': 44, 'Startaplar': 42, 'Retseptlar Yangi Yil': 22, 'Abituriyent': 20, 'None': 18, 'Sog‘lom turmush': 12, 'Intervyu': 11, 'Yangi yil': 7, 'Futzal JCh—2016': 7, 'Dasturxon': 7, 'Prezident saylovi—2016': 6, 'Дунё': 2, 'Yevro—2016': 2, 'U-23 Qatar—2016': 2, 'Sayohat': 1, 'Абитуриент': 1}
# Count of Categories after recategorization:
# {'Local': 70312, 'World': 62326, 'Sport': 27566, 'Tech': 12151, 'Misc': 4743, 'Media': 4379, 'Culture': 4359, 'Science': 2150, 'Health': 1254, 'Food': 574}
def recategorize(category):
    category_dict = {
        'Mahalliy': 'Local', 
        'Dunyo': 'World', 
        'Sport': 'Sport', 
        'Texnologiyalar': 'Tech', 
        'Avto': 'Tech', 
        'Madaniyat': 'Culture', 
        'Qo‘ziqorin': 'World', 
        'Foto': 'Misc', 
        'Shou-biznes': 'Media', 
        'Kino': 'Media', 
        'Ilm-fan': 'Science', 
        'Gadjetlar': 'Tech', 
        'Maslahatlar': 'Misc', 
        'Salomatlik': 'Health', 
        'Koinot': 'Science', 
        'Retseptlar': 'Food', 
        'Musiqa': 'Media', 
        'Moda': 'Media', 
        'Go‘zallik': 'Health', 
        'Kitob': 'Science', 
        'Media': 'Media', 
        'San’at': 'Media', 
        'Osiyo kubogi-2015': 'Sport', 
        'Lifestyle': 'Misc', 
        'Farzand': 'Health', 
        'Reklama': 'Misc', 
        'Ingliz tilini o‘rganamiz!': 'Misc', 
        'Karyera': 'Misc', 
        'Teatr': 'Media', 
        'Mehridaryo': 'Misc', 
        'Kolumnistlar': 'Misc', 
        'Arxitektura': 'Science', 
        'Startaplar': 'Misc', 
        'Retseptlar Yangi Yil': 'Food', 
        'Abituriyent': 'Misc', 
        'None': 'Misc', 
        'Sog‘lom turmush': 'Health', 
        'Intervyu': 'Misc', 
        'Yangi yil': 'Misc', 
        'Futzal JCh—2016': 'Sport', 
        'Dasturxon': 'Food', 
        'Prezident saylovi—2016': 'Misc', 
        'Дунё': 'World', 
        'Yevro—2016': 'Sport', 
        'U-23 Qatar—2016': 'Sport', 
        'Sayohat': 'World', 
        'Абитуриент': 'Misc'
    }
    if category in category_dict.keys():
        return category_dict[category]
    else:
        return 'None'


def simplify(list_element):
    if(len(list_element)>0):
        return list_element[0]
    else:
        return "None"

# Loading the JSON file:
with open('data/article_body.json') as json_file:
    print("Loading JSON file")
    data = json.load(json_file)
    article_id = 0 # this is the id element we are adding to each article.
    text_corpus = open("data/corpus_daryo_uz.txt", "w") # All articles are collected in this file as a text.
    category_counter = Counter()
    count_sentences = 0 
    # Running through each article in the JSON file:
    for p in data:
        # Assignng an ID to each article:
        article_id += 1
        p['article_id'] = article_id

        # Simplifying json format:
        p['article_title'] = simplify(p['article_title'])
        # p['article_body'] = simplify(p['article_body']) 
        p['article_category'] = simplify(p['article_category'])
        p['article_metadata'] = simplify(p['article_metadata'])

        # Loading elements:
        article_title = p['article_title']
        article_body = p['article_body']
        article_category = recategorize(p['article_category']) 
        # Recategorizing:
        p['article_category'] = article_category
        print("Article #", article_id, ": ", article_title)

        # Title as a part of the body
        article_body = article_title + ". " + article_body
        
        # Cleaning the article:
        article_body = clean_article(article_body)
        
        #Category Count
        category_counter.update([article_category])
        
        # Put it back:
        p['article_body'] = article_body

        #Sentence Count
        count_sentences += len(article_body.split("."))

        text_corpus.write("###" + str(article_id) + "\n")
        text_corpus.write(article_body + "\n")
    text_corpus.close()
    # Writing the resulting JSON data to a new file:
    print("Saving the new JSON file.")
    with open('data/article_body_new.json', 'w') as outfile:
        json.dump(data, outfile, indent=0)
    print("New JSON file saved.")
    print("Categories count:")
    print(category_counter)
    print("Total number of (possible) sentences: ", count_sentences)

    # Follow repetition
    # print(FOLLOW_REPITITION)
    with open('data/follow_repetition.txt', 'w') as repfile:
        repfile.write(json.dumps(FOLLOW_REPITITION, indent=0))
    repfile.close()
    print("Follow repetition has been saved as data/follow_repetition.txt")
