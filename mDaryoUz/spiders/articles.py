# -*- coding: utf-8 -*-

# Spider 1 
# Articles.py which scrape article links

# imports
import scrapy
from scrapy.http import Request
from mDaryoUz.items import MdaryouzItem



class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    allowed_domains = ['m.daryo.uz']
    start_urls = ['http://m.daryo.uz/']
    
    def start_requests(self):
        # Hardcoded URL that contains 10 article headlines with links each page.
        url="https://m.daryo.uz/page/{}/"
        number_of_total_pages = 19063 # This is pretty much all news since Daryo.uz started working in January 2013.
        link_urls = [url.format(i) for i in range(1,number_of_total_pages)]
        # Loops through all pages available to get the article links
        for link_url in link_urls:
            # print("#### Headline Page link: ", link_url)
            # Request to get the HTML content
            request=Request(link_url, cookies={'store_language':'uz'}, 
            callback=self.parse_main_pages)
            yield request
    
    def parse_main_pages(self,response):
        item=MdaryouzItem()
        # Gets HTML content where the article links are stored
        #content=response.xpath('//div[@id="items"]//div[@class="article-meta"]')
        content=response.xpath('//*[@id="content"]/div[1]/ul')
        # print("##### Content", content)
        # Loops through the each and every article link in HTML 'content'
        for article_link in content.xpath('.//a'):
            # print("##### Article link: ", article_link)
            # Extracts the href info of the link to store in scrapy item
            item['article_url'] =article_link.xpath('.//@href').extract_first()
            item['article_url'] ="https://m.daryo.uz"+item['article_url']
            yield(item)


    def parse(self, response):
        pass
