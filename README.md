World Padel Tour - Top 50 Dataset
---

> Autores: Alberto García Galindo y Federico Alejandro Floriano Pardal

> Asignatura: M2.851 - Tipología y ciclo de vida de los datos

> Titulación: Máster Universitario en Ciencia de Datos (Data Science)

Introducción
---

Este repositorio se enmarca en la elaboración de la práctica 1 de *web scraping* de la asignatura *Tipología y ciclo de vida de los datos*, perteneciente al plan de estudio del Máster en Cienca de Datos (Data Science) de la Universitat Oberta de Catalunya. 

Objetivo
---

En esta práctica se plantea el objetivo de utilizar técnicas de *web scraping* en el lenguaje de programación Python para la construcción de un conjunto de datos con la información de los 50 mejores jugadores y las 50 mejores jugadoras del ránking [World Padel Tour](https://www.worldpadeltour.com/).

Para ello, se partirá de la página web donde se muestra la clasificación de los mejores jugadores y jugadoras del mundo. Exploraremos la información de los jugadores y obtendremos algunas características interesantes como su posición, su altura o los resultados en las competiciones de anteriores campaañs.

Estructura del proyecto
---

- `informe`. En este fichero encontramos el informe técnico del proyecto realizado, el contexto en el que se ha realizado e información sobre el conjunto de datos generado.
- `scrapers`. En este fichero encontramos el script `main.py` que, al ejecutarse, invocará a la clase `WPTScraper` y procederá a la obtención de los datos de los jugadores y los almacenará en un archvio csv.
- `dataset`. Conjunto de datos resultante del proyecto, con la información de los 100 jugadores y jugadoras.
- `notebooks`. Jupyter Notebooks información adicional del proyecto. Se incluye una primera exploración del sitio web y un primer análisis del conjunto de datos resultante.
