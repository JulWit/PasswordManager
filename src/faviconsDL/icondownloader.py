import favicon
import requests
from urllib.parse import urlparse


def download_favicon(url):
    # Methode zum Downloaden des Favicons einer bestimmten URL

    # Favicon URL herausfinden
    icon = favicon.get(url)
    icon = icon[0]

    # Name der Datei erstellen
    file_name = urlparse(url).netloc
    file_name = '.'.join(file_name.split('.')[1:])
    file_name = '.'.join(file_name.split('.')[:1])

    # Favicon Downloaden
    response = requests.get(icon.url, stream=True)
    with open('{}.{}'.format(file_name, icon.format), 'wb') as image:
        for chunk in response.iter_content(1024):
            image.write(chunk)

# Methode testen
download_favicon("https://www.google.com/")





