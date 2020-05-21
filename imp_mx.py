from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import util


def scraping_mx(und, ip):
    dict_tags = {}
    dict_serie = {}
    linha = ""
    try:
        scrape_url = 'http://'+ip+'/sys_count.html'
        scrape_url_main = 'http://'+ip+'/main.html'
        html = urlopen(scrape_url)
        html_main = urlopen(scrape_url_main)
    except HTTPError as e:
        linha = util.verifica_pb_color(und, ip)
    except URLError as u:
        linha = und + ' - ' + ip + ' - Destino nao encontrado.'
    else:
        res = BeautifulSoup(html, 'html.parser')
        res_main = BeautifulSoup(html_main, 'html.parser')

        # list_tr = res.find_all('tr')
        list_form = []
        for tr in res.find_all('tr'):
            for td in tr:
                for t in td:
                    list_form.append(t)

            chave = list_form[1]
            valor = list_form[3].replace('=', ' ')
            dict_tags.update({chave: valor})
            if chave == "Cor Única":
                break

            list_form.clear()

        list_main = []
        for tr in res_main.find_all('tr'):
            for td in tr:
                for t in td:
                    list_main.append(t)

            chave = list_main[1]
            valor = list_main[3].replace('=', ' ')
            dict_serie.update({chave: valor})

            if chave == "Nome do Modelo:":
                break

            list_main.clear()

        # busca a chave referente ao campo da página html
        serie = dict_serie.get('Número de Série da Unidade:', 'Serie não encontrada')

        # busca a contagem referente ao campo da página html
        total_pb = dict_tags.get('Preto e branco', 'Contador Preto e Branco não encontrado.')
        total_color = dict_tags.get('Cor Total', 'Contador Colorido não encontrado.')

        linha1 = und + ' - ' + ip + ' - ' + serie.strip() + ' - COLOR: ' + total_pb.strip()
        linha2 = und + ' - ' + ip + ' - ' + serie.strip() + ' - PRETO/BRANCO: ' + total_color.strip()
        linha = [linha1, linha2]

    return linha


#  scraping_mx('PMS', '10.1.7.2')
