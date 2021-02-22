import favicon
import requests
import os

from PySide6.QtCore import QByteArray, QFile, QIODevice

import re


def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url


def download_favicon(url):
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
        return None


"""
    file = QFile("/home/marius/test.ico")
    file.open(QIODevice.WriteOnly)
    file.write(img_bytes)
    file.close()
"""
