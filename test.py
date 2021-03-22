import json
from collections import Counter
import re

with open('data/article_body_new.json') as json_file:
    print("Loading JSON file")
    data = json.load(json_file)
    for p in data:
        # Loading elements:
        article_id = p['article_id']
        article_body = p['article_body']
        article_category = p['article_category']
        for finding in re.findall("Yanada ko.proq.*bo.ling",article_body):
            print(finding)
    print("Done!")
