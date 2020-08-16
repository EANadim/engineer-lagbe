import scrapy
from scrapy.loader import ItemLoader
from engineer_lagbe.items import EngineerLagbeItem

class CefaloSpider(scrapy.Spider):
    name = 'cefalo'
    allowed_domains = ['www.cefalo.com']
    start_urls = [
        'https://www.cefalo.com/career'
    ]

    def parse(self, response):
        circulars = response.xpath(".//div[@class='custom-column-wrap']")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.item['company_name'] = "Cefalo"
            loader.add_xpath('post', ".//h3/text()")
            loader.add_xpath('link', ".//a[@class='more-button']/@href")
            engineer_lagbe_item = loader.load_item()

            yield scrapy.Request(circular.css('a::attr(href)').get(), callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

    def parse_details(self, response):
        engineer_lagbe_item = response.meta['engineer_lagbe_item']
        loader = ItemLoader(item=engineer_lagbe_item, response=response)
        loader.add_xpath('location','.//strong[text()="Job Location:"]/following::ul[1]//li[1]/text()')
        loader.add_xpath('deadline','.//strong[text()="Application Deadline:"]/following::ul[1]//li[1]//strong[1]//span[1]/text()')
        loader.add_xpath('job_requirements','.//strong[text()="Job Requirements:"]/following::ul[1]//li/text()')
        loader.add_xpath('educational_requirements','.//strong[text()="Educational Requirements:"]/following::ul[1]//li/text()')

        yield loader.load_item()