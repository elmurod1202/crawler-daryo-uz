# Crawler - Daryo.uz: Extracting the Raw Text Data from the WEB

Daryo.UZ Crawler is a website crawler that uses [Scrapy](https://scrapy.org/) framework.
Initially I wanted to collect some text data from news websites in Uzbek language for NER annotation. 
So I set this up to collect all news articles from daryo.uz (used its mobile version: m.daryo.uz for simplicity) website in case I need more text data in the future.


## Using this code

Just clone this repository using git.

```bash
git clone git@github.com:elmurod1202/daryo-crawler.git
```

## Installation

Assuming that you already have Python already, it is necessary to install Scrapy framework as well. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Scrapy and start your project.

```bash
# Install the scrapy first
$ pip install scrapy
```
Now, you can Either use this repo as a project as it is, or start a new web scraping project with scrapy as follows:
*NOTE: you don't need to start a new project if you are planning to use/edit this repo.*
```bash
$ scrapy startproject mDaryoUz
$ cd mDaryoUz
mDaryoUz $ scrapy genspider articles m.daryo.uz
mDaryoUz $ scrapy genspider articleScraper m.daryo.uz
```

## Usage
We setup items class and two Scrapy spiders in this project:

### Data structure setup:
Based on what data you need to scrape from a website, fields have to be set up.
Inside the project folder, the *items.py* should look like this: 

```python
import scrapy

class MdaryouzItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_url = scrapy.Field()
    article_title = scrapy.Field()
    article_category = scrapy.Field()
    article_metadata = scrapy.Field()
    article_body = scrapy.Field()    
    pass
```

### First Spider
Our first spider which is “articles.py” will get the article links by visiting all (19063 in my case) m.daryo.uz web pages. It will be extracting the href information of the article links available (10 article links each webpage in my case) at each page and storing them in a JSON file.

```python
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
```
After we finalized our first spider, we can now run it with the below command to generate “article_links” JSON file. 

*NOTE: When crawling webpages, it is recommended to follow target web server's robots.txt and setup your crawler with autoThrotlle activated. Read Scrapy docs for more info.* 

```bash
mDaryoUz $ scrapy crawl -o article_links.json -t json articles
```
When spider finishes crawling, article_links.json file should look like this:

```json
[
{"article_url": "https://m.daryo.uz/2021/03/09/shavkat-mirziyoyev-turkiya-tashqi-ishlar-vaziri-mavlud-chavushoglini-qabul-qildi/"},
{"article_url": "https://m.daryo.uz/2021/03/09/hyundai-ioniq-5-elektrokari-oldindan-buyurtmalar-borasidagi-rekordni-yangiladi/"},
{"article_url": "https://m.daryo.uz/2021/03/09/ozbekiston-kasaba-uyushmalari-federatsiyasi-rahbari-fermerlar-kengashi-raisi-orinbosarini-prezidentni-aldayotganlikda-aybladi/"},
{"article_url": "https://m.daryo.uz/2021/03/09/bekajonlar-uchun-tavsiya-vanna-tozalashning-gayrioddiy-ammo-eng-qulay-usuli/"},
{"article_url": "https://m.daryo.uz/2021/03/09/key-liga-rustam-ashurmatov-jamoasi-songgi-daqiqalarda-2-ta-gol-otkazib-galabani-boy-berdi/"},
...
]
```

### Second Spider.
The next step is to scrape the news articles using the links stored in the JSON file. To do this, let’s create our second spider which is “ArticleScraper”.

```python
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
```
Below command runs the articleScraper spider and generates a JSON file containing the news articles. 

```bash
mDaryoUz $ scrapy crawl -o article_body.json -t json articleScraper
```

You can see below the content of the JSON file that the spider produced.

```json
[
{"article_title": ["Shavkat Mirziyoyev Turkiya tashqi ishlar vaziri Mavlud Chavusho\u2018g\u2018lini qabul qildi"], "article_category": ["Mahalliy"], "article_metadata": ["19:59 Kecha  //  21227"], "article_body": " O\u2018zbekiston Prezidenti...."},
{"article_title": ["Hyundai Ioniq 5 elektrokari oldindan buyurtmalar borasidagi rekordni yangiladi"], "article_category": ["Avto"], "article_metadata": ["19:48 Kecha  //  13867"], "article_body": " Hyundai Ioniq 5\u2019ning taqdimotidan bir ne...."},
{"article_title": ["O\u2018zbekiston kasaba uyushmalari federatsiyasi rahbari Fermerlar kengashi raisi o\u2018rinbosarini Prezidentni aldayotganlikda aybladi"], "article_category": ["Mahalliy"], "article_metadata": ["19:39 Kecha  //  28056"],"...."},
{"article_title": ["Bekajonlar uchun tavsiya: vanna tozalashning g\u2018ayrioddiy, ammo eng qulay usuli"], "article_category": ["Maslahatlar"], "article_metadata": ["19:26 Kecha  //  19140"], "article_body": " Ushbu noodatiy usul egilishi qiyi...."},
...
]
```

### Rearranging collected data:
You can reorganize the obtained data as you need. In my case, I made the json format simpler, added an ID element to each news article, recategorized them and also saved all texts in a single text file.
You can use *article_add_ids.py* for that:
```bash
python article_add_ids.py
```
