# Passwort Manager
Passwort Manager auf Basis von Python. Die grafische Benutzeroberfläche wurde mit Pyside und Qt6 umgesetzt.
Die Einträgen werden in einer lokalen SQLite Datenbank gespeichert, welche mit AES256 und dem Betriebsmodus CBC
verschlüsselt wird.

#Funktionen
* Verschlüsselte Speicherung von Einträgen, welche aus einem Benutzernamne, Passwort, URL und ggf. Notizen bestehen
* Passwortgenerator mit anpassbarer Länge und Auswahl von Sonderzeichen
* Einfaches kopieren von Benutzername und Passwort
* Aufruf von gespeicherten URLs im Browser
* Automatischer Favicon-Download für eingetragene URLs

#Bilder
[![Screenshot-from-2021-12-07-05-22-17.png](https://i.postimg.cc/KcwCTbtw/Screenshot-from-2021-12-07-05-22-17.png)](https://postimg.cc/nMKd86RG)
[![Screenshot-from-2021-12-07-05-24-16.png](https://i.postimg.cc/X75mcP8J/Screenshot-from-2021-12-07-05-24-16.png)](https://postimg.cc/QHXfj0vG)
[![Screenshot-from-2021-12-07-05-26-49.png](https://i.postimg.cc/V6TZX90n/Screenshot-from-2021-12-07-05-26-49.png)](https://postimg.cc/1nGKQqH3)
[![Screenshot-from-2021-12-07-05-26-53.png](https://i.postimg.cc/2yZcGqnJ/Screenshot-from-2021-12-07-05-26-53.png)](https://postimg.cc/1Vyr53Cc)

#Installation
1. `sudo apt install git`
2. `sudo apt install libopengl0`
3. `sudo apt install python3-pip`
4. Wechsel in das Verzeichnis in dem sich das Projekt befinden soll
5. `git clone https://github.com/JulWit/PasswordManager.git`
6. `cd PasswordManager`
7. `pip3 install -r requirements.txt`
8. `python3 start.py`
