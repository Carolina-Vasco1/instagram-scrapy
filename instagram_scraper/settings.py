BOT_NAME = 'instagram_scraper'

SPIDER_MODULES = ['instagram_scraper.spiders']
NEWSPIDER_MODULE = 'instagram_scraper.spiders'

# No obedecer robots.txt para poder acceder a los perfiles
ROBOTSTXT_OBEY = False

# Requerimiento: Delay de 2 segundos para evitar bloqueos
DOWNLOAD_DELAY = 2

# Configuración de salida automática a CSV
FEEDS = {
    'instagram_data.csv': {
        'format': 'csv',
        'encoding': 'utf8',
        'store_empty': False,
        'fields': ['username', 'full_name', 'followers', 'following', 'posts', 'bio'],
    },
}

# Middleware para rotar User-Agents (evita que Instagram detecte el bot)
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_useragents.middlewares.UserAgentMiddleware': 400,
}