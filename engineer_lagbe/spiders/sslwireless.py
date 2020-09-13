import scrapy
from scrapy.loader import ItemLoader
from engineer_lagbe.items import EngineerLagbeItem


class SslWirelessSpider(scrapy.Spider):
    name = 'sslwireless'
    allowed_domains = ['www.sslwireless.com']
    start_urls = [
        'https://www.sslwireless.com/careers/'
    ]

    def parse(self, response):
        circulars = response.xpath(
            ".//section[@class='space--sm']//div[@class='container']//div[@class='row']//div[@class='col-sm-4']")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.add_xpath('location', ".//div[@class='feature feature-1 boxed boxed--border']//p/text()")
            loader.add_xpath('post', ".//div[@class='feature feature-1 boxed boxed--border']//h5/text()")
            loader.item['company_name'] = "SSL WIRELESS"
            loader.add_xpath('link', ".//a/@href")
            engineer_lagbe_item = loader.load_item()
            yield scrapy.Request(circular.css('a::attr(href)').get(), callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

    def parse_details(self, response):
        engineer_lagbe_item = response.meta['engineer_lagbe_item']
        loader = ItemLoader(item=engineer_lagbe_item, response=response)
        job_requirements = []
        job_requirements = loader.get_xpath(
            ".//h5[contains(text(), 'Required Skills/Knowledge:')]/following::ul[1]//li/text()") if loader.get_xpath(
            ".//h5[contains(text(), 'Required Skills/Knowledge:')]/following::ul[1]//li/text()") != [] else job_requirements
        job_requirements = loader.get_xpath(
            ".//h5[contains(text(), 'Required Skills/Knowledge:')]/following::ul[1]//li//span/text()") if loader.get_xpath(
            ".//h5[contains(text(), 'Required Skills/Knowledge:')]/following::ul[1]//li//span/text()") != [] else job_requirements

        loader.item["job_requirements"] = job_requirements

        try:
            exp_edu_reqs = loader.get_xpath(".//h5[contains(text(), 'Experience & Academic Requirements')]/following::p/text()")
            loader.item["experience"] = exp_edu_reqs[0]
            loader.item["educational_requirements"] = exp_edu_reqs[1]
        except Exception as ex:
            print(ex)

        yield loader.load_item()
