# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

def serialize_price(value):
    return f'$ {str(value)}' # originally it was pound sign, but I can't find that on my keyboard, and since this is just for learning purposes, I have changed it to $

class BookItem(scrapy.Item):
    # yield {
    #         'upc': table_rows[0].css('td ::text').get(),
    #         'name': response.css('.product_main h1::text').get(),
    #         'category': response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get(),
    #         'product-type': table_rows[1].css('td ::text').get(),
    #         'price-excl-tax': table_rows[2].css('td ::text').get(),
    #         'price-incl-tax': table_rows[3].css('td ::text').get(),
    #         'tax': table_rows[4].css('td ::text').get(),
    #         'no of reviews': table_rows[6].css('td ::text').get(),
    #         'stars': rating_map[response.css('p.star-rating ::attr(class)').get().replace('star-rating ', '')],
    #         'description': response.xpath('//*[@id="content_inner"]/article/p/text()').get()
    #     }
    url = scrapy.Field()
    title = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()

    # A better way to do this is through pipelines, they allow us to process data, but if you did not want to use pipelines and are scraping little data without much post-processing this works too

    # price_excl_tax = scrapy.Field(serializer=serialize_price)
    # price_incl_tax = scrapy.Field(serializer=serialize_price)
    
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
