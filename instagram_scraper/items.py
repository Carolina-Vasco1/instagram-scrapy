import scrapy

class InstagramScraperItem(scrapy.Item):
    username = scrapy.Field()
    full_name = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
    posts = scrapy.Field()
    bio = scrapy.Field()