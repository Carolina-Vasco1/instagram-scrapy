import scrapy
import re
from instagram_scraper.items import InstagramScraperItem

class IgSpiderSpider(scrapy.Spider):
    name = "ig_spider"
    allowed_domains = ["instagram.com"]
    
    # Aquí puedes agregar todas las URLs que necesites extraer
    start_urls = [
        "https://www.instagram.com/davidmastermg/",
        "https://www.instagram.com/psykhe_memes_uce/",
        "https://www.instagram.com/willy_ec_/"
    ]

    def parse(self, response):
        item = InstagramScraperItem()

        # Extraer descripción de los Meta Tags (contiene seguidores, seguidos y posts)
        description = response.xpath('//meta[@name="description"]/@content').get()
        
        if description:
            # Buscamos números o letras de magnitud (K, M) antes de las palabras clave
            stats = re.findall(r"([\d\.\,KkMm]+)", description)
            item['followers'] = stats[0] if len(stats) > 0 else "0"
            item['following'] = stats[1] if len(stats) > 1 else "0"
            item['posts'] = stats[2] if len(stats) > 2 else "0"
        else:
            item['followers'] = item['following'] = item['posts'] = "N/A"

        # Nombre de usuario desde la URL
        item['username'] = response.url.split('/')[-2]

        # Nombre completo desde el tag og:title
        title_content = response.xpath('//meta[@property="og:title"]/@content').get()
        if title_content:
            # Limpiamos el texto para obtener solo el nombre antes del "(@username)"
            item['full_name'] = title_content.split('(@')[0].strip()
        else:
            item['full_name'] = item['username']

        # Biografía desde og:description
        bio_content = response.xpath('//meta[@property="og:description"]/@content').get()
        item['bio'] = bio_content if bio_content else "Sin biografía"

        yield item