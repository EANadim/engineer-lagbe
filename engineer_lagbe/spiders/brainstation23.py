import scrapy
from scrapy.loader import ItemLoader
from engineer_lagbe.items import EngineerLagbeItem


class BrainStation23(scrapy.Spider):
    name = 'brainstation23'
    allowed_domains = ['erp.bs-23.com']
    start_urls = [
        'https://erp.bs-23.com/jobs'
    ]

    def parse(self, response):
        link_var = self.start_urls[0].replace("/jobs", "")
        circulars = response.xpath(".//li[@class='media']")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.item['company_name'] = "Brainstation 23"
            loader.add_xpath('post', ".//h3[@class='media-heading']//span/text()")
            loader.add_xpath('location', ".//span[@itemprop='streetAddress']/text()")
            posted_on = str(loader.get_xpath(".//i[@class='fa fa-clock-o']/following::span[1]/text()")[0])
            loader.item["posted_on"] = posted_on[:10]
            link = link_var + str(loader.get_xpath(".//h3[@class='media-heading']//a/@href")[0])
            loader.item["link"] = link
            engineer_lagbe_item = loader.load_item()
            yield scrapy.Request(link, callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

    def parse_details(self, response):
        engineer_lagbe_item = response.meta['engineer_lagbe_item']
        loader = ItemLoader(item=engineer_lagbe_item, response=response)

        loader.add_xpath('educational_requirements', ".//div[@class='col-sm-6 mb92 mt64 col-md-6']//span/text()")
        educational_requirements = []
        educational_requirements = loader.get_xpath(
            ".//div[@class='col-sm-6 mb92 mt64 col-md-6']//span[1]/text()") if loader.get_xpath(
            ".//div[@class='col-sm-6 mb92 mt64 col-md-6']//span[1]/text()") != [] else educational_requirements
        educational_requirements = loader.get_xpath(
            ".//div[@class='col-sm-6 col-md-5 mt16 mb128']//span[1]/text()") if loader.get_xpath(
            ".//div[@class='col-sm-6 col-md-5 mt16 mb128']//span[1]/text()") != [] else educational_requirements
        educational_requirements = loader.get_xpath(
            ".//div[@class='col-sm-6 mt0 col-md-5']//span[1]/text()") if loader.get_xpath(
            ".//div[@class='col-sm-6 mt0 col-md-5']//span[1]/text()") != [] else educational_requirements
        if len(educational_requirements):
            educational_requirements = [educational_requirements[0]]
        loader.item["educational_requirements"] = educational_requirements

        job_requirements = []
        job_requirements = loader.get_xpath(
            ".//div[@class='col-sm-6 mt0 mb0 col-md-6']//p//sub//span/text()") if loader.get_xpath(
            ".//div[@class='col-sm-6 mt0 mb0 col-md-6']//p//sub//span/text()") != [] else job_requirements
        loader.item["job_requirements"] = job_requirements

        # job_responsibility = []
        # for span_tag in loader.get_xpath(".//div[@class='col-sm-6 col-md-7']//ul[1]/li//span"):
        #     job_responsibility.append("".join(span_tag.get_xpath("//text()")))
        # loader.item["job_responsibility"] = job_responsibility
        yield loader.load_item()
