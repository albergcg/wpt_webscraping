# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 14:44:37 2020
https://selenium-python.readthedocs.io/locating-elements.html
@author: Usuario
"""


from selenium.webdriver.common.keys import Keys  
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

# Busco el lugar donde tengo mi .exe
path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)

# Tomo el control de la web a través de SELENIUM
driver.get('https://www.worldpadeltour.com/jugadores?ranking=todos')

# Bajo con scroll hasta el final de la página y espero 60  segundos a que se cargue toda la info:
driver.execute_script("window.scrollBy(0,9000)", "")
time.sleep(60)

# Hago un list comprehensive para obtener el item asociado a la posición de cada jugador/a:
texts = [el.text for el in driver.find_elements_by_class_name("c-player-card__position")]

# Imprimo la lista
print(texts)
