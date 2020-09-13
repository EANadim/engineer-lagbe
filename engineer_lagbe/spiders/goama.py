import scrapy
from scrapy.loader import ItemLoader
from engineer_lagbe.items import EngineerLagbeItem

def get_removed_bullet_point_list(bList):
    removed_bullet_point_list = []
    for li in bList:
        li = li.replace("● ", "").strip()
        removed_bullet_point_list.append(li)
    return removed_bullet_point_list

class GoamaSpider(scrapy.Spider):
    name = 'goama'
    allowed_domains = ['goama.com']
    start_urls = [
        'https://goama.com/category/careers/'
    ]

    def parse(self, response):
        circulars = response.xpath(".//div[@class='stm_loop stm_loop__grid']//div[contains(@id,'post')]")
        for circular in circulars:
            loader = ItemLoader(item=EngineerLagbeItem(), selector=circular)
            loader.item["location"] = "Dhaka"
            loader.item['company_name'] = "Goama"
            loader.add_xpath('posted_on', ".//li[@class='post_date']/text()")
            loader.add_xpath('link', ".//a/@href")
            loader.item['post'] = str(loader.get_xpath(".//span/text()")).replace("Position:", "").replace("['","").replace("']","").strip()
            engineer_lagbe_item = loader.load_item()
            yield scrapy.Request(circular.css('a::attr(href)').get(), callback=self.parse_details,
                                 meta={'engineer_lagbe_item': engineer_lagbe_item})

    def parse_details(self, response):
        engineer_lagbe_item = response.meta['engineer_lagbe_item']
        loader = ItemLoader(item=engineer_lagbe_item, response=response)
        experience = loader.get_xpath(".//div[@class='stm_mgb_20 stm_single_post__content']//p//strong[contains(text(), 'Experience')]//ancestor::p/following::p[1]/text()")
        experience = get_removed_bullet_point_list(experience)
        loader.item["experience"] = experience[0]
        salary_range = loader.get_xpath(".//div[@class='stm_mgb_20 stm_single_post__content']//p//strong[contains(text(), 'Salary')]//ancestor::p/following::p[1]/text()")
        salary_range = get_removed_bullet_point_list(salary_range)
        loader.item["salary_range"] = salary_range[0]
        job_responsibility = loader.get_xpath(".//div[@class='stm_mgb_20 stm_single_post__content']//p//strong[contains(text(), 'Requirements')]//ancestor::p/following::p[1]/text()")
        job_responsibility = get_removed_bullet_point_list(job_responsibility)
        loader.item['job_responsibility'] = job_responsibility

        yield loader.load_item()
