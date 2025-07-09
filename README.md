# Passwort Manager
Implementierung eines Passwort Managers in Python. Die grafische Benutzeroberfläche wurde mit PySide und Qt6 umgesetzt.
Die Einträge werden in einer lokalen SQLite Datenbank gespeichert, welche mit AES256 und dem Betriebsmodus CBC
verschlüsselt wird.

## Funktionen
* Verschlüsselte Speicherung von Einträgen, welche aus einem Benutzernamen, Passwort, URL und ggf. Notizen bestehen
* Passwortgenerator mit anpassbarer Passwortlänge und enthaltenen Sonderzeichen
* Einfaches kopieren von Benutzername und Passwort
* Aufruf von gespeicherten URLs im Browser
* Automatischer Favicon-Download für eingetragene URLs
* Durchsuchen von Einträgen

## Bilder
[![Screenshot-from-2021-12-07-05-22-17.png](https://i.postimg.cc/KcwCTbtw/Screenshot-from-2021-12-07-05-22-17.png)](https://postimg.cc/nMKd86RG)
[![Screenshot-from-2021-12-07-05-24-16.png](https://i.postimg.cc/X75mcP8J/Screenshot-from-2021-12-07-05-24-16.png)](https://postimg.cc/QHXfj0vG)
[![Screenshot-from-2021-12-07-05-26-49.png](https://i.postimg.cc/V6TZX90n/Screenshot-from-2021-12-07-05-26-49.png)](https://postimg.cc/1nGKQqH3)
[![Screenshot-from-2021-12-07-05-26-53.png](https://i.postimg.cc/2yZcGqnJ/Screenshot-from-2021-12-07-05-26-53.png)](https://postimg.cc/1Vyr53Cc)
[![Screenshot-from-2025-09-07-13-92-53.png](https://i.postimg.cc/prPW8cNx/Screenshot-2025-07-09-130048.png)](https://postimg.cc/xJFVVRTF)

## Installation (Ubuntu)
1. `sudo apt install git`
2. `sudo apt install libopengl0`
3. `sudo apt install python3-pip`
4. Wechsel in das Verzeichnis in dem das Projekt geklont werden soll (z. B. /home/PasswordManager)
5. `git clone https://github.com/JulWit/PasswordManager.git`
6. `cd PasswordManager`
7. `pip3 install -r requirements.txt`
8. `python3 start.py`
