import requests
from bs4 import BeautifulSoup

# URL base
base_url = 'https://books.toscrape.com/catalogue/'

# Página inicial
url = base_url + 'page-1.html'

# Mientras haya una siguiente página
while True:
    print(f'Procesando: {url}')

    # Obtener el contenido HTML
    res = requests.get(url)
    sopa = BeautifulSoup(res.text, 'html.parser')

    # Extraer títulos de libros
    libros = sopa.select('article.product_pod h3 a')

    for libro in libros:
        titulo = libro['title']
        print(f'- {titulo}')

    # Buscar el botón de "next"
    next_btn = sopa.select_one('li.next a')

    if next_btn:
        # Armar la URL de la siguiente página
        next_url = next_btn['href']
        url = base_url + next_url
    else:
        print('Fin de la paginación.')
        break