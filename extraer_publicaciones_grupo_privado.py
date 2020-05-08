from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from time import time
import random
import datetime as dt


def extraer_publicaciones_grupo_privado(user,pwd,iteraciones,archivo_final,id_grupo="",ultima_pagina='',mostrar_autor=True,mostrar_iteracion_proceso = True,archivo_proceso=''):
    driver = webdriver.Firefox(executable_path=r'/etc/geckodriver/geckodriver') #Busca el controlador asociado a la libreria


    driver.get("https://mobile.facebook.com/") # Nos dirigimos a la pagina de facebook

    #Proceso de login
    elem = driver.find_element_by_id("m_login_email") 
    elem.send_keys(user)
    elem = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/table/tbody/tr/td/div[2]/div[2]/form/ul/li[2]/section/input')
    elem.send_keys(pwd)
    elem.send_keys(Keys.RETURN)
    if ultima_pagina =="":
        assert id_grupo != "", "No existen los parametros necesesarios para ejecutar"
        ultima_pagina = 'https://mobile.facebook.com/groups/'+id_grupo+'/'
    start = time()    

    
    #Función para capturar las publicaciones de cada pagina cargada
    #Tratar con errores nos ayudará a clasificar la información y a que nuestro spider no "caiga"

    def capturarDatos():
        
        #Extracción autor
        try:
            autorcont = k.find_element_by_xpath(
                './/div/header/table/tbody/tr/td[2]/header/h3')
            autor = autorcont.find_element_by_xpath('.//span/strong[1]/a')
            link_autor = autor.get_attribute('href')
            link_autor = link_autor[28:link_autor.find('?')]
        except:
            autor = None
            link_autor = None
        #Extracción texto publicación
        try:
            texto = k.find_element_by_xpath('.//div/div').text
            texto = texto.replace('\n', "<enter>")
            texto = texto.replace(',', " <coma>")
            texto = texto.replace(';', "<pcoma>")
        except:
            texto = ""
        #Extracción de imagen o recurso
        try:
            imagen = k.find_element_by_xpath('.//img[@class="t"]')
            imagen_content = imagen.get_attribute('alt')
            imagen = imagen.get_attribute('src')
            imagen = imagen.replace('\n', "<enter>")
            imagen = imagen.replace(';', "<pcoma>")
            imagen = imagen.replace(',', " <coma>")
            imagen_content = imagen_content.replace('\n', "<enter>")
            imagen_content = imagen_content.replace(';', "<pcoma>")
            imagen_content = imagen_content.replace(',', " <coma>")
        except:
            imagen = ""
            imagen_content = ""
        #Extracción de la fecha a partir de la hora de tomada estos datos (fecha actual - fecha capturada = fecha publicacion)
        try:
            fecha = k.find_element_by_xpath('.//footer/div[1]').text
        except:
            fecha = ""
        #Extracción número de reacciones
        try:
            num_reacciones = k.find_element_by_xpath(
                './/a[@class="eb ec"]').text
        except:
            num_reacciones = '0'
        #Extracción número de comentarios
        try:
            num_comentarios = (k.find_element_by_xpath(
                './/a[@class="ec"]').text).split(" ")[0]
        except:
            num_comentarios = '0'
        #Extracción del identificador
        try:
            l = k.find_elements_by_xpath('.//footer/div[2]/a')
            if len(l) == 4:
                l = l[1].get_attribute('href')
            else:
                l = l[-2].get_attribute('href')
            m = l.find('id=')
            l = l[m+3:l.find('&', m)]
        except:
            l = '0'
        #Escritura de los datos
        #Para minimizar el uso de memoria abrimos y cerramos en cada pagina cargada el documento
        #Evitar el borrado de información si ocurre un error
        f = open(archivo_final, 'a')
        if autor is not None:
            if mostrar_autor:
                print('Publicación de '+autor.text)
            
        
            f.write('\n' + l+','+autor.text+','+link_autor+','+texto+','+imagen +
                    ','+imagen_content+','+fecha+','+num_reacciones+','+num_comentarios)
        f.close()

        

    sleep(3)
    #ingresamos al grupo o la ultima pagina que visitamos
    driver.get(ultima_pagina)

    #iteraciones sobre la pagina
    # Número de iteración en la que va
    iteracion_en_proceso = 0
    siguiente_pagina = ""
    
    for i in range(0, iteraciones):
        publicaciones = driver.find_elements_by_tag_name('article')[1:]
        iteracion_en_proceso = i
        if mostrar_iteracion_proceso:
            print('Iteración N° '+str(iteracion_en_proceso))
        for k in publicaciones:
            capturarDatos()
             
        siguiente_pagina = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[1]/div[4]/div/a').get_attribute('href')
        driver.get(siguiente_pagina)
        sleep(random.uniform(0.,2.))

    #Se captura la ultima pagina y sus parametros
    capturarDatos()
    siguiente_pagina = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[1]/div[4]/div/a').get_attribute('href')

    #Calculo de los datos del proceso
    end = time()
    tiempo_ejecucion = end - start

    mensaje = 'Fecha y Hora de inicio : '+str(dt.datetime.fromtimestamp(start))+'\nFecha y Hora de fin : '+str(dt.datetime.fromtimestamp(end))+"\nTiempo ejecución : "+str(tiempo_ejecucion)+'seg \nUltima iteración : '+str(iteracion_en_proceso)+'\nSiguiente pagina a visitar : '+str(siguiente_pagina)+'\n'
    print(mensaje)
    datosproceso = open ("datosproceso.txt", "w")
    datosproceso.write(mensaje)
    datosproceso.close()
    driver.quit()

