# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CospaCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    store_name         = scrapy.Field() # 店舗名
    city               = scrapy.Field() # 住所
    tel                = scrapy.Field() # 電話番号
    access             = scrapy.Field() # アクセス
    business_hours     = scrapy.Field() # 営業時間
    
    course_list        = scrapy.Field() # コースリスト
    # course_price       = scrapy.Field() # 料金
    # course_description = scrapy.Field() # コースの説明
    # course_time        = scrapy.Field() # コースの利用可能時間・曜日
    facility           = scrapy.Field() # 設備
    remarks            = scrapy.Field() # 備考
    store_url          = scrapy.Field() # 店舗のURL