import scrapy
from scrapy.loader import ItemLoader
from engineer_lagbe.items import EngineerLagbeItem


class BjitSpider(scrapy.Spider):
    name = 'bjit'
    allowed_domains = ['bjitgroup.com']
    start_urls = [
        'https://bjitgroup.com/career/'
    ]

    def parse(self, response):
        circulars = response.xpath(".//div[@class='career_list'][1]//table[@class='table'][1]//tr")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.item['company_name'] = "BJIT"
            loader.item['location'] = "Dhaka"
            loader.add_xpath('post', ".//td[2]//div[@class='job_name']//h3/text()")
            posted_on = loader.get_xpath(".//div[@class='job_time'][1]/text()")[1]
            posted_on = posted_on.replace("Post Date :", "")
            posted_on = posted_on.replace("\r\n", "")
            loader.item["posted_on"] = posted_on.strip()

            deadline = loader.get_xpath(".//div[@class='job_time'][2]/text()")[1]
            deadline = deadline.replace("Deadline :", "")
            deadline = deadline.replace("\r\n", "")
            loader.item["deadline"] = deadline.strip()

            loader.add_xpath('link', ".//a[@class='view_btn']/@href")
            engineer_lagbe_item = loader.load_item()

            yield scrapy.Request(circular.css('a::attr(href)').get(), callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

    def parse_details(self, response):
        engineer_lagbe_item = response.meta['engineer_lagbe_item']
        loader = ItemLoader(item=engineer_lagbe_item, response=response)
        loader.add_xpath('experience', ".//div[@class='job-position']/ul[1]//li[2]/text()")

        loader.add_xpath('job_responsibility',
                         ".//div[@class='job-info']//p[@class='MsoNormal']//span//strong//span[text()='Job Responsibilities ']/ancestor::span/ancestor::p/following::ul[1]//li//span/text()")
        job_responsibility = []
        job_responsibility = loader.get_xpath(
            ".//div[@class='job-info']//p[@class='MsoNormal']//span//strong//span[text()='Job Responsibilities ']/ancestor::span/ancestor::p/following::ul[1]//li//span/text()") if loader.get_xpath(
            ".//div[@class='job-info']//p[@class='MsoNormal']//span//strong//span[text()='Job Responsibilities ']/ancestor::span/ancestor::p/following::ul[1]//li//span/text()") != [] else job_responsibility
        job_responsibility = loader.get_xpath(
            ".//div[@class='job-info']//div[@class='job_des']//h5//span[text()=' Job Responsibilities ']/ancestor::h5//following::ul[1]//li//span/text()") if loader.get_xpath(
            ".//div[@class='job-info']//div[@class='job_des']//h5//span[text()=' Job Responsibilities ']/ancestor::h5//following::ul[1]//li//span/text()") != [] else job_responsibility

        loader.item["job_responsibility"] = job_responsibility
        yield loader.load_item()
