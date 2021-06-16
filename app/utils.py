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
    for c in horario.clases:
        if c.curso.codigo in horario_dict:
            horario_dict[c.curso.codigo][0] += 2**c.tipo.value
        else:
            horario_dict[c.curso.codigo] = [2**c.tipo.value, c.curso.lab * 2**TipoClaseEnum.lab.value + c.curso.teoria * 2**TipoClaseEnum.teoria.value + c.curso.teoria_virtual * 2**TipoClaseEnum.teoria_virtual.value]
    status = "Complete"
    for c in horario_dict:
        if horario_dict[c][0] != horario_dict[c][1]:
            status = "Pending"
            break
    return status