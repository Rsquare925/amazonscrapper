# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import AmazonItem


class AtozSpider(CrawlSpider):
    name = 'atoz'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/s?k=Best+books&i=stripbooks&rh=n%3A17%2Cp_n_feature_twelve_browse-bin%3A10159408011&dc&qid=1585669767&rnid=5393827011&ref=sr_nr_p_n_feature_twelve_browse-bin_4/']

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(url="https://www.amazon.com/s?k=Best+books&i=stripbooks&rh=n%3A17%2Cp_n_feature_twelve_browse-bin%3A10159408011&dc&qid=1585669767&rnid=5393827011&ref=sr_nr_p_n_feature_twelve_browse-bin_4/", headers={
            'User-Agent': self.user_agent
        })
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='a-section a-spacing-none']/h2/a[@class='a-link-normal a-text-normal']"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_css=".a-last a"), process_request='set_user_agent')
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def get_price(self, selector):
        hardbook = selector.xpath(".//descendant::span[@class='a-color-secondary'][2]/text()").get()
        book = selector.xpath(".//descendant::span[@class='a-size-base a-color-secondary'][2]/text()").get()
        book1 = selector.xpath(".//descendant::span[@class='a-color-secondary'][3]/text()").get()
        book2 = selector.xpath(".//descendant::span[@class='a-size-base a-color-secondary']/text()").get()
        book3 = selector.xpath(".//descendant::span[@class='a-color-secondary']/text()").get()
        book4 = selector.xpath(".//descendant::span[@class='a-color-base']/text()").get()
        if hardbook is not None:
            return hardbook.replace("\n", "").strip(" ")
        elif book is not None:
            return book.replace("\n", "").strip(" ")
        elif book1 is not None:
            return book1.replace("\n", "")
        elif book2 is not None:
            return book2.replace("\n", "").strip(" ")
        elif book3 is not None:
            return book3.replace("\n", "").strip(" ")
        elif book4 is not None:
            return book4.replace("\n", "").strip(" ")

    def get_title(self, selector):
        title = selector.xpath(".//span[@id='productTitle']/text()").get()
        if title is not None:
            return title.replace("\n", "").strip(" ")
        else:
            return selector.xpath(".//span[@id='ebooksProductTitle']/text()").get().replace("\n", "").strip(" ")

    def get_author(self, selector):
        author = selector.xpath(".//descendant::a[@class='a-link-normal contributorNameID'][1]/text()").get()
        author1 = selector.xpath(".//descendant::a[@class='a-link-normal'][1]/text()").get()
        if author is not None:
            return author
        elif author1 is not None:
            return author1
        else:
            return "Fuck !!!"

    def get_image(self, selector):
        image = selector.xpath("descendant::img[@id='main-image']/@src").get()
        image1 = selector.xpath(".//descendant::img[@id='ebooksImgBlkFront']/@src").get()
        image2 = selector.xpath(".//descendant::img[@id='sitbLogoImg']/@src").get()
        image3 = selector.xpath(".//descendant::img[@id='imgBlkFront']/@src").get()
        if image is not None:
            return image
        elif image1 is not None:
            return image1
        elif image2 is not None:
            return image2.replace("\n", "")
        elif image3 is not None:
            return image3.replace("\n", "")
        else:
            return "Fuck !!!"



    def parse_item(self, response):
        items = AmazonItem()
        price_tag = response.xpath("//ul[@class='a-unordered-list a-nostyle a-button-list a-horizontal']")
        book_title = response.xpath("//h1[@id='title']")
        book_author = response.xpath("//div[@id='bylineInfo']")
        book_image = response.xpath("//div[@id='dp-container']")
        items['Book_Name'] = self.get_title(book_title)
        items['Book_Author'] = self.get_author(book_author)
        items['Book_Price'] = self.get_price(price_tag)
        items['Book_Image'] = self.get_image(book_image)

        yield items