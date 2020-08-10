import scrapy
from scrapy.loader import ItemLoader
from engineer_lagbe.items import EngineerLagbeItem
from scrapy_splash import SplashRequest


class BdJobsBdSpider(scrapy.Spider):
    name = 'bdjobs'
    allowed_domains = ['bdjobs.com']
    start_urls = [
        'https://jobs.bdjobs.com/jobsearch.asp?fcatId=8'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                                endpoint='render.html',
                                args={'wait': 2.0},
                                )
            # yield SplashRequest(url, self.parse, endpoint='render.html',
            #                     args={'wait': 0.5, 'viewport': '1024x2480', 'timeout': 90, 'images': 0})

    def parse(self, response):
        link_var = "https://jobs.bdjobs.com/"
        circulars = response.xpath(".//div[@class='norm-jobs-wrapper']")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.add_xpath('post', ".//div[@class='job-title-text']//a/text()")
            loader.add_xpath('company_name', ".//div[@class='comp-name-text']/text()")
            link = link_var + str(loader.get_xpath(".//div[@class='job-title-text']//a/@href")[0])
            loader.item['link'] = link
            engineer_lagbe_item = loader.load_item()
            yield scrapy.Request(link, callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

        circulars = response.xpath(".//div[@class='south-jobs-wrapper']")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.add_xpath('post', ".//div[@class='job-title-text']//a/text()")
            loader.add_xpath('company_name', ".//div[@class='comp-name-text']/text()")
            link = link_var + str(loader.get_xpath(".//div[@class='job-title-text']//a/@href")[0])
            loader.item['link'] = link
            engineer_lagbe_item = loader.load_item()
            yield scrapy.Request(link, callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

        circulars = response.xpath(".//div[@class='sout-jobs-wrapper']")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.add_xpath('post', ".//div[@class='job-title-text']//a/text()")
            loader.add_xpath('company_name', ".//div[@class='comp-name-text']/text()")
            link = link_var + str(loader.get_xpath(".//div[@class='job-title-text']//a/@href")[0])
            loader.item['link'] = link
            engineer_lagbe_item = loader.load_item()
            yield scrapy.Request(link, callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

        # next_page = response.xpath(".//ul[@class='pagination']//ul[@class='pagination']//li[last()]//a/@href").get()
        # if next_page is not None:
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_details(self, response):
        engineer_lagbe_item = response.meta['engineer_lagbe_item']
        loader = ItemLoader(item=engineer_lagbe_item, response=response)
        loader.add_xpath('posted_on',
                         ".//div[@class='panel-body']//h4//strong[text()='Published on:']/following::text()")
        loader.add_xpath('salary_range', ".//div[@class='panel-body']//h4//strong[text()='Salary:']/following::text()")
        loader.add_xpath('experience',
                         ".//div[@class='panel-body']//h4//strong[text()='Experience:']/following::text()")
        loader.add_xpath('deadline',
                         ".//div[@class='panel-body']//h4//strong[text()='Application Deadline:']/following::text()")
        loader.add_xpath('location',
                         ".//div[@class='panel-body']//h4//strong[text()='Job Location:']/following::text()")
        loader.item["job_responsibility"] = [item.strip() for item in loader.get_xpath(
            ".//div[@class='job_des']//h5[text()='Job Responsibilities ']/following::ul[1]//li/text()")]
        loader.item["educational_requirements"] = [item.strip() for item in loader.get_xpath(
            ".//div[@class='edu_req']//h5[text()='Educational Requirements']/following::ul[1]//li/text()")]
        yield loader.load_item()
