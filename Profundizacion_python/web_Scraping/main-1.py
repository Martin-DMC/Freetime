import bs4
import requests

result = requests.get('https://www.fder.edu.uy/', timeout=10)

sopa = bs4.BeautifulSoup(result.text, 'html.parser')

"""
        CARACTERES UTILES PARA EXTRAER DATOS

CARACTER: "
UTILIDAD: Sirve para extraer todos los elementos con una cierta etiqueta
EJEMPLO: sopa.select('div')
RESULTADO: todos los resultados con la etiqueta 'div'

CARACTER: #
UTILIDAD: sirve para extraer un cierto id
EJEMPLO: sopa.select('#estilo_4')
RESULTADO: todos los elementos que tengan el id='estilo_4'

CARACTER: .
UTILIDAD: sirve para extraer elementos de una cierta clase
EJEMPLO: sopa.select('.columna_der')
RESULTADO: todos los elementos que tengan la class='columna_der'

CARACTER: (espacio)
UTILIDAD: sirve para extraer un cierto elemento dentro de otro
EJEMPLO: sopa.select('div span')
RESULTADO: cualquier elemento llamado 'span' dentro de un elemento 'div'

CARACTER: >
UTILIDAD: sirve para extraer todos los elementos con un cierto tipo que estan dentro de otro, sin nada en medio
EJEMPLO: sopa.select('div>span')
RESULTADO: cualquier elemento llamado 'span' que esta directamente dentro de un elemento 'div', sin nada en medio

"""

noticias_grid = sopa.find_all('div', class_='views-view-responsive-grid__item')

for item in noticias_grid:
    titulo = item.find('h2', class_='node__title').text.strip() if item.find('h2', class_='node__title') else 'Sin titulo'
    fecha = item.find('div', class_="node__meta").text.strip() if item.find('div', class_='node__meta') else 'Sin fecha'
    enlace = item.find('a')
    enlace_web = 'https://www.fder.edu.uy/' + enlace['href'] if enlace else 'Sin enlace'

    print(f'Tiulo: {titulo}')
    print(f'Fecha: {fecha}')
    print(f'Enlace: {enlace_web}')
    print('-' * 40)