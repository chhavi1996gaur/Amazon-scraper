import scrapy
import pandas as pd
from ..items import AmazonScraperItem
#import csv
class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    page_num = 2
    allowed_domains = ['amazon.in']
    start_urls = ['https://www.amazon.in/s?i=electronics&bbn=1805560031&rh=n%3A976419031%2Cn%3A976420031%2Cn%3A1389401031%2Cn%3A1389432031%2Cn%3A1805560031%2Cp_36%3A2500000-%2Cp_85%3A10440599031&hidden-keywords=smartphone&pf_rd_i=1389401031&pf_rd_m=A1K21FY43GMZF8&pf_rd_p=b0d90f85-e375-4eb9-a5d5-da690b9019e8&pf_rd_r=VTZFS1H0JSE81E1WZ2AC&pf_rd_s=merchandised-search-20&pf_rd_t=101&ref=s9_acss_bw_cg_CPACSM20_8f1_w']
    #custom_settings = {'FEED_FORMAT' : 'csv', 'FEED_URI' : 'amazon_spider'}
    def parse(self,response):
        items = AmazonScraperItem()
        product_name = response.css(".a-color-base.a-text-normal").css('::text').extract()
        product_stars = response.xpath("//span[(@class='a-icon-alt')]/text()").extract()
        product_imagelink = response.css('.s-image::attr(src)').extract()
        product_price = response.css(".a-price-whole::text").extract()
        items['product_name'] = str(product_name).split(',')
        items['product_stars'] = str(product_stars).split(",")
        items['product_price'] = str(product_price).split("$")
        items['product_imagelink'] = str(product_imagelink).split(",")
        #yield {'name':product_name, 'stars':product_stars, 'imagelink':product_imagelink, 'price':product_price}
        for i in zip(product_name,product_stars,product_imagelink,product_price):
            info1 = {'name':i[0], 'stars':i[1], 'imagelink':i[2], 'price':i[3]}
            yield info1
            next_page = 'https://www.amazon.in/s?i=electronics&bbn=1805560031&rh=n%3A976419031%2Cn%3A976420031%2Cn%3A1389401031%2Cn%3A1389432031%2Cn%3A1805560031%2Cp_36%3A2500000-%2Cp_85%3A10440599031&page=' + str(AmazonSpiderSpider.page_num) +  '&hidden-keywords=smartphone&pf_rd_i=1389401031&pf_rd_m=A1K21FY43GMZF8&pf_rd_p=b0d90f85-e375-4eb9-a5d5-da690b9019e8&pf_rd_r=VTZFS1H0JSE81E1WZ2AC&pf_rd_s=merchandised-search-20&pf_rd_t=101&qid=1599292354&ref=sr_pg_1'
            if AmazonSpiderSpider.page_num<=10:
                AmazonSpiderSpider.page_num += 1
                yield response.follow(next_page, callback = self.parse)



