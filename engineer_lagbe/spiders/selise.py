import scrapy
from scrapy.loader import ItemLoader
from engineer_lagbe.items import EngineerLagbeItem

class SeliseSpider(scrapy.Spider):
    name = 'selise'
    allowed_domains = ['selise.ch']
    start_urls = [
        'https://selise.ch/career/'
    ]

    def parse(self, response):
        circulars = response.xpath(".//div[@class='job-posts-attributes']")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            location = loader.get_xpath(".//div[@class='locations']//span/text()")[0]
            if location.find("Dhaka"):
                continue
            loader.item['location'] = location
            loader.item['company_name'] = "Selise"
            loader.add_xpath('post', ".//div[@class='title']//h3/text()")
            loader.add_css('link', "a::attr(href)")
            engineer_lagbe_item = loader.load_item()
            yield scrapy.Request(circular.css('a::attr(href)').get(), callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

    def parse_details(self, response):
        engineer_lagbe_item = response.meta['engineer_lagbe_item']
        loader = ItemLoader(item=engineer_lagbe_item, response=response)
        job_responsibility = []
        job_responsibility = loader.get_xpath(".//div[@class='job-description']//h3[text()='What you’ll do']/following::ul[1]//li//span/text()") if loader.get_xpath(".//div[@class='job-description']//h3[text()='What you’ll do']/following::ul[1]//li//span/text()")!=[] else job_responsibility
        job_responsibility = loader.get_xpath(".//div[@class='job-description']//h3[text()='What you’ll do']/following::ul[1]//li/text()") if loader.get_xpath(".//div[@class='job-description']//h3[text()='What you’ll do']/following::ul[1]//li/text()")!=[] else job_responsibility
        job_responsibility = loader.get_xpath(".//div[@class='job-description']//h3[text()='What you will do']/following::ul[1]//li//span/text()") if loader.get_xpath(".//div[@class='job-description']//h3[text()='What you will do']/following::ul[1]//li//span/text()")!=[] else job_responsibility
        job_responsibility = loader.get_xpath(".//div[@class='job-description']//h3[text()='What you will do']/following::ul[1]//li/text()") if loader.get_xpath(".//div[@class='job-description']//h3[text()='What you will do']/following::ul[1]//li/text()")!=[] else job_responsibility
        job_responsibility = loader.get_xpath('.//div[@class="job-description"]//h3[text()="What you\'ll do"]/following::ul[1]//li//span/text()') if loader.get_xpath('.//div[@class="job-description"]//h3[text()="What you\'ll do"]/following::ul[1]//li//span/text()')!=[] else job_responsibility
        job_responsibility = loader.get_xpath('.//div[@class="job-description"]//h3[text()="What you\'ll do"]/following::ul[1]//li/text()') if loader.get_xpath('.//div[@class="job-description"]//h3[text()="What you\'ll do"]/following::ul[1]//li/text()')!=[] else job_responsibility
        loader.item['job_responsibility'] = job_responsibility

        job_requirements = []
        job_requirements = loader.get_xpath(".//div[@class='job-description']//h3[text()='Who you are']/following::ul[1]//li//span/text()") if loader.get_xpath(".//div[@class='job-description']//h3[text()='Who you are']/following::ul[1]//li//span/text()")!=[] else job_requirements
        job_requirements = loader.get_xpath(".//div[@class='job-description']//h3[text()='Who you are']/following::ul[1]//li/text()") if loader.get_xpath(".//div[@class='job-description']//h3[text()='Who you are']/following::ul[1]//li/text()")!=[] else job_requirements
        loader.item['job_requirements'] = job_requirements

        yield loader.load_item()