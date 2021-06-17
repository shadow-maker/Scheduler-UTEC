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
