import scrapy
from scrapy.loader import ItemLoader
from engineer_lagbe.items import EngineerLagbeItem

class EnosisSpider(scrapy.Spider):
    name = 'enosis'
    allowed_domains = ['www.enosisbd.com']
    start_urls = [
        'https://www.enosisbd.com/careers/'
    ]

    def parse(self, response):
        circulars = response.xpath(".//ul[@class='joblist']//li")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.item["location"] = "Dhaka"
            loader.item['company_name'] = "Enosis"
            loader.add_xpath('post', ".//h2/text()")
            loader.add_xpath('link', ".//a/@href")
            engineer_lagbe_item = loader.load_item()
            yield scrapy.Request(circular.css('a::attr(href)').get(), callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

    def parse_details(self, response):
        engineer_lagbe_item = response.meta['engineer_lagbe_item']
        loader = ItemLoader(item=engineer_lagbe_item, response=response)
        loader.add_xpath('experience','.//div[@class="job-feature-title"][text()="Experience Requirements"]/following::ul[1]//li[1]/text()')
        loader.add_xpath('job_responsibility','.//div[@class="job-feature-title"][text()="Major Duties & Responsibilities"]/following::ul[1]//li/text()')
        loader.add_xpath('job_requirements','.//div[@class="job-feature-title"][text()="Qualifications & Requirements"]/following::ul[1]//li/text()')
        yield loader.load_item()