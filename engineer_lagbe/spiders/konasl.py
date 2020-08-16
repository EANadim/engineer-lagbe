import scrapy
from scrapy.loader import ItemLoader
from engineer_lagbe.items import EngineerLagbeItem


class KonaslSpider(scrapy.Spider):
    name = 'konasl'
    allowed_domains = ['konasl.com']
    start_urls = [
        'https://konasl.com/life-at-konasl/career-journey/'
    ]

    def parse(self, response):
        circulars = response.xpath(".//div[@class='vc_row wpb_row vc_row-fluid vc_custom_1567582041518']")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.item["location"] = "Dhaka"
            loader.item['company_name'] = "Kona Software Lab Ltd"
            loader.add_xpath('post', ".//h3[@class='title']/text()")
            div_id = loader.get_xpath(".//a/@href")[0].strip()
            link = self.start_urls[0] + div_id
            div_id = div_id.replace("#", "")
            loader.item['link'] = link
            loader.add_xpath('job_requirements',
                             ".//div[@id='" + div_id + "']//div[@class='vc_tta-panel-body']//p//strong[text()='Minimum Technical Expectations']/ancestor::p/following::ul[1]//li/text()")
            loader.add_xpath('educational_requirements',
                             ".//div[@id='" + div_id + "']//div[@class='vc_tta-panel-body']//p//strong[text()='Education and Experience']/ancestor::p/following::p[1]/text()")
            loader.add_xpath('experience',
                             ".//div[@id='" + div_id + "']//div[@class='vc_tta-panel-body']//p//strong[text()='Education and Experience']/ancestor::p/following::p[2]/text()")

            yield loader.load_item()
