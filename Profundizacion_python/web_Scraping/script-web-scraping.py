import requests
from bs4 import BeautifulSoup

url_base = 'https://books.toscrape.com/catalogue/'
dominio = 'https://books.toscrape.com'

url = url_base + 'page-1.html'

with open('libros.csv', 'w') as archivo:
    archivo.write('Titulo,Precio\n')

    while True:
        print(f'Procesando: {url}')

        res = requests.get(url, timeout=10)
        sopa = BeautifulSoup(res.text, 'html.parser')

        libros = sopa.select('article.product_pod h3 a')
        precios = sopa.select('div.product_price p.price_color')

        for libro, precio in zip(libros, precios):
            titulo = libro['title']
            price = precio.text.strip()
            
            linea = f'"{titulo}", {price}\n'
            archivo.write(linea)
        
        list_img = sopa.select('div.image_container a img')
        img = list_img[0]
        ruta_img = img.get('src')

        if ruta_img.startswith('/'):
            url_absoluta = dominio + ruta_img
        elif ruta_img.startswith('http') or ruta_img.startswith('https'):
            url_absoluta = ruta_img
        else:
            url_absoluta = dominio + '/' + ruta_img

        response = requests.get(url_absoluta)
        name_img = libros[0].get('title')
        for letra in name_img:
            if not letra.isalnum():
                name_img = name_img.replace(letra, '_')

        with open(f'imagenes_destacadas/{name_img}.jpg', 'wb') as archivo_img:
            archivo_img.write(response.content)

        next_btn = sopa.select_one('li.next a')

        if next_btn:
            next_url = next_btn['href']
            url = url_base + next_url
        else:
            print('Fin de la paginación.')
            break