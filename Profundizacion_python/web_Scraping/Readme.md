principios basicos:

esto trata del web scraping y la manipulación de datos web, y las herramientas (librerias de python) que vamos a utilizar son:

-#-#- beautifulsoup4 -#-#-:
    es una librería de Python diseñada para analizar (parsear) documentos HTML y XML. Su principal ventaja es que es muy tolerante con el código HTML malformado. A diferencia de otros parsers más estrictos, BeautifulSoup puede interpretar etiquetas que no están cerradas o anidadas incorrectamente, lo que la hace ideal para "raspar" (scrapear) sitios web del mundo real.

-#-#- lxml -#-#-: 
    es una de las librerías más rápidas y poderosas para analizar HTML y XML en Python. Aunque se puede usar por sí sola, a menudo se integra con BeautifulSoup como el motor de análisis (parser) predeterminado debido a su velocidad y robustez.

             -#-#-#-#- Resumen y cómo se integran -#-#-#-#-

En la práctica, lo más común es usar BeautifulSoup con LXML como su parser.

    requests: Tu punto de partida para hacer la petición HTTP y obtener el contenido de la página.

    BeautifulSoup: La interfaz amigable y tolerante que te permite navegar y buscar elementos de manera sencilla.

    lxml: El motor ultrarrápido y potente que hace el trabajo pesado de analizar el documento.

-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
visualizar codigo fuente:
    hablo sobre la consola del navegador.
    los cambios que hagamos dentro de la consola se ven reflejados en nuestra instancia local nada mas.

    en el main solo importamos las librerias.

-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
extraer titulo pagina:
    primero hicimos un request para ver todo el codigo fuente, luego nos mostro todo el codigo fuente pero usando beautifulsoup codificando con lxml para notar la diferencia (es minima pero bue).
    despues hablo de select(), usando . con la variable sopa para poder seleccionar etiquetas dentro del contenido de la request, usando prints vimos como la funcion nos devuelve un array de cohincidencias a las cuales podemos seleccionar como si fuece una lista comun de python, usando []. tambien nos mostro el .getText(), que es lo que nos muestra la cohincidencia pero sin etiquetas ni corchetes, solo el texto que contiene.

    sopa.select('p')
    element = sopa.select('p')[1].getText()

-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
extraer elementos de clases:
    para este video use el archivo main_1.py
    importamos las librerias bs4 y request y declaramos la variable sopa para poder trabajar con el contenido de la request, pero en este caso usamos el segundo parametro 'html.parse' (es para tener una manera mas sensilla/ordenada de buscar en el contenido).

    la idea era hacer una aplicacion que tenga la funcion de extraer sierta data especifica de una pagina web mediante a busquedas que nosotros hacemos, para eso utilizamos 'find' que sirve para buscar, tambien usamos 'strip' para que se extraiga solo el texto que queremos sin espacios innecesarios, todos los datos estan en el main_1.

-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
extraer imagenes:
    Importamos las librerias y sumamos la libreria 'os'.
    Definimos la url objetivo en una variable, para luego hacer la request.get con esa variable.
    Organizamos la informacion que retorna el request con el objeto beautifulsoup y 'html.parser' y lo guardamos en una variable.
    Creamos otra variabre para usar 'select' con el objeto 'sopa' y guardar todas las imagenes de la request en esta variable.
    Ahora que tenemos un array de las imagenes que obtuvimos de la pagina procedemos a usar 'len' dentro de un print para mostrar la cantidad de imagenes.
    Aprovechamos el array para hacer un 'for' para recorrerlo y obtener el atributo 'src' de cada etiqueta < img> que esta en la request que hicimos y asi saber su URL, usamos enumerate y le sumamos uno a la i para que arranque de 1, y luego solo mostramos el resultado del 'img.get()' capturado en una variable.
    Por ultimo seleccionamos una imagen para hablar de las rutas relativas y absolutas, creamos unos condicionales para filtrar la url y convertirla en absoluta sea como sea que se encontrara la informacion del 'src'
    Todo lo de este video esta em main-2

-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
guardar imagenes:
    Es un continuado del video pasado, voy a trabajar con main-2.py.
    Luego de convertir la URL de la imagen que deseamos descargar en absoluta, nuestro proximo paso es hacer la peticion a esa URL que obtuvimos.
    Definimos una variable para guardar el contenido de request.get() con dicha URL.
    Usamos with con open, ponemos el nombre deseado y lo abrimos con 'wb', luego escribimos el archivo usando la respuesta que obtuvimos del request y le agregamos .content para escribir el contenido.
    Por ultimo hacemos un print para mostrarle al usuario que se descargo.
    Aprendimos como (a partir del codigo) identificamos imagenes, trabajar con ellas, extraer el source (src) y convertirlo en rutas absolutas para luego hacer un request a esa ruta y poder descargar la imagen.

-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
multiples paginas:
    Importamos las librerias que nesecitamos, ahora usamos la URL 'https://books.toscrape.com/catalogue/', es una pagina que nos permite practicar web scraping.
    La consigna es hacer una aplicacion que extraiga todos los nombres de los libros que contiene esta pagina, la dificultad es hacer que nuestra aplicacion maneje el boton next para ver los siguientes resultados y asi capturar los nombres de todos los libros.
    Declaramos la 'base_url' u luego hacemos la url que vamos a utilizar concatenando la vace mas 'page-1.html'.
    Declaramos un while (para recorrer todas las paginas), ponemos un print para mostrar la url que estamos procesando.
    Obtenemos el contenido HTML, haciendo lo de siempre (request y luego creamos el objeto beautifulsoup con html.parser).
    Declaranmos una variable para contener el array del titulo de los libros de esa pagina y usamos el objeto 'sopa' para seleccionar 'articles.product_pod h3 a' (captura la etiqueta < a> de un h3 que esta dentro de articles con clase product_pod).
    Luego ejecutamos un 'for' en ese array para obtener el titulo de cada libro en una variable y poder imprimirla por pantalla.
    Despues abordamos la parte del boton next de cada pagina.
    Declaramos su variable y usamos el objeto 'sopa' con .select.one() y le pasamos la referencia para encontrarlo 'li.next a' (capturamos los a que estan dentro de un li con la clase next).
    Por ultimo metemos los condicionales si existe el boton(variable anterior), armamos la URL de la siguiente pagina, capturando el 'href' de dicho boton y concatenandolo a la url base que ya habiamos declarado, si no existe ese boton ponemos un print para avisar el final de las paginas y hacer el break para terminar el while.

-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

