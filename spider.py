# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy



class SpiderSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['https://www.wildberries.ru/catalog/obuv/muzhskaya/kedy-i-krossovki/kedy']

    def parse(self, response):

        urls = response.css('a.ref_goods_n_p::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url = url, callback=self.parse_detail)


        next_url_page = response.css('a.next::attr(href)').extract_first()
        if next_url_page:
            next_url_page = response.urljoin(next_url_page)
            yield scrapy.Request(url = next_url_page, callback = self.parse)

        

    def parse_detail(self, response):        
        yield {
             'data' : datetime.now(),
             'brand' : response.css('div.brand-and-name > span.brand::text').extract_first(),
             'name' : response.css('div.brand-and-name > span.name::text').extract_first(),
             'href' : response.url,
             'current_price' : response.css('span.add-discount-text-price::text').get(default=''),
             'img' : response.css('img.preview-photo::attr(src)').extract_first(),
             'description' : response.css('div.j-description > p').extract_first()
         }       