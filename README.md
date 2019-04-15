# Práctica 1: Web Scraping - BlaBlaCrawler

## Descripción
Crawler que extrae información de viajes de la página web de [BlaBlaCar](https://blablacar.es) y lo exporta en formato _CSV_. 

Este trabajo se ha realizado bajo el contexto del máster de Ciencia de Datos de la UOC. En concreto, responde al enunciado de la Práctica 1 de la asignatura de _Tipología y Ciclo de Vida de los Datos_.

## Miembros del equipo
Esta práctica ha sido realizada por los alumnos **Daniel Mato Regueira** e **Iago Veiras Lens**.

## Ficheros del repositorio

- **csv/blablacar_extraccion_viajes.csv**: fichero _CSV_ con la información extraída de los viajes de la web de BlaBlaCar.
- **pdf/Practica_1_Respuestas.doc**-**pdf**: documento _doc_-_pdf_ con las respuestas a lsa preguntas del enunciado de la práctica.
- **src/blablaCrawler.py**: fichero que contiene las funciones ´consultar_viajes´ y ´extr_blabla´, necesarias para poder realizar la extracción de la información.
- **src/main.py**: fichero principal del código en el que se invocan las funciones de extracción de la información sobre los viajes.

## Ejecución
Antes de ejecutar el programa es necesario tener instalado los siguientes paquetes:

```rubi
pip install requests
pip install bs4
pip install urllib
pip install pandas
pip install numpy
pip install time
pip install sys
```

Una vez instaladas las librerías necesarias podremos llamar al programa de dos maneras diferentes:

- En el caso de que queramos reproducir la misma búsqueda* con la que se obtuvo el csv **blablacar_extraccion_viajes.csv**, deberemos ejecutar el script de la siguiente manera, en donde los parámetros de entrada son, por orden, origen, destino, asientos, fecha de origen y límite de páginas:
```rubi
python main.py Madrid Cualquiera 1 2019-04-17 Cualquiera
```
- En el caso de querer cambiar los parámetros de búsqueda de viajes, podemos llamar simplemente al script y te irá proponiendo por pantalla los posibles filtros que se pueden utilizar:
```rubi
python main.py
```

_*Cabe notar que aún repitiendo la búsqueda con los mismo parámetros de entrada, debido a la volatilidad de los viajes en BlaBlaCar, difíclmente se puede obtener exactamente el mismo resultado._
