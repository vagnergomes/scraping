

def verifica_pb_color(und, ip):
    if '10.1.7.100' or '10.14.1.53' in ip:
        linha1 = und + ' - ' + ip + ' - [serie] - COLOR: Erro de protocolo.'
        linha2 = und + ' - ' + ip + ' - [serie] - PRETO/BRANCO: Erro de protocolo.'
        linha = [linha1, linha2]
    else:
        linha = und + ' - ' + ip + ' - Erro de protocolo.'
    return linha


def identifica_unidade(ip):
    und = ''
    if '10.1.' in ip: und = 'PMS'
    if '10.14.' in ip: und = 'STZ'
    if '10.9.' in ip: und = 'PTR'
    if '10.5.' in ip: und = 'IBA'
    if '10.10.' in ip: und = 'SGT'
    if '10.4.' in ip: und = 'PTU'
    if '10.13.' in ip: und = 'CMP'
    return und