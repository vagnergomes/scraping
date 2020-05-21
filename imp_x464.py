from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import util


def scraping_x464(und, ip):
    dict_tags = {}
    linha = ""
    try:
        scrape_url = 'http://' + ip + '/cgi-bin/dynamic/printer/config/reports/deviceinfo.html'
        html = urlopen(scrape_url)
    except HTTPError as e:
        linha = util.verifica_pb_color(und, ip)
    except URLError as u:
        linha = und + ' - ' + ip + ' - Destino nao encontrado.'
    else:
        res = BeautifulSoup(html, 'html.parser')

        # list_tr = res.find_all('tr')
        list_form = []
        for tr in res.find_all('tr'):
            for td in tr:
                for p in td:
                    for t in p:
                        list_form.append(t)

            if len(list_form) > 2:
                list_form.pop(2)

            chave = str(list_form[0])
            valor = list_form[1].replace('=', ' ')
            dict_tags.update({chave: valor})

            if chave == "TLI":
                break

            list_form.clear()

        # busca a chave referente ao campo da página html
        serie = dict_tags.get('Número\xa0de\xa0série', False)
        if serie == False:
            serie = dict_tags.get('Número de série', False)
        if serie == False:
            serie = dict_tags.get('Número de Série', 'Serie nao encontrada.')

        # busca a contagem referente ao campo da página html
        total = dict_tags.get('Contagem\xa0pág.', False)
        if total == False:
            total = dict_tags.get('Contagem pág.', False)
        if total == False:
            total = dict_tags.get('Cont. Pág.', 'Contagem nao Encontrada.')

        linha = und + ' - ' + ip + ' - ' + serie.strip() + ': ' + total.strip()

    return linha


