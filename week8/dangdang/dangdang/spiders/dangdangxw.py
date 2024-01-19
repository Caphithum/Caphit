import scrapy
from urllib.parse import urljoin
from scrapy.http import Request


class DangdangxwSpider(scrapy.Spider):
    name = "dangdangxw"
    allowed_domains = ["dangdang.com"]
    start_urls = ["http://search.dangdang.com/?key=%BC%C6%CB%E3%BB%FA%C0%E0%CA%E9%BC%AE&act=input"]

    def parse(self, response):
        for i in range(1,61):
            lab = "line"+str(i)
            lab1 = "li."+lab
            for eachbook in response.css(lab1):
                title = eachbook.xpath('./a/@title').extract_first()
                author = eachbook.xpath('./p[@class="search_book_author"]/span/a/@title').extract_first()
                price = eachbook.xpath('./p[@class= "price"]/span[@class="search_now_price"]/text()').extract_first()
                yield{
                    "title":title,
                    "author":author,
                    "price":price,
                }

        next_url = response.css('div.paging li.next a::attr(href)').extract_first()
        print(next_url)
        if next_url:
            url = response.urljoin(next_url)
            yield Request(url,callback=self.parse)

