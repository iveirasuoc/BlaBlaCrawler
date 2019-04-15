# -*- coding: utf-8 -*-
"""
Creación de funciones necesarias para la ejecución de un Crawler en la página de BlablaCar.

    -consultar_viajes: consigue un pandas DataFrame a partir de los datos aportados (soup).
    
    -extr_blabla: se encarga de realizar las llamadas a la página web de BlablaCar
     con los parámetros que le hayamos asignado. Además llama a consultar_viajes para crear
     el dataframe.
"""

#Importamos las librerías necesarias
import requests
from bs4 import BeautifulSoup 
import urllib
import pandas as pd
import numpy as np
import time


# Definimos las clases y url que buscaremos en el html de BlaBlaCar
class_trip = 'jsx-1522777265 kirk-tripCard mb-m'
class_name =  'kirk-text kirk-text-title'
class_dep = 'jsx-1448366035 kirk-itinerary-location kirk-itinerary--departure'
class_arr = 'jsx-1448366035 kirk-itinerary-location kirk-itinerary--arrival'
class_price = 'kirk-text kirk-text-titleStrong kirk-tripCard-price'
class_flags = 'jsx-1522777265 kirk-tripCard-flags'
url_f = 'https://cdn.blablacar.com/comuto3/images/avatar/pixar/passenger-f.svg'
url_m = 'https://cdn.blablacar.com/comuto3/images/avatar/pixar/passenger-m.svg'


# Función que extrae información de viajes de "soup" y la almacena en "datos"
def consultar_viajes(soup, datos):
    # Buscamos todos los viajes de la página e iteramos por ellos
    viajes = soup.find_all('li',{'class': class_trip})
    for iter in range(len(viajes)):
        # Inicializamos la lista de variables a extraer
        d_via = [0] * 14
        # Nombre del viaje
        d_via[0] = viajes[iter].find('a', {
                'class': '', 'rel': 'nofollow'}).attrs['href']
        # Url del viaje
        d_via[1] = viajes[iter].find('meta', {
                'class': 'jsx-1522777265', 'itemprop': 'url'}).attrs['content']
        # Nombre del conductor
        d_via[2] = viajes[iter].find('span', {'class': class_name}).contents[0]
        # Localidad de origen del viaje
        d_via[3] = viajes[iter].find('li',{'class': class_dep}).find(
                'meta', {'class': 'jsx-1448366035', 'itemprop': 'name'}).attrs[
                'content']
        # Fecha de salida del viaje
        d_via[4] = pd.to_datetime(viajes[iter].find(
                'meta', {'class': 'jsx-1522777265', 'itemprop':
                    'startDate'}).attrs['content'])
        # Localidad de destino del viaje
        d_via[5] = viajes[iter].find('li', {'class': class_arr}).find(
                'meta', {'class': 'jsx-1448366035', 'itemprop': 
                    'name'}).attrs['content']
        # La fecha de llegada del viaje
        d_via[6] = pd.to_datetime(viajes[iter].find(
                'meta', {'class': 'jsx-1522777265', 'itemprop': 
                    'endDate'}).attrs['content'])
        # Duración del viaje
        d_via[7] = round((d_via[6] - d_via[4])/np.timedelta64(1, 'h'), 2)
        # Precio del vije
        d_via[8] = float(viajes[iter].find('span', {
                'class':class_price }).contents[0][:-2].replace(",","."))
        # Distancia a la localidad origen definida
        d_via[9] = viajes[iter].find('li', {'class': class_dep}).find(
                'svg', {'class': 'kirk-icon', 'aria-hidden': 
                    'false'}).title.contents[0]
        # Distancia a la localidad destino definida (en caso de estar definida)
        try:
            d_via[10] = viajes[iter].find('li', {'class': class_arr}).find(
                    'svg', {'class': 'kirk-icon', 'aria-hidden': 
                        'false'}).title.contents[0]
        except:
            d_via[10] = np.nan
        # Autoaceptación
        try:
            viajes[iter].find('div', {'class': class_flags}).find('path', {
                    'fill': 'none'}).attrs['stroke-width']
            d_via[11] = True
        except:
            d_via[11] = False
        # Dos asientos detrás
        try: 
            viajes[iter].find('div', {'class': class_flags}).find('g', {
                    'fill': 'none'}).attrs['stroke-width']
            d_via[12] = True
        except:
            d_via[12] = False
        # Conductor con foto
        if viajes[iter].find('img', {'class': 'jsx-3474581579', 
                 'src': url_f}) != None:
            d_via[13] = False
        elif viajes[iter].find('img', {'class': 'jsx-3474581579', 
                   'src': url_m}) != None:
            d_via[13] = False
        else:
            d_via[13] = True
        # Concatenamos la información del viaje en "datos"
        datos = pd.concat([datos, pd.DataFrame(d_via).T], ignore_index = True)
    return datos


# Función que descarga las páginas de BlaBlaCar y extrae información relevante
def extr_blabla(seats = 1, dep_date = '2019-04-15', dep = 'Madrid', arr = '',lim_paginas=100, de='2019-04-17'):
    # Inicializamos el set de datos
    blablaset = pd.DataFrame()
    # Inicializamos la página de búsqueda a 1 y el límite de páginas a 100
    pag = 1
    # Definimos el header de la consulta y la raíz de la url
    header = {'User-Agent': 
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) ' + 
        'Gecko/20100101 Firefox/66.0',
        'Accept-Language': 'gl-GL,gl;q=0.8,en-US;q=0.5,en;q=0.3'}
    url_blablacar = 'https://www.blablacar.es/search?'
    # Iteramos por las páginas de búsqueda
    while pag < lim_paginas:
        # Definimos las características de la petición url y la construimos
        url_pet = {'seats': seats, 'db': dep_date, 'departure_city': dep, 
                   'arrival_city': arr, 'page': str(pag), 'de': de}
        url_total = url_blablacar + urllib.parse.urlencode(
                url_pet, quote_via = urllib.parse.quote)
        # Realizamos la petición url y la convertimos con BeautifulSoup
        r = requests.get(url_total, headers = header)
        soup = BeautifulSoup(r.content, features = 'lxml')
        # Comprobamos si ya no hay viajes en la página para detener el bucle
        pag_error = soup.find('h1', {'class':'kirk-title py-xl w-full'})
        if pag_error != None:
            break
        else:
            # Mostramos por pantalla la página extraída y la extraemos
            print(u'Extrayendo página ' + str(pag) + ':')
            print(url_total)
            print('\n')
            blablaset = consultar_viajes(soup, blablaset)
            # Esperamos 1s para evitar que nos bloqueen y cambiamos de página
            time.sleep(1)
            pag += 1

    # Si hemos extraído algún viaje, formateamos el nombre de las variables y el tipo de las numéricas
    if pag > 1:
        blablaset.columns = ['nombre', 'url', 'nombre_conductor', 'origen', 
                             'fecha_salida', 'destino', 'fecha_llegada',
                             'duracion', 'precio', 'distancia_origen', 
                             'distancia_destino', 'auto_aceptacion',
                             'dos_asientos_detras', 'conductor_con_foto']
        blablaset.precio=blablaset.precio.astype(float)
        blablaset.duracion=blablaset.duracion.astype(float)
    return blablaset