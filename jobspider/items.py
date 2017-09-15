# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Job51Item(scrapy.Item):
    id= scrapy.Field()
    link=scrapy.Field()
    companyname=scrapy.Field()
    companydescription=scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    salary = scrapy.Field()
    time_range=scrapy.Field()
    contact_phonenum=scrapy.Field()
    edu=scrapy.Field()
    count=scrapy.Field()
    updatetime=scrapy.Field()
    linker=scrapy.Field()
    lang=scrapy.Field()
    email=scrapy.Field()
    benefit=scrapy.Field()
    responsibility=scrapy.Field()
    qualification=scrapy.Field()
    address=scrapy.Field()

    pass

