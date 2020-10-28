# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 19:22:42 2020

@author: AFP
"""
# Importar las librerías necesarias (recordar hacer un requirements.txt)
import requests 
from bs4 import BeautifulSoup
import re
import csv

# Elegir la página a la que hacer scraping
url = 'https://www.worldpadeltour.com/jugadores?ranking=todos'

# En este caso debemos cambiar el header de la petición para que no bloquee:
headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
*/*;q=0.8",
"Accept-Encoding": "gzip, deflate, sdch, br",
"Accept-Language": "en-US,en;q=0.8",
"Cache-Control": "no-cache",
"dnt": "1",
"Pragma": "no-cache",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5\
37.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}

# Se hace el requrimiento a la página web
page = requests.get(url, headers = headers)

# Se parsea el contenido y ya tenemos el objeto soup:
soup = BeautifulSoup(page.content)

# Gestionamos el archivo donde vamos a guardar la información:
csv_file = open('datos_padel.csv', 'w')

csv_writer = csv.writer(csv_file)
# La primera fila con el listado de valores a guardar por jugador:
csv_writer.writerow(['nombre', 'apellido1','link','compañero/a','posiciòn juego','puesto','puntos'])

# BUCLE PARA EXTRAER LA INFORMACIÓN DE CADA JUGADOR MOSTRADO:
for jugador in soup.find_all('li', class_='c-player-card__item'):
    
    # De aquí saco 2 atributos de cada jugador/a:
    nombre=jugador.find('div',class_='c-player-card__name').text
    link=jugador.find('a', class_='c-trigger')['href']
  
    # Separo el nombre en una lista de Nombre y Apellidos:
    nombre_completo = []
    nombre_completo = re.findall('[A-Z][^A-Z]*', nombre)
    
    # ENTRO EN EL LINK DE CADA JUGADOR:
    page_jugador = requests.get(link, headers = headers)
    soup_jugador = BeautifulSoup(page_jugador.content)
      
    # Se extrae una lista con la información siguiente:
        # nombre compañero/a, posicion de juego, lugar nacimiento, fecha nacimiento, altura, residencia:     
    lista_datos_personales = []
    for x in soup_jugador.find_all('li', class_='c-player__data-item'):
        y = x.find('p').text
        lista_datos_personales.append(y)
        
        # posicion, puntos, partidos jugados, partidos ganados, partidos perdidos, efectividad, victorias consecutivas
    lista_datos_partidos = []
    for x in soup_jugador.find_all('div', class_='c-ranking-header__data-box'):
        y = x.find('p',class_='c-ranking-header__data').text
        lista_datos_partidos.append(y)
    
    # Si queremos ver en pantalla, imprimimos esto:
    print(nombre_completo,link,lista_datos_personales, lista_datos_partidos)
    
    # algunos datos pasados al fichero creado:
    #csv_writer.writerow([nombre_completo[0], nombre_completo[1],link,lista_datos_personales[0],lista_datos_personales[1],lista_datos_partidos[0],lista_datos_partidos[1]])
csv_file.close()




  