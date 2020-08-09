from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.item import Item, Field


class EngineerLagbeItem(Item):
    company_name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    post = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    location = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    deadline = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    link = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    experience = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    salary_range = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    educational_requirements = Field()
    job_responsibility = Field()
    posted_on = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
