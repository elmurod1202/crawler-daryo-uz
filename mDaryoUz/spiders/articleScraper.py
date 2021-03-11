# -*- coding: utf-8 -*-

# Spider 2
# ArticleScraper.py which scrape article headlies and bodies

# imports
import scrapy
from scrapy.http import Request
from mDaryoUz.items import MdaryouzItem
import json

class ArticlescraperSpider(scrapy.Spider):
    name = 'articleScraper'
    allowed_domains = ['m.daryo.uz']
    start_urls = ['http://m.daryo.uz/']

    def start_requests(self):
        # Open the JSON file which contains article links
        with open('/home/elmurod/env-workspace/scrapy/mDaryoUz/article_links.json') as json_file:
            data = json.load(json_file)
            for p in data:
                print('URL: ' + p['article_url'])
                # Request to get the HTML content
                request=Request(p['article_url'], cookies={'store_language':'uz'}, callback=self.parse_article_page)
                yield request

    def parse_article_page(self,response):
        item=MdaryouzItem()
        a_body=""
        
        # Extracts the article_title and stores in scrapy item
        item['article_title']=response.xpath('//*[@id="content"]/div[1]/h1/text()').extract();
        
        # Extracts the article_category and stores in scrapy item
        item['article_category']=response.xpath('//*[@id="content"]/div[1]/div[1]/a/text()').extract();
        
        # Extracts the article_metadata (Published date, time, number of views) and stores in scrapy item
        item['article_metadata']=response.xpath('//*[@id="content"]/div[1]/div[2]/text()').extract();

        # Extracts the article_body in <p> elements
        for p in response.xpath('//*[@id="content"]/div[1]/div[3]//p//text()').extract():
            a_body=a_body + " " + p
        item['article_body']= a_body
        yield(item)

    def parse(self, response):
        pass
