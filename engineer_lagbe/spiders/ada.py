import scrapy
from scrapy.loader import ItemLoader
from engineer_lagbe.items import EngineerLagbeItem
from scrapy_splash import SplashRequest


class AdaSpider(scrapy.Spider):
    name = 'ada'
    allowed_domains = ['ada.bamboohr.com']
    start_urls = [
        'https://ada.bamboohr.com/jobs/'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, args={'wait': 0.5}, callback=self.parse, endpoint='render.html')

    def parse(self, response):
        circulars = response.xpath(".//li[@class='ResAts__card-content ResAts__listing']")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.item['company_name'] = "Ada"
            loader.item['location'] = "Dhaka"
            link = "https://ada.bamboohr.com/jobs/"
            location = loader.get_xpath(".//div[@class='AtsLead truncate']/text()")[0]
            if location == "Dhaka":
                loader.add_xpath('post', ".//a[@class='ResAts__listing-link']/text()")
                halflink = loader.get_xpath(".//a[@class='ResAts__listing-link']/@href")[0]
                link = link+halflink
                loader.item['link'] = link
                engineer_lagbe_item = loader.load_item()
                yield scrapy.Request(link, callback=self.parse_details,
                                     meta={'engineer_lagbe_item': engineer_lagbe_item})

    def parse_details(self, response):
        engineer_lagbe_item = response.meta['engineer_lagbe_item']
        loader = ItemLoader(item=engineer_lagbe_item, response=response)
        loader.add_xpath('experience', ".//div[@class='ResAts__sideBar js-jobs-sidebar col-md-4']//li[@class='posInfo "
                                       "posInfo--minExperience']/div[2]/text()") 
        loader.item['job_responsibility'] = response.xpath(".//div[@class='col-xs-12 BambooRichText']/ul["
                                                           "1]/li/span/text()").extract()
        loader.item['job_requirements'] = response.xpath(".//div[@class='col-xs-12 BambooRichText']/ul["
                                                         "2]/li/span/text()").extract()
        yield loader.load_item()

