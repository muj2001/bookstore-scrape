import scrapy
from bookscraper.items import BookItem
import random


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    custom_settings = {
        'FEEDS': {
            'booksdata.csv': {
                    'format': 'csv',
                    'overwrite': True
                }
        }
    }

    user_agent_list = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36']

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            book_page = book.css('h3 a ::attr(href)').get()
            if book_page is not None:
                if 'catalogue/' in book_page:
                    book_page_url = 'https://books.toscrape.com/' + book_page
                else:
                    book_page_url = 'https://books.toscrape.com/catalogue/' + book_page
                    
                yield response.follow(book_page_url, callback=self.parse_book_page)


        next_page = response.css('li.next a ::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
                
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):

        book_item = BookItem()

        
        table_rows = response.css("table tr")

        # yield {
        #     'upc': table_rows[0].css('td ::text').get(),
        #     'name': response.css('.product_main h1::text').get(),
        #     'category': response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get(),
        #     'product-type': table_rows[1].css('td ::text').get(),
        #     'price-excl-tax': table_rows[2].css('td ::text').get(),
        #     'price-incl-tax': table_rows[3].css('td ::text').get(),
        #     'tax': table_rows[4].css('td ::text').get(),
        #     'no of reviews': table_rows[6].css('td ::text').get(),
        #     'stars': rating_map[response.css('p.star-rating ::attr(class)').get().replace('star-rating ', '')],
        #     'description': response.xpath('//*[@id="content_inner"]/article/p/text()').get()
        # }

        book_item['url'] = response.url
        book_item['title'] = response.css('.product_main h1::text').get()
        book_item['product_type'] = table_rows[1].css('td ::text').get()
        book_item['price_excl_tax'] = table_rows[2].css('td ::text').get()
        book_item['price_incl_tax'] = table_rows[3].css('td ::text').get()
        book_item['tax'] = table_rows[4].css('td ::text').get()
        book_item['num_reviews'] = table_rows[6].css('td ::text').get()
        # book_item['stars'] = rating_map[response.css('p.star-rating ::attr(class)').get().replace('star-rating ', '')]
        book_item['stars'] = response.css('p.star-rating ::attr(class)').get()
        book_item['category'] = response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get()
        book_item['description'] = response.xpath('//*[@id="content_inner"]/article/p/text()').get()
        book_item['upc'] = table_rows[0].css('td ::text').get()

        yield book_item