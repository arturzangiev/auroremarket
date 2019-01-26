# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['auroremarket.fr']
    start_urls = [
        'https://auroremarket.fr/s-1/en_stock-oui?p=1',
    ]

    def parse(self, response):
        urls = response.xpath('//a[@class="product_img_link"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

        # Calling next page
        for page in range(2, 80):
            next_page_url = 'https://auroremarket.fr/s-1/en_stock-oui?p={}'.format(page)
            yield scrapy.Request(url=next_page_url)

    def individual_page(self, response):
        fields = dict()
        fields["base_price"] = response.xpath('//span[@class="am_old_price"]/text()').re_first('(\d+\,\d+) €')
        fields["discounted_price"] = response.xpath('//p[@class="our_price_display"]/span[@class="price"]/@content').extract_first()
        fields["product_name"] = response.xpath('//h1[@class="am_marque_title "]/text()').extract_first().strip()
        fields["category"] = response.xpath('//span[@class="navigation_page"]/span/a/@title').extract_first()
        fields["brand"] = response.xpath('//div[@class="am_product_marque"]/a/span/text()').extract_first()
        fields["description"] = response.xpath('//div[@id="short_description_content"]//text()').extract_first()

        yield fields