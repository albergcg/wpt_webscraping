<div style="width: 100%; clear: both;">
<div style="float: left; width: 50%;">
<img src="http://www.uoc.edu/portal/_resources/common/imatges/marca_UOC/UOC_Masterbrand.jpg", align="left">
</div>
<div style="float: right; width: 50%;">
<p style="margin: 0; padding-top: 22px; text-align:right;">M2.851 · Tipología y ciclo de vidad de los datos · PRA1</p>
<p style="margin: 0; text-align:right;">2019-2 · Máster Universitario en Ciencia de Datos (<i>Data Science</i>)</p>
<p style="margin: 0; text-align:right; padding-button: 100px;">Estudios de Informática, Multimedia y Telecomunicación</p>
</div>
</div>
<div style="width:100%;">&nbsp;</div>

<div style="background-color: #EDF7FF; border-color: #7C9DBF; border-left: 5px solid #7C9DBF; padding: 0.5em;">
<strong>1. Introducción</strong>
    
En este primer notebook, vamos a realizar una primera exploración sobre el sitio web que buscamos trabajar. Nos servirá como una primera toma de contacto, examinaremos el archivo robots.txt y resolveremos los primeros problemas que nos surjan al realizar nuestras primeras peticiones al servidor.

Autores: <strong>Alberto García Galindo</strong> y <strong>Federico Alejandro Floriano Pardal</strong>
</div>

Para el desarrollo de esta primera práctica, buscamos realizar un ejercico de *web scraping* sobre la página web del World Padel Tour. El objetivo de la misma será la construcción de un conjunto de datos con la información más relevante de los mejores jugadores del mundo del pádel.


```python
URL = "https://www.worldpadeltour.com"
```

Dentro de este sitio web, podemos encontrar un categoría que refleja la información de la clasificación mundial del circuito. Será esta clasificación la que utilizaremos para obtener los registros que contendrá nuestro conjunto de datos.

Para empezar a conocer nuestro sitio web, puede ser interesante explorar el contenido del archivo *robots.txt*, con el objetivo de seguir las recomendaciones del propietario a la hora de realizar el *scraping*.


```python
from urllib.request import urlopen, Request
```


```python
f = urlopen(URL + "/robots.txt")
```


    ---------------------------------------------------------------------------

    HTTPError                                 Traceback (most recent call last)

    <ipython-input-3-f66820f9ce03> in <module>
    ----> 1 f = urlopen(URL + "/robots.txt")
    

    D:\Alberto\Anaconda3\lib\urllib\request.py in urlopen(url, data, timeout, cafile, capath, cadefault, context)
        220     else:
        221         opener = _opener
    --> 222     return opener.open(url, data, timeout)
        223 
        224 def install_opener(opener):
    

    D:\Alberto\Anaconda3\lib\urllib\request.py in open(self, fullurl, data, timeout)
        529         for processor in self.process_response.get(protocol, []):
        530             meth = getattr(processor, meth_name)
    --> 531             response = meth(req, response)
        532 
        533         return response
    

    D:\Alberto\Anaconda3\lib\urllib\request.py in http_response(self, request, response)
        639         if not (200 <= code < 300):
        640             response = self.parent.error(
    --> 641                 'http', request, response, code, msg, hdrs)
        642 
        643         return response
    

    D:\Alberto\Anaconda3\lib\urllib\request.py in error(self, proto, *args)
        567         if http_err:
        568             args = (dict, 'default', 'http_error_default') + orig_args
    --> 569             return self._call_chain(*args)
        570 
        571 # XXX probably also want an abstract factory that knows when it makes
    

    D:\Alberto\Anaconda3\lib\urllib\request.py in _call_chain(self, chain, kind, meth_name, *args)
        501         for handler in handlers:
        502             func = getattr(handler, meth_name)
    --> 503             result = func(*args)
        504             if result is not None:
        505                 return result
    

    D:\Alberto\Anaconda3\lib\urllib\request.py in http_error_default(self, req, fp, code, msg, hdrs)
        647 class HTTPDefaultErrorHandler(BaseHandler):
        648     def http_error_default(self, req, fp, code, msg, hdrs):
    --> 649         raise HTTPError(req.full_url, code, msg, hdrs, fp)
        650 
        651 class HTTPRedirectHandler(BaseHandler):
    

    HTTPError: HTTP Error 403: Forbidden


Como vemos, nada mas intentar leer el archivo *robots.txt* mediante una petición al sitio web nos encontramos con un `HTTP Error 403`, lo que nos indica que el servidor ha rechazado nuestra petición. Cabe la posibilidad de que este rechazo se haya debido al intentar realizar la petición con las cabeceras por defecto generadas por las bibliotecas. Para solucionar este problema, editamos la petición con unas cabeceras estándar.


```python
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "no-cache",
    "dnt": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}
```


```python
req = Request(url=URL + "/robots.txt", headers=headers) 
f = urlopen(req)
```

En esta ocasión, parece que el arhivo se ha leído correctamente. 


```python
print(f.read().decode("utf-8"))
```

    
    
    
    User-agent: *
    Disallow:
    Crawl-delay: 10
    
    

Como vemos, el propietario no tiene bloqueado el acceso a ninguno de los directorios del sitio web. No obstante, aparece la recomendación de esperar 10 segundos entre peticiones.


```python

```
