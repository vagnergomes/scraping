##################################################################################################################
# O código abaixo faz uma verificação na página html de cada impressora buscando a serie e o numerador atual.    #
# Este código atende apenas impressora do modelo X464 e E460 e Brother HL.                                                     #
##################################################################################################################

# from urllib.request import urlopen
# from urllib.error import HTTPError
# from urllib.error import URLError
# from bs4 import BeautifulSoup
import PySimpleGUI as sg
from datetime import date
import Contador_Impressoras.imp_x464 as x
import Contador_Impressoras.imp_mx as mx
import Contador_Impressoras.imp_hl as hl
import Contador_Impressoras.util as u
import re
import time

# O diretório dos arquivos fica na pasta Contadores no disco C do servidores de impressoras TAPMS01VS0052.
diretorio = '//tapms01vs0052/c$/Contadores/'
# diretorio = ''

# Busca os dados por modelo de impressora.
# Cada modelo tem uma pagina web diferente, portanto existe uma classe pra cada
def total_paginas(list_ip):
    list_out = []
    linha = ""
    for ip in list_ip:
        und = u.identifica_unidade(ip)
        ip = str(ip)

        if '10.1.7.2' in ip:
            linha = mx.scraping_mx(und, ip)  # fazer funcao scraping_mx
        elif '10.1.7.17' in ip:
            linha = hl.scraping_hl(und, ip)
        else:
            linha = x.scraping_x464(und, ip)

        if type(linha) is list:
            for lh in linha:
                list_out.append(lh)
        else:
            list_out.append(linha)

    return list_out


def gerar_arquivo(data, lista, lista2, lista3):
    info = ''
    for a in (lista + lista2 + lista3):
        info += a + '\n'

    nome_arquivo = 'contador_imp_' + data
    try:
        arq_existe = open(diretorio+nome_arquivo + '.txt', 'r')
    except:
        arq_existe = False

    # verifica se já existe um arquivo de mesmo nome, caso exista, adiciona um numero na frente do novo.
    if arq_existe:
        cont = 0
        for n in range(1000):
            cont += 1
            nome_arquivo2 = nome_arquivo + ' (' + str(cont) + ')'
            try:
                arq_existe2 = open(diretorio+nome_arquivo2 + '.txt', 'r')
            except:
                arq_existe2 = False
            if arq_existe2 is False:
                nome_arquivo = nome_arquivo2
                break

    # gera o novo arquivo e insere os dados nele.
    with open(diretorio+nome_arquivo + '.txt', 'w') as arquivo:
        arquivo.write('\n------------------------------------------------------\n')
        arquivo.write('CONTADORES IMPRESSORAS TERRENA AGRONEGOCIOS\n')
        arquivo.write('Data: ' + data_em_texto + '\n')
        arquivo.write('Unidade - Ip - Serie - Contador\n')
        arquivo.write(info)
        arquivo.write('\n------------------------------------------------------\n')
        arquivo.close()
        print('> Arquivo ' + arquivo.name + ' gerado com sucesso.')


def ler_txt():
    with open(diretorio+'lista_impressoras.txt', 'r') as arq:
        results = [line.replace('\n', '') for line in arq.readlines()]
        # print(split_list(results))
        length = len(results)
        wanted_parts = 3
        return [results[j * length // wanted_parts: (j + 1) * length // wanted_parts]
                for j in range(wanted_parts)]


# lista de ip das impressoras
#list_ip = ['10.1.7.100', '10.1.7.2', '10.1.7.36', '10.1.7.34', '10.1.7.39', '10.1.7.41', '10.1.7.40',
 #          '10.1.7.37', '10.1.7.38', '10.1.7.31', '10.1.7.32', '10.1.7.33', '10.1.7.35', '10.1.7.30', '10.1.7.46',
  #         '10.1.7.63', '10.1.7.64', '10.1.7.47', '10.1.7.65', '10.1.7.70', '10.1.7.71', '10.1.7.72', '10.14.1.50',
   #        '10.14.1.51', '10.14.1.52', '10.14.1.53']

#list_ip2 = ['10.9.0.20', '10.9.0.24', '10.9.0.100', '10.9.0.170', '10.9.0.15', '10.9.0.45', '10.5.0.20', '10.5.0.170',
 #           '10.5.0.15', '10.5.1.43', '10.5.0.100', '10.10.0.20', '10.10.0.170', '10.10.0.112', '10.10.0.100']

# list_ip3 = ['10.4.0.68', '10.4.0.20', '10.4.0.160', '10.4.0.170', '10.4.0.113', '10.4.0.100', '10.13.0.20',
#             '10.13.0.170', '10.13.0.22', '10.13.0.21', '10.13.0.100']


list_ip, list_ip2, list_ip3 = ler_txt()[0], ler_txt()[1], ler_txt()[2]


if __name__ == '__main__':
    # ini = time.time()
    data_em_texto = date.today().strftime('%d-%m-%Y')
    print('Buscando...')
    lista = total_paginas(list_ip)
    lista2 = total_paginas(list_ip2)
    lista3 = total_paginas(list_ip3)
    gerar_arquivo(data_em_texto, lista, lista2, lista3)
    print('Finalizado!')
    # fim = time.time()
    # print(fim - ini)

