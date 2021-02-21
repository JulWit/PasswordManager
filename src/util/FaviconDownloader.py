import favicon
import requests
import os


def download_favicon(url):
    # Methode zum Downloaden des Favicons einer bestimmten URL

    # Favicon URL herausfinden
    icons = favicon.get(url)
    icon = icons[0]

    # Name der Datei erstellen
    i = 1
    file_pattern = 'favicon-%s.%s'
    while os.path.exists(file_pattern % (i, icon.format)):
        i += 1
    file_name = file_pattern % (i, format(icon.format))

    # Favicon Downloaden
    response = requests.get(icon.url, stream=True)
    with open('{}'.format(file_name), 'wb') as image:
        for chunk in response.iter_content(1024):
            image.write(chunk)


# Methode testen
download_favicon("https://www.fh-swf.de")
#download_favicon("http://google.com")
# download_favicon("google.com")
