import favicon
import requests
import os

from PySide6.QtCore import QByteArray, QFile, QIODevice


def download_favicon(url):
    # Methode zum Downloaden des Favicons einer bestimmten URL

    # Favicon URL herausfinden
    icons = favicon.get(url)
    icon = icons[0]

    # Favicon Downloaden
    response = requests.get(icon.url, stream=True)
    img_bytes = QByteArray()
    for chunk in response.iter_content(1024):
        img_bytes.append(chunk)

    return img_bytes

"""
    file = QFile("/home/marius/test.ico")
    file.open(QIODevice.WriteOnly)
    file.write(img_bytes)
    file.close()
"""

