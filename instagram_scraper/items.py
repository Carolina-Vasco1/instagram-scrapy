import scrapy

# Organizar tabla o modelo de datos de datos extraidos

class InstagramScraperItem(scrapy.Item):
    username = scrapy.Field()
    full_name = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
    posts = scrapy.Field()
    bio = scrapy.Field()