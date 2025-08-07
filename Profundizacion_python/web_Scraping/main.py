import bs4
import requests

result = requests.get('https://encode.edu.uy/')

print(type(result))

sopa = bs4.BeautifulSoup(result.text, 'lxml')

print(sopa.select('title'))
print(sopa.select('title')[0])
print(sopa.select('title')[0].getText())

print(sopa.select('p'))
parrafo_select = sopa.select('p')[1].getText()
print(parrafo_select)