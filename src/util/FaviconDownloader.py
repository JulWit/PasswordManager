import favicon
import requests
import re
from src import ROOT_DIR
from PySide6.QtCore import QByteArray


def formaturl(url) -> str:
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url


def download_favicon(url) -> bytearray:
    # Methode zum Downloaden des Favicons einer bestimmten URL

    # Favicon URL herausfinden
    try:
        icons = favicon.get(formaturl(url), timeout=2)
        icon = icons[0]

        # Favicon Downloaden
        response = requests.get(icon.url, stream=True)
        img_bytes = QByteArray()
        for chunk in response.iter_content(1024):
            img_bytes.append(chunk)

        return img_bytes

    except:
        with open(ROOT_DIR + "/img/globe.svg", "rb") as image:
            icon = image.read()
        return bytearray(icon)
