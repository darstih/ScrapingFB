# Extraer publicaciones de grupo privado de facebook



## Uso
Usar esta función cuando requiera hacer una extracción de las publicaciones sin los comentarios de un grupo de facebook privado del cual tenga una cuenta con acceso a este

## extraer_publicaciones_grupo_privado
```
extraer_publicaciones_grupo_privado(user,pwd,iteraciones,archivo_final,id_grupo="",ultima_pagina='',mostrar_autor=True,mostrar_iteracion_proceso = True,archivo_proceso='')
```


## Parametros
- user: Usuario de la cuenta de facebook que tiene acceso al grupo
- pwd: Contraseña de la cuenta
- iteraciones: cantidad de paginas a las cuales va a entrar el algoritmo
- archivo_final: ruta del archivo en formato csv o txt en la cual se escribiran los datos extraidos
- id_grupo: identificador del grupo objetivo
- archivo proceso: (opcional) si se desea guardar los datos del proceso ingrese esta variable como la ruta donde se guardarán los datos del proceso al finalizar la ejecución
- ultima_pagina: (opcional) si usted ya ejecutó una primera extracción con las iteraciones insuficientes podrá continuar escribiendo aquí la pagina siguiente de los datos de proceso
- mostrar_autor: (opcional) si desea observar en consola los autores de cada publicación escrita a medida que se extraen los datos
- mostrar_iteracion_proceso: (opcional) si desea observar en consola el número de iteraciones a medida que se cargan


## Salida
Al finalizar la ejecución se mostrará por pantalla y/o se guardarán los datos del proceso
Hora de inicio, tiempo de ejecución, ultima iteración, siguiente pagina a visitar la cual se podrá usar para continuar más adelante la extracción

En el archivo final podra ver los datos de cada publicación  
id,autor,usuario_autor,texto,imagen,imagen_content,fecha,num_reacciones,num_comentarios

La fecha capturada en las primeras publicaciones será la fecha a partir de la hora de tomada estos datos (fecha actual - fecha capturada = fecha publicacion)

Capturará publicaciones con identificador 0, que significa en realidad que son publicaciones externas al  grupo que un usuario compartió en este

El texto que captura que contenga comas y/o saltos de linea serán reemplazadas por <coma> y/o <enter> respectivamente



### Ejemplo
- usuario = user
- password = password
- iteraciones = 10000
- id_grupo = 1
- archivo final = publicaciones.csv
```
extraer_publicaciones_grupo_privado(user = 'user',pwd='password',iteraciones=10000,id_grupo="149144201830763",archivo_final='publicaciones.csv',archivo_proceso='datosproceso.txt')
```


## Descripción
El codigo aquí implementado contiene una función que hace una extracción de datos de un grupo privado del cual el usuario es miembro, saltando de esta forma la mala calidad que nos brinda la API de facebook.

## Características
* Se usa la libreria selenium de python [Documentación selenium](https://selenium-python.readthedocs.io/)
* Por lo anterior abrira un navegador web donde simulará una la vista de un usuario
* El algoritmo escribirá en disco cada publicación
* El algoritmo usará la antigua mobile.facebook.com para minimizar el uso de red
* Podrá descargar gran cantidad de estos datos
* Tiene una velocidad aproximada de #### publicaciones por hora

## Requerimientos
* python 3
* libreria selenium
* descargar el geckodriver de la libreria según el navegador que usará para este proposito
* conexión a internet(obviamente)

## Desventajas 
* Por evitar que facebook identifique el algoritmo como robot, este debe hacer ciertas pausas para "Humanizar" el comportamiento, por lo tanto, gastará bastante tiempo
* Dado que usamos mobile.facebook.com el algoritmo no podrá obtener los comentarios, sin embargo, al obtener el id de la publicación se puede hacer un scraping horizontal iterando por cada uno de estos
