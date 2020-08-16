import scrapy
from scrapy.loader import ItemLoader
from engineer_lagbe.items import EngineerLagbeItem

class BdJobsBdSpider(scrapy.Spider):
    name = 'bdjobsbd'
    allowed_domains = ['bdjobs.com.bd']
    start_urls = [
        'http://bdjobs.com.bd/CategoryJob/18'
    ]

    def parse(self, response):
        circulars = response.xpath(".//p[@class='br1']/../../../..")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.add_xpath('post', ".//p[@class='br1']/text()")
            loader.add_xpath('company_name', ".//p[@class='br2']/text()")
            loader.add_xpath('location', ".//span[@class='loc']/text()")
            loader.add_xpath('deadline', ".//div[@class='col-md-6']//p//span/text()")
            loader.add_xpath('posted_on', ".//i[@class='glyphicon glyphicon-calendar']/following::span[1]/text()")
            loader.add_css('link', "a::attr(href)")
            engineer_lagbe_item = loader.load_item()
            yield scrapy.Request(circular.css('a::attr(href)').get(), callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

        next_page = response.xpath(".//ul[@class='pagination']//ul[@class='pagination']//li[last()]//a/@href").get()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_details(self, response):
        engineer_lagbe_item = response.meta['engineer_lagbe_item']
        loader = ItemLoader(item=engineer_lagbe_item, response=response)
        loader.add_xpath('salary_range',
                         ".//div[@class='col-md-9 jb_details_ri8_mrgn']//div[@class='title_7'][text()='Salary Range']/following::div[@class='job_tex']/text()")
        loader.add_xpath('experience',
                         ".//div[@class='col-md-9 jb_details_ri8_mrgn']//div[@class='title_7'][text()='Experience Requirements']/following::div[@class='job_tex']//ul//li/text()")
        loader.add_xpath('educational_requirements',
                         ".//div[@class='col-md-9 jb_details_ri8_mrgn']//div[@class='title_7'][text()='Educational Requirements']/following::div[@class='job_tex'][1]//ul//li/text()")
        loader.add_xpath('job_responsibility',
                         ".//div[@class='col-md-9 jb_details_ri8_mrgn']//div[@class='title_7'][text()='Job Description / Responsibility']/following::div[@class='job_tex'][1]//ul//li/text()")
        loader.add_xpath('job_requirements',
                         ".//div[@class='col-md-9 jb_details_ri8_mrgn']//div[@class='title_7'][text()='Experience Requirements']/following::div[@class='job_tex'][1]//ul//li/text()")
        yield loader.load_item()
