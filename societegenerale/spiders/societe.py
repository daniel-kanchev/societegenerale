import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from societegenerale.items import Article
from datetime import datetime


class SocieteSpider(scrapy.Spider):
    name = 'societe'
    allowed_domains = ['societegenerale.com']
    start_urls = ['https://www.societegenerale.com/en/news/newsroom']

    def parse(self, response):
        articles = response.xpath('//ul//article')
        for article in articles:
            link = article.xpath('.//a/@href').get()
            date = article.xpath('.//span[@class="date"]/text()').get()
            category = article.xpath('.//strong[@class="tag"]/text()').get()
            yield response.follow(link, self.parse_article, cb_kwargs=dict(date=date, category=category))

        next_page = response.xpath('//a[@title="Go to next page"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response, date, category):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        try:
            title = response.xpath('//h1//text()').get()
        except:
            print('skip')
            return

        date = date.split()[-1]
        date = datetime.strptime(date, '%d/%m/%Y')
        date = date.strftime('%Y/%m/%d')

        content = response.xpath('//div[@class="sgnews_single_content"]//text()').getall()
        if not content:
            content = response.xpath('//div[@class="paragraph default-padding default-width paragraph--type--rte"]'
                                     '//text()').getall()
        content = " ".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('category', category)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
