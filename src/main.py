# -*- coding: utf-8 -*-
"""
Función principal del código
"""

# Cargamos el módulo con las funciones para extraer información de BlaBlaCar
import blablaCrawler

# Extraemos la información que cumplan las características definidas
blablaset = blablaCrawler.extr_blabla(1, '2019-04-17', 'Madrid', 'Jumilla')

# Exportamos los resultados obtenidos a CSV
blablaset.to_csv('extraccion_BlaBlaCar.csv', index = False, sep = ';', 
                 encoding = 'utf-8-sig')