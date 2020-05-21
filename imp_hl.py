import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import util


def scraping_hl(und, ip):
    dict_tags = {}
    linha = ""

    try:
        scraping_url = requests.get('http://'+ip+'/printer/maininfo.html').text
    except HTTPError:
        linha = util.verifica_pb_color(und, ip)
    except URLError:
        linha = und + ' - ' + ip + ' - Destino nao encontrado.'
    else:
        res = BeautifulSoup(scraping_url, 'html.parser')

        # adiciono todas as tabelas da pagina em uma lista
        tables = []
        tables = res.findAll('table')

        # posicao da tabela que estão os dados procurados
        table = tables[5]

        lines = []
        lines = str(table).split("\n")

        list = []
        for l in lines:
            if l.__contains__("<dd>Serial no.") or l.__contains__("<dd>Page Count"):
                list.append(l)

        for t in list:
            r = []
            r = t.split('<td>')
            chave = r[0].replace('<dd>', '').replace('</dd></td>', '')
            valor = r[1].replace('</td>', '').replace('</tr>', '')

            dict_tags.update({chave: valor})

        serie = dict_tags.get('Serial no.', 'Serie nao encontrada.')
        total = dict_tags.get('Page Count', 'Contagem nao Encontrada.')

        linha = und + ' - ' + ip + ' - ' + serie.strip() + ': ' + total.strip()

    return linha


# print(scraping_hj('PMS', '10.1.7.17'))