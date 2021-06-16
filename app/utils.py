from flask import request
from urllib.parse import urlparse, urljoin
from enum import IntEnum

class TipoClaseEnum(IntEnum):
    lab = 0
    teoria = 1
    teoria_virtual = 2


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def status_horario(horario):
    horario_dict = {}
    horario_table = [
        #L ,M ,M ,J ,V ,S ,D
        ['','','','','','',''], #7-8
        ['','','','','','',''], #8-8
        ['','','','','','',''], #9-9
        ['','','','','','',''], #10-10
        ['','','','','','',''], #11-12
        ['','','','','','',''], #12-13
        ['','','','','','',''], #13-14
        ['','','','','','',''], #14-15
        ['','','','','','',''], #15-16
        ['','','','','','',''], #16-17
        ['','','','','','',''], #17-18
        ['','','','','','',''], #18-19
        ['','','','','','',''], #19-20
        ['','','','','','',''], #20-21
        ['','','','','','',''], #21-22
    ] 
    for c in horario.clases:
        for s in c.sesiones:
            for hora in range(s.hora_inicio, s.hora_fin):
                horario_table[hora-7][s.dia-1] = c.curso.codigo

        if c.curso.codigo in horario_dict:
            horario_dict[c.curso.codigo][0] += 2**c.tipo.value
        else:
            horario_dict[c.curso.codigo] = [2**c.tipo.value, c.curso.lab * 2**TipoClaseEnum.lab.value + c.curso.teoria * 2**TipoClaseEnum.teoria.value + c.curso.teoria_virtual * 2**TipoClaseEnum.teoria_virtual.value]
    status = "Complete"
    cursos_pendientes = []
    for c in horario_dict:
        if horario_dict[c][0] != horario_dict[c][1]:
            status = "Pending"
            cursos_pendientes.append(c)
    return status, horario_table, ",".join(cursos_pendientes)