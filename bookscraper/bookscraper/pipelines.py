# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip all whitespaces from strings besides description
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        # Category and product type to lowercase
        lowercase_keys = ['category', 'product_type']
        for key in lowercase_keys:
            value = adapter.get(key)
            adapter[key] = value.lower()
        
        price_keys = ['price_excl_tax', 'price_incl_tax', 'tax']
        for key in price_keys:
            value = adapter.get(key)
            value = value.replace('£', '')
            adapter[key] = float(value)

        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        rating_map = {
            "Zero": 0, 
            "One": 1, 
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
            }
        
        star_strings = adapter.get('stars')
        split_stars_array = star_strings.split(' ')
        stars_text_value = split_stars_array[1]
        stars = rating_map[stars_text_value]
        adapter['stars'] = stars

        return item

import mysql.connector

class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'password',
            database = 'books'
        )

        # Create cursor to execute commands

        self.cur = self.conn.cursor()

        # Create books table if none exists
        
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL AUTO_INCREMENT,
            url VARCHAR(255),
            title text,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):

        self.cur.execute("""
        INSERT INTO books (
            url,
            title,
            upc,
            product_type,
            price_excl_tax,
            price_incl_tax,
            tax,
            num_reviews,
            stars,
            category,
            description
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """, (
                item['url'],
                item['title'],
                item['upc'],
                item['product_type'],
                item['price_excl_tax'],
                item['price_incl_tax'],
                item['tax'],
                item['num_reviews'],
                item['stars'],
                item['category'],
                item['description']
            )
        )

        self.conn.commit()
        return item

    def close_spider(self, spider):
        
        # Scrapy automatically looks for this function
        # Close cursor and connection to database

        self.cur.close()
        self.conn.close()
