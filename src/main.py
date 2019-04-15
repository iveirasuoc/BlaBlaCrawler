# -*- coding: utf-8 -*-
"""
Función principal del código. Puede ser ejecutada dando los parámetros en la llamada
o, en su defecto, se peidrán por pantalla.
"""

#Importamos los módulos que necesitamos
import blablaCrawler
import sys

#Definimos una función que devuelva los argumentos de la sentencia
def main():
    return sys.argv

    
print("Vamos a buscar viajes de Blablacar. \n")

#Si tenemos los parámetros en la llamada, los extraemos. Si no es así, los pedimos por pantalla
if __name__ == "__main__":
    try:
        parametros=main()
        parametros=[x.replace("Cualquiera","") for x in parametros]
        origen=parametros[1]
        destino=parametros[2]
        asientos=int(parametros[3])
        forigen=parametros[4]
        try:
            lim_paginas=int(parametros[5])+1
        except:
            lim_paginas=999
        de=parametros[6]
    except:
        #Establecemos los parámetros de búsqueda
        print("Vamos a definir los parámetros de búsqueda. Si no quires aplicar alguno pulsa intro \n")
        print("\n")
        origen=input("¿Desde dónde sales? \n")
        print("\n")
        destino=input("¿A donde te gustaría viajar? \n")
        print("\n")
        asientos=input("¿Cuántos asientos buscas? \n")
        try:
            asientos=int(asientos)
        except:
            asientos=""
        print("\n")
        forigen=input("¿Qué día nos vamos? (aaaa-mm-dd) \n")
        print("\n")
        lim_paginas=input("¿Quieres buscar en un número límite de páginas? \n")
        try:
            lim_paginas=int(lim_paginas)+1
        except:
            lim_paginas=999
        de=input("¿Cuál es la fecha límite del viajes? (aaaa-mm-dd) \n")
        
        
print(f"""Está bien, los parámetros de tu búsqueda son:
    Origen: {origen}
    Destino: {destino}
    Asientos: {asientos}
    Fecha origen: {forigen}  
    Límite de páginas: {lim_paginas-1}
    Fecha límite: {de}
    """)
print("Empezamos la búsqueda!")
print("\n")




blablaset = blablaCrawler.extr_blabla(asientos, forigen, origen, destino,lim_paginas,de)
nviajes=len(blablaset)

print(f"Extracción de datos realizada con éxito. Se han conseguido {nviajes} viajes. \n")

print("Exportando el csv...\n")

blablaset.to_csv('blablacar_extraccion_viajes.csv', index = False, sep = ';', encoding = 'utf-8-sig',decimal=",")

print("Proceso terminado satisfactoriamente. \n")
