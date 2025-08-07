import bs4
import requests
import os

#1. URL objetivo
url = 'https://www.fder.edu.uy/'

#2. Realizamos la peticion HTTP
result = requests.get(url, timeout=10)

#3. Creamos el objeto BeautifulSoup para analizar el HTML
sopa = bs4.BeautifulSoup(result.text, 'html.parser')

#4. Seleccionamos todas las etiquetas <img>
imagenes = sopa.select('img')

#5. Muestra cuantas imagenes se encontraron
print(f'Se encontraron {len(imagenes)}')

#6. Recorremos las imagenes y mostramos su URL
for i, img in enumerate(imagenes):
    src = img.get('src')
    print(f'{i+1}. {src}')

#7. Elegimos una imagen para descargar, por ejemplo la !
# Nota: algunas rutas pueden ser relativas, asi que las convertimos a absulutas
img_relative = imagenes[0].get('src')

# Si la URL de la imagen comienza con '/', es relativa
if img_relative.startswith('/'):
    img_url = url.rstrip('/') + img_relative
elif img_relative.startswith('http'):
    img_url = img_relative
else:
    img_url = url + '/' + img_relative

print(f'Descargando imagen desde: {img_url}')


#-#-#-#-#-#-#-#- GUARDAR IMAGENES #-#-#-#-#-#-#-#-#- 

#8. Relizamos la peticion a la URL de la imagen
respuesta_img = requests.get(img_url)

#9. Guardamos la imagen localmente
# Le damos un nombre, por ejemplo "primer-imagen.jpg"
with open('primer-imagen.jpg', 'wb') as archivo:
    archivo.write(respuesta_img.content)

print('Imagen guardada como primer-imagen.jpg')