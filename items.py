# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose
from scrapy.loader import processors

class JgzjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def return_value(value):
    return value

# def get_nums(value):
#     match_re = re.match(".*?(\d+).*", value)
#     if match_re:
#         nums = int(match_re.group(1))
#     else:
#         nums = 0
#
#     return nums
#
# class JgzjBookLoader(ItemLoader):
#     default_output_processor = TakeFirst()

class JgzjbookItem(scrapy.Item):
    # title = scrapy.Field(
    #     output_processor = MapCompose(return_value)
    # )
    # url = scrapy.Field(
    #     output_processor = MapCompose(return_value)
    # )
    # cover_img_url = scrapy.Field(
    #     output_processor = MapCompose(return_value)
    # )
    # cover_img_path = scrapy.Field(
    #     output_processor = MapCompose(return_value)
    # )
    # read_nums = scrapy.Field(
    #     input_processor = MapCompose(get_nums),
    #     output_processor = MapCompose(return_value)
    # )
    # comment_nums = scrapy.Field(
    #     input_processor = MapCompose(get_nums),
    #     output_processor = MapCompose(return_value)
    # )
    title = scrapy.Field()
    url = scrapy.Field()
    cover_img_url = scrapy.Field()
    cover_img_url_data = scrapy.Field()
    cover_img_path = scrapy.Field()
    read_nums = scrapy.Field()
    comment_nums = scrapy.Field()
