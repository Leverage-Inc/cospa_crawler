# -*- coding: utf-8 -*-
import scrapy
from cospa_crawler.items import CospaCrawlerItem 

class ScrapyCospaSpiderSpider(scrapy.Spider):
    name            = 'scrapy_cospa_spider'
    allowed_domains = ['www.ogsports.co.jp']
    start_urls      = ['https://www.ogsports.co.jp/']

    def parse(self, response):
        """
        Topページ下部フッターから各店舗個別ページのURLリストを作成
        そのリストに対してリクエストをかけて、parse_store_page関数を呼び出す
        """
        item        = CospaCrawlerItem()
        store_links = response.css('div#storeList ul.clr a::attr(href)').getall() # type：list

        # 各店舗urlにリクエストをかけて、parse_store_pageを呼び出す
        for store_link in store_links[:5]:
            # URLが相対パスだった場合に絶対パスに変換する
            print(store_link)
            store_link           = response.urljoin(store_link)
            request              = scrapy.Request(url=store_link, callback=self.parse_store_page)
            request.meta['item'] = item  # Requestのmetaにitemを格納しておく。そしたらメソッド間で受け渡し可能 
            yield request

    def parse_store_page(self, response):
        """
        店舗情報のテーブルがあるクラスを取得して、項目とその内容を取得
        取得した項目とその内容をitem内にプッシュ
        各ジムのコース一覧情報が記載されているURLを取得して、そのURLに対してリクエストをかけて
        parse_course_page関数を呼び出す
        """
        item               = response.meta['item']
        item["store_name"] = response.css('div.ttlInner a::text').get().strip()
        item["store_url"]  = response.urljoin(response.url)  
        #「店舗情報」のテーブルの各行を取得
        store_tr_tags     = response.css('div.clr tr')
        for store_tr_tag in store_tr_tags:
            # 取得した各行の項目名（thタグのtext）を取得
            store_th_tag  = store_tr_tag.css('th::text').get()          

            # 取得した項目名が条件と一致した場合 2列目（tdタグのテキスト）の情報を取得
            if store_th_tag == "住所":
                item["city"]           = store_tr_tag.css("td").xpath("string()").get().strip()

            if store_th_tag == "アクセス":
                item["access"]         = store_tr_tag.css("td").xpath("string()").get().strip()

            if store_th_tag == "電話番号":
                item["tel"]            = store_tr_tag.css("td").xpath("string()").get().strip()

            if store_th_tag == "営業時間":
                item["business_hours"] = store_tr_tag.css("td").xpath("string()").get().strip()

            if store_th_tag == "設備":
                item["facility"]       = store_tr_tag.css("img").xpath("@alt").getall()

        # 各ジムのコース一覧情報が記載されているページのurlを取得
        course_link          = response.urljoin(response.css('li#navPrice a::attr(href)').get())
        request              = scrapy.Request(url=course_link, callback=self.parse_course_page)

        request.meta['item'] = item
        yield request

    def parse_course_page(self, response):
        """
        コース一覧のテーブルから列ごとに取得してから、
        listの状態でitemにプッシュする。
        """
        item           = response.meta['item'] 

        # コース一覧（料金表）のテーブルから各行を取得
        course_table        = response.css('table.storeTable2.table01')[0]
        course_tr_tags      = course_table.css('tr')[1:]
        course_td_text      = course_tr_tags.css('td').xpath('string()').getall()
        item["course_list"] = course_td_text
        
        # 各列のデータを取得して、配列に追加してitemに入れる
        return item





