import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://lapatria.bo/'

XPATH_LINK_TO_ARTICLE= '//h3[@class="entry-title td-module-title"]/a/@href'
XPATH_TITLE='//div/p/text()'
XPATH_BODY='//div/p/text()'

# Creamos las funcioens para ejecutar el script.
def parse_notice(link, today,num):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                #title = title.replace('"','') #eliminar las comillas de un título en caso de que existan para evitar errores
                body = parsed.xpath(XPATH_BODY) #tomar los parrafos de Body.
            except IndexError: #en caso de que no haya resumen o body, regresa a la función en vez de marcar un error.
                return
            with open(f'{today}/{num}.txt','w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                #f.write(summary)
                f.write('\n\n')
                for p in body:
                    parrafo=p.replace('-','')
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices) #se imprime para ver como progresa
            today = datetime.date.today().strftime('%d-%m-%y')#funcion trae una fecha, today trae la de hoy y strftime le da un formato deseado.
            if not os.path.isdir(today):
                os.mkdir(today)
            cont=1
            for link in links_to_notices:
                parse_notice(link, today,cont)
                cont+=1
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()


if __name__ == '__main__':
    run()