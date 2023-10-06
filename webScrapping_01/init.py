from bs4 import BeautifulSoup
import requests
import lxml.html as html

def parser_func(url):
    req = requests.get(url)
    home = req.content.decode('utf-8')

    parser = html.fromstring(home)
    return parser


def buscarInfo(urls_inmueble):


    for i in urls_inmueble:
        title = '//div[@class="bg-darken-1 px3 py2"]/h1/text()'
        price = '//div[@class="bg-darken-1 px3 py2"]//div[@class="h2 mt0 main bolder"]/text()'
        tipo_ope_dor = '//div[@class="inline-flex align-baseline2 col-10"]/a/text()'
        zona = '//div[@class="col col-12 md-pt2"]/p[@class="mt0 h4"]/text()'
        date = '//div[@class="bg-darken-1 px3 py2"]//div[@class="h5 center"]/text()'

        parser = parser_func(i)

        precio = parser.xpath(price)
        data_list= parser.xpath(tipo_ope_dor)
        barrio=parser.xpath(zona)
        titulo = parser.xpath(title)
        aux_fecha = parser.xpath(date)

        aux_fecha = aux_fecha[0].lstrip('Fecha de actualización: ')

        if(len(barrio)!=1):
            barrio.append("null")

        if (len(data_list)==1):
            data_list.insert(0,"Comercio")
            data_list.append("N/A")
        elif(len(data_list)<1):
            data_list.append("null")
            data_list.append("null")
            data_list.append("null")

        data_list.append(precio[0])
        data_list.append(barrio[0])
        data_list.append(aux_fecha)
        data_list.append(titulo[0])

        print(f"*{data_list}*\n") 
        #guardar



# url de la pagina de la voz con filtros previos en cba, alquileres departamentos
url_ppal = "https://clasificados.lavoz.com.ar/inmuebles/todo?ciudad=cordoba&operacion=alquileres"

paginacion = '//a[@class="page-link h4"]/text()'
links_inmuebles = '//div[@class="col col-12 mx1 md-mx0 md-mr1 bg-white mb2 line-height-3 card relative safari-card "]/a[@class="text-decoration-none"]/@href'

parser = parser_func(url_ppal)

cantidad_de_paginas = parser.xpath(paginacion)

maximo = int(cantidad_de_paginas[-1])

for i in range(1, maximo):
    
    pagina = f"{url_ppal}&page={i}"
    parser = parser_func(pagina)
    links = parser.xpath(links_inmuebles)

    print(f"**********{pagina}**********\n")

    buscarInfo(links)    

    if (i == 2):
        break




