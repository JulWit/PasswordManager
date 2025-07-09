import favicon
import requests
import re
from src import ROOT_DIR
from PySide6.QtCore import QByteArray

from src.util.Theme import icon_path


def format_url(url) -> str:
    """
    Formatiert eine URL, indem sie bei Bedarf ein Protokoll wie 'http://' hinzufügt.

    Wenn die übergebene URL kein gültiges Protokoll (http, https, ftp) enthält,
    wird standardmäßig 'http://' vorangestellt.

    :param url: Die zu formatierende URL.
    :return: Eine gültige URL mit Protokoll.
    """
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url


def download_favicon(url) -> QByteArray | bytearray:
    """
    Lädt das Favicon einer gegebenen Website herunter.

    Es wird zunächst versucht, mithilfe des `favicon`-Moduls die Favicon-URL der Website zu ermitteln.
    Anschließend wird das Favicon über einen HTTP-Request heruntergeladen und als Bytearray zurückgegeben.
    Falls kein Favicon gefunden oder ein Fehler auftritt, wird ein Standard-Icon (`globe.svg`) aus dem Projektverzeichnis zurückgegeben.

    :param url: Die URL der Website, von der das Favicon geladen werden soll.
    :return: Das Favicon als `bytearray`. Im Fehlerfall das Standard-Icon.
    """
    try:
        icons = favicon.get(format_url(url), timeout=2)
        icon = icons[0]

        # Favicon Downloaden
        response = requests.get(icon.url, stream=True)
        img_bytes = QByteArray()
        for chunk in response.iter_content(1024):
            img_bytes.append(chunk)

        return img_bytes

    except:
        with open(str(icon_path / "globe.svg"), "rb") as image:
            icon = image.read()
        return bytearray(icon)
