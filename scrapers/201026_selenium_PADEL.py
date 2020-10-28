# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 14:44:37 2020
https://selenium-python.readthedocs.io/locating-elements.html
@author: Usuario
"""
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.keys import Keys  
#import re
from selenium import webdriver
import time
import csv

# GESTIONAMOS EL ARCHIVO:
csv_file = open('datos_padel2.csv', 'w')

csv_writer = csv.writer(csv_file)
    # La primera fila con el listado de valores a guardar por jugador:
csv_writer.writerow(['posicion', 'nombre','puntuación'])

# GESTIONAMOS EL WEBDRIVER:
    # Busco el lugar donde tengo mi .exe
path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)

    # Tomo el control de la web a través de SELENIUM
driver.get('https://www.worldpadeltour.com/jugadores?ranking=todos')

# NOS MOVEMOS AL FINAL DE LA PÁGINA:
driver.execute_script("window.scrollBy(0,9000)", "")
time.sleep(60)

# ENCONTRAMOS TODOS LOS JUGADORES:
jugadores = driver.find_elements_by_class_name('c-player-card__item')

# Para cada jugador sacamos la posición, el nombre y la puntuación:
for jugador in jugadores:
    posicion = jugador.find_element_by_class_name('c-player-card__position')
    nombre = jugador.find_element_by_class_name("c-player-card__name")
    score = jugador.find_element_by_class_name('c-player-card__score')
    
    #imprimo lo extraído:
    print(posicion.text,nombre.text,score.text)
    # grabamos la información en una fila del archivo
    csv_writer.writerow([posicion.text,nombre.text,score.text])

# cerramos el archivo    
csv_file.close()   


