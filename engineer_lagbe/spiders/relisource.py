import scrapy
from scrapy.loader import ItemLoader
from engineer_lagbe.items import EngineerLagbeItem

class RelisourceSpider(scrapy.Spider):
    name = 'relisource'
    allowed_domains = ['relisource.com']
    start_urls = [
        'https://relisource.com/careers/'
    ]

    def parse(self, response):
        circulars = response.xpath(".//ul[@class='styled-list']/li")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.item['company_name'] = "Relisource"
            loader.add_xpath('post', "./a/text()")
            loader.add_xpath('link', "./a/@href")
            engineer_lagbe_item = loader.load_item()
            yield scrapy.Request(circular.xpath("./a/@href").get(), callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

    def parse_details(self, response):
        engineer_lagbe_item = response.meta['engineer_lagbe_item']
        loader = ItemLoader(item=engineer_lagbe_item, response=response)
        loader.add_xpath('location', ".//div[@class='page-content']/div[2]/text()")
        loader.add_xpath('deadline', ".//div[@class='page-content']/div[1]/text()")
        loader.add_xpath('experience', ".//div[@class='page-content']/div[5]/text()")
        loader.add_xpath('salary_range', ".//div[@class='page-content']/div[9]/ul/li[1]/text()")
        loader.item['educational_requirements'] = response.xpath(".//div[@class='page-content']/div[4]/ul/li/text()").extract()
        if response.xpath(".//div[@class='page-content']/div[4]/ul/li/text()").extract() == []:
            loader.item['educational_requirements'] = response.xpath(
                ".//div[@class='page-content']/div[4]/div/ul/li/text()").extract()

        loader.item['job_responsibility'] = response.xpath(".//div[@class='page-content']/div[3]/text()").extract()
        loader.item['job_requirements'] = response.xpath(".//div[@class='page-content']/div[7]/ul/li/text()").extract()

        yield loader.load_item()