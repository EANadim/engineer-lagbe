import scrapy
from scrapy.loader import ItemLoader
from engineer_lagbe.items import EngineerLagbeItem


class JobBdSpider(scrapy.Spider):
    name = 'jobbd'
    allowed_domains = ['job.com.bd']
    start_urls = [
        'http://job.com.bd/jobs/?c=10'
    ]

    def parse(self, response):
        link_var = "http://job.com.bd/"
        circulars = response.xpath(".//table[3]//table[3]//tr[@class='w1']")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.add_xpath('post', ".//td[3]//a//label/text()")
            loader.add_xpath('company_name', ".//td[2]/text()")
            link = link_var + 'jobs/' + str(loader.get_xpath(".//td[3]//a/@href")[0])
            loader.item['link'] = link
            engineer_lagbe_item = loader.load_item()
            yield scrapy.Request(link, callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

        circulars = response.xpath(".//table[3]//table[3]//tr[@class='w2']")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.add_xpath('post', ".//td[3]//a//label/text()")
            loader.add_xpath('company_name', ".//td[2]/text()")
            link = link_var + 'jobs/' + str(loader.get_xpath(".//td[3]//a/@href")[0])
            loader.item['link'] = link
            engineer_lagbe_item = loader.load_item()
            yield scrapy.Request(link, callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

        next_page = response.xpath(".//table[3]//table[4]//tr[@class='whiteTitle']//td//a[last()]/@href").get()
        if next_page is not None:
            next_page = link_var + next_page.replace("../", "")
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_details(self, response):
        engineer_lagbe_item = response.meta['engineer_lagbe_item']
        loader = ItemLoader(item=engineer_lagbe_item, response=response)
        deadline = loader.get_xpath(".//table[2]//table[2]//table[1]//tr[2]//td[1]/text()")[0].replace("Published on :",
                                                                                                       "").strip()
        loader.item["deadline"] = deadline
        posted_on = loader.get_xpath(".//table[2]//table[2]//table[1]//tr[2]//td[2]/text()")[0].replace(
            "Application Deadline:", "").strip()
        loader.item["posted_on"] = posted_on
        loader.add_xpath('location',
                         ".//table[2]//table[2]//table[1]//tr//td[1][text()='Job Location']/following::td[2]/text()")
        loader.add_xpath('salary_range',
                         ".//table[2]//table[2]//table[1]//tr//td[1][text()='Salary']/following::td[2]/text()")
        loader.add_xpath('experience',
                         ".//table[2]//table[2]//table[1]//tr//td[1][text()='Experience']/following::td[2]//li/text()")
        educational_requirements = loader.get_xpath(
            ".//table[2]//table[2]//table[1]//tr//td[1][text()='Educational Requirement']/following::td[2]/text()")[0]
        educational_requirements = [educational_requirements.strip()]
        loader.item["educational_requirements"] = educational_requirements
        job_responsibility = loader.get_xpath(
            ".//table[2]//table[2]//table[1]//tr//td[1][text()='Responsibilities']/following::td[2]//li/text()")
        loader.item["job_responsibility"] = job_responsibility

        yield loader.load_item()
