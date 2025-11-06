from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# import urllib3 # urllib3 es un cliente HTTP potente y fácil de usar para Python.
import re # Expresiones regulares 
import time
import pandas as pd

#  Configuración del driver 
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
time.sleep(2)

#url
driver.get("https://www.imdb.com/chart/top/")
time.sleep(2)
"""
buscar con find_element o find_elements
by Xpath
encontrar la seccion (section, ul, li, head....)
con contain () buscar por clase que
resumen: buscar la path que contenga la clase que sea y de ahi elegir. Hay casos que hay 2 y hay que elegir por posicion
"""
#Localizar el UL principal de las películas
ul = driver.find_element(By.XPATH, '//section//ul[contains(@class, "ipc-metadata-list")]')

#Dentro de ese UL, obtener todos los LI (cada película)
peliculas = ul.find_elements(By.XPATH, './li[contains(@class, "ipc-metadata-list-summary-item")]')

data = [] #dict vacio

for pelicula in peliculas:
    try:
        titulo_completo = pelicula.find_element(By.XPATH, './/h3[contains(@class,"ipc-title__text")]').text
        posicion,titulo = titulo_completo.split(".")  
        print(posicion)

        #Año y duración. Van juntos en la misma clase en la posicion 0 el año y en la 1 la duracion
        anio_duracion = pelicula.find_elements(By.XPATH, './/span[contains(@class, "cli-title-metadata-item")]')
        anio = anio_duracion[0].text if len(anio_duracion) > 0 else ""
        duracion = anio_duracion[1].text if len(anio_duracion) > 1 else ""

        #Rating
        rating = pelicula.find_element(By.XPATH, './/span[contains(@class, "ipc-rating-star--rating")]').text
        #rellenar dict
        data.append({
            "Posición": posicion,
            "Título": titulo,
            "Año": anio,
            "Duración": duracion,
            "Rating": rating
        })
    except Exception as e:
        print("Error en un elemento:", e)

driver.quit()

df = pd.DataFrame(data)
print(df.head())
df.to_csv("prueba.csv")
