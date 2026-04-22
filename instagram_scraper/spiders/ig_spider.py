import scrapy
import re

class IgSpiderSpider(scrapy.Spider):
    name = "ig_spider"
    allowed_domains = ["instagram.com"] #solo a un dominio, no a otros

    # --- CONFIGURACIÓN DE COOKIES ---
    #usuario logueado
    # Reemplaza los valores con los que obtengas de tu navegador, aquí se guardan las cookies del navegador
    cookies = {
        'sessionid': '4003120443%3ArEXdN2A8hzthxG%3A11%3AAYiNlVAPhOxIuFq7cFj04Nn1zok5T7S5SrUWo-LXIg',
        'ds_user_id': '4003120443',
        'csrftoken': 'AYQ4XiCUBykFSaEBFgfnfOBs3A6yIhuP',
    }

    def start_requests(self): 
        # El programa se detendrá aquí y esperará a que escribas en la consola
        print("\n" + "="*30)
        entrada = input("AGREGAR USUARIO (separa por comas si son varios): ")
        print("="*30 + "\n")

        # Convertimos la entrada en una lista
        lista_usuarios = [u.strip() for u in entrada.split(',') if u.strip()]

        if not lista_usuarios: #sino ingresa nada, se detiene el programa
            self.logger.error("No ingresaste ningún usuario válido.")
            return

        for usuario in lista_usuarios: #recorre cada ususrio ingresado
            url = f"https://www.instagram.com/{usuario}/"
            # Enviamos la petición con tus cookies
            yield scrapy.Request(url=url, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        # 1. Extraer el nombre de usuario de la URL
        username = response.url.split('/')[-2] #penúltimo elemento

        # 2. Extraer estadísticas desde los Meta Tags (seguidores, seguidos, posts)
        # Instagram pone esto en <meta name="description" content="...">
        description = response.xpath('//meta[@name="description"]/@content').get()
        
        followers = "0"
        following = "0"
        posts = "0"

        if description:
            # Usamos regex para encontrar números o abreviaturas como 1.5K, 2M, etc.
            stats = re.findall(r"(\d[\d,\.]*\s?[KkMm]?)", description)
            if len(stats) >= 3:
                followers = stats[0]
                following = stats[1]
                posts = stats[2]

        # 3. Extraer Nombre Completo
        full_name_raw = response.xpath('//meta[@property="og:title"]/@content').get()
        full_name = full_name_raw.split('(@')[0].strip() if full_name_raw else username # quita el @del usuario 

        # 4. Extraer Biografía
        bio = response.xpath('//meta[@property="og:description"]/@content').get()

        # Retornamos los datos para que Scrapy los guarde en el CSV
        yield {
            'username': username,
            'full_name': full_name,
            'followers': followers,
            'following': following,
            'posts': posts,
            'bio': bio if bio else "Sin biografía"
        }