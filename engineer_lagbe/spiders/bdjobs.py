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
    script = """"
    function main(splash)
      assert(splash:autoload("https://code.jquery.com/jquery-3.1.1.min.js"))
      assert(splash:go("https://jobs.bdjobs.com/jobsearch.asp?fcatId=8"))
      assert(splash:wait(10.0))
      assert(splash:runjs('document.getElementsByClassName("prevnext")[1].click()'))
      assert(splash:wait(10.0))
      return {
        html = splash:html()
        }
        end
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                                endpoint='render.html',
                                args={'wait': 2.0},
                                )

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

        javascript = response.xpath(".//a[@class='prevnext'][text()='Next »']/@href").get()
        if javascript:
            yield SplashRequest(self.start_urls[0], self.parse,
                                # cookies={'store_language': 'en'},
                                endpoint='execute',
                                args={'lua_source': self.script, 'javascript': javascript, 'wait': 5.0})

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
