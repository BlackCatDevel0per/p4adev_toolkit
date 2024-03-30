import ssl
# from os import environ as os_environ

# from certifi import where as where_cert

# TODO: Try to modify env vars & "patch" some libs to avoid ssl issues..
# os_environ['SSL_CERT_FILE'] = where_cert()


# ssl_context = ssl.create_default_context(cafile=where_cert())

ssl._create_default_https_context = ssl._create_stdlib_context


# Test by:
"""
from urllib.request import urlopen

from kivy.logger import Logger

try:
    # Logger.warning(f'Cert path: `{certifi.where()}`')
    resp = urlopen('https://daviantart.com').read()[:100]
    # resp = urlopen('https://daviantart.com', context=ssl.create_default_context(cafile=certifi.where())).read()[:100]
    Logger.warning(f'{resp}')
except Exception as e:
    Logger.warning(f'Exception: `{e}`')
    exit()
"""
