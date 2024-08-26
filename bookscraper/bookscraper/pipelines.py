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
