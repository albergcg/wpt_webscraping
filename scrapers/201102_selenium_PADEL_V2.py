# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 14:44:37 2020
https://selenium-python.readthedocs.io/locating-elements.html
@author: Usuario
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import csv

# CARGAMOS LA WEB:
path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get('https://www.worldpadeltour.com/jugadores?ranking=todos') 


# GESTIONAMOS LA CREACIÓN Y APRETURA DEL ARCHIVO:
csv_file = open('datos_padel_final.csv', 'w')

csv_writer = csv.writer(csv_file)
# La primera fila con el listado de valores a guardar por jugador:
csv_writer.writerow(['nombre','ranking','puntos','compañero','posicion de juego','partidos jugados','ganados','perdidos','efectividad','lugar_nac','fecha_nac','altura','residencia'])

# Hacemos click a la cookie que aparece para poder después presionar un botón que es necesario para pasar a la pestaña DATOS PERSONALES:
cookie= WebDriverWait(driver, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="ok-cookies"]'))).click()     

# NOS MOVEMOS A SALTOS EN LA WEB HASTA LLEGAR AL JUGADOR 100:
i= 0
for i in range(10):
    driver.execute_script("window.scrollBy(0,1000)", "")
    i=i+1
    time.sleep(2)
time.sleep(60)  

# Creamos las listas donde irán los links del ranking masculino y femenino:
links_m = []
links_f = []

# Obtenemos los primeros 5 links del ranking MASCULINO y los guardamos en la lista:
for i in range(1, 5):
    player = WebDriverWait(driver, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[4]/div/div[1]/ul/li['+str(i)+']/a')))
    link=player.get_attribute('href')
    links_m.append(link)
 
# Obtenemos los primeros 5 links del ranking FEMENINO y los guardamos en la lista:
for i in range(1, 5):
    player = WebDriverWait(driver, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[4]/div/div[2]/ul/li['+str(i)+']/a')))
    link=player.get_attribute('href')
    links_f.append(link)  

# BUCLE RANKING MASCULINO:
i=1
for link in links_m:
    driver.get(link)
    
    # La ubicación de la información para el jugador 1 es distintas que pare todo el resto
    if i == 1:    
        # Extraemos nombre, ranking y puntos
        nombre = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/div[1]/div/h1')))
        ranking = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/div[1]/div/div/div[1]/p[2]')))
        puntos = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/div[1]/div/div/div[2]/p[2]')))
        i=i+1
        
    # Ubicación de la información para los jugadores 2 a 100:
    else:
        # Extraemos nombre, ranking y puntos
        nombre = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/div[2]/div/h1')))
        ranking = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/div[2]/div/div/div[1]/p[2]')))
        puntos = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/div[2]/div/div/div[2]/p[2]')))
    
    # La ubicación de esta información es común para todos los jugadores. Obtenemos información de :
    # Compañero, posición de juego, partidos jugados, ganados, perdidos, efectividad:
    companero = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[1]/li[1]/p/a')))
    posicion = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[1]/li[2]/p')))
    jugados= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[2]/div/div/div[1]/p[2]')))
    ganados= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[2]/div/div/div[2]/p[2]')))
    perdidos= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[2]/div/div/div[3]/p[2]')))
    efectividad= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[2]/div/div/div[4]/p[2]'))) 
    print(nombre.text,ranking.text,puntos.text,companero.text,posicion.text,jugados.text,ganados.text,perdidos.text,efectividad.text)

# Presionamos el botón para entrar en la pestaña DATOS PERSONALES (no funciona si se extrae la información del href, hay que presionar la pestaña:
    WebDriverWait(driver, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/ul/li[2]/a'))).click()

    # Ubicación y extracción de información de:
    # Lugar de nacimiento, fecha nacimiento, altura, lugar residencia:
    lugar_nac= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[2]/li[1]/p')))
    fecha_nac= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[2]/li[2]/p')))
    altura= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[2]/li[3]/p')))
    residencia= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[2]/li[4]/p')))
    print(lugar_nac.text, fecha_nac.text, altura.text,residencia.text)
    
    # Guardamos en csv fila a fila:
    csv_writer.writerow([nombre.text,ranking.text,puntos.text,companero.text,posicion.text,jugados.text,ganados.text,perdidos.text,efectividad.text,lugar_nac.text,fecha_nac.text,altura.text,residencia.text])


# BUCLE RANKING FEMENINO:
i=1
for link in links_f:
    driver.get(link)
    
    # La ubicación de la información para el jugador 1 es distintas que pare todo el resto
    if i == 1:    
        # Extraemos nombre, ranking y puntos
        nombre = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/div[1]/div/h1')))
        ranking = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/div[1]/div/div/div[1]/p[2]')))
        puntos = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/div[1]/div/div/div[2]/p[2]')))
        
        i=i+1
    # Ubicación de la información para las jugadoras 2 a 100:
    else:
        # Extraemos nombre, ranking y puntos
        nombre = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/div[2]/div/h1')))
        ranking = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/div[2]/div/div/div[1]/p[2]')))
        puntos = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/div[2]/div/div/div[2]/p[2]')))

    # La ubicación de esta información es común para todos los jugadores. Obtenemos información de :
    # Compañero, posición de juego, partidos jugados, ganados, perdidos, efectividad:     
    companero = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[1]/li[1]/p/a')))
    posicion = WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[1]/li[2]/p')))
    jugados= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[2]/div/div/div[1]/p[2]')))
    ganados= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[2]/div/div/div[2]/p[2]')))
    perdidos= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[2]/div/div/div[3]/p[2]')))
    efectividad= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[2]/div/div/div[4]/p[2]')))
    
    print(nombre.text,ranking.text,puntos.text,companero.text,posicion.text,jugados.text,ganados.text,perdidos.text,efectividad.text)


# Presionamos el botón para entrar en la pestaña DATOS PERSONALES (no funciona si se extrae la información del href, hay que presionar la pestaña:
    WebDriverWait(driver, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[1]/ul/li[2]/a'))).click()

    lugar_nac= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[2]/li[1]/p')))
    fecha_nac= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[2]/li[2]/p')))
    altura= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[2]/li[3]/p')))
    residencia= WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="site-container"]/div[1]/div/div[2]/div[2]/ul[2]/li[4]/p')))
    print(lugar_nac.text, fecha_nac.text, altura.text,residencia.text)
  
    # Guardamos en csv fila a fila:
    csv_writer.writerow([nombre.text,ranking.text,puntos.text,companero.text,posicion.text,jugados.text,ganados.text,perdidos.text,efectividad.text,lugar_nac.text,fecha_nac.text,altura.text,residencia.text])

# cerramos el archivo    
csv_file.close()   














