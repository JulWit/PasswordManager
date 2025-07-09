from dataclasses import dataclass
from datetime import datetime

from PySide6.QtCore import QByteArray


@dataclass
class Entry:
    id: str | None  = None
    title: str = None
    username: str = None
    password: str = None
    url: str = None
    notes: str = None
    icon: QByteArray | bytearray = None
    modified: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
