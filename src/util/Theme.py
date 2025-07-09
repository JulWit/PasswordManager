import platform
import winreg
import subprocess
from pathlib import Path

from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication

from src import ROOT_DIR

def is_dark_theme_enabled():
    """
    Bestimmt, ob der Dark Mode auf dem aktuellen Betriebssystem aktiviert ist.

    :return: True, wenn der Dark Mode aktiviert ist, sonst False.
    """
    system = platform.system()
    if system == "Windows":
        return is_dark_theme_windows()
    elif system == "Darwin":
        return is_dark_theme_macos()
    else:
        # Fallback for Linux or unknown: check via Qt
        return is_dark_theme_other()


def is_dark_theme_macos():
    """
    Prüft, ob auf macOS der Dark Mode aktiviert ist.

    :return: True, wenn der Dark Mode aktiv ist, sonst False.
    """
    try:
        result = subprocess.run(
            ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
            capture_output=True, text=True
        )
        return 'Dark' in result.stdout
    except:
        return False


def is_dark_theme_windows():
    """
    Prüft, ob auf Windows der Dark Mode aktiviert ist.

    :return: True, wenn der Dark Mode aktiv ist, sonst False.
    """
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        # 0 = Dark mode, 1 = Light mode
        return value == 0
    except:
        return False


def is_dark_theme_other():
    """
    Prüft, ob ein dunkles Qt-Design aktiv ist (z.B. unter Linux).

    :return: True, wenn das aktuelle Qt-Theme dunkel ist, sonst False.
    """
    palette = QApplication.palette()
    color = palette.color(QPalette.ColorRole.Window)
    # HSV brightness: <128 is dark
    return color.value() < 128

icon_path_dark = Path(ROOT_DIR) / "img" / "dark"
icon_path_light = Path(ROOT_DIR) / "img" / "light"
icon_path = icon_path_light if is_dark_theme_enabled() else icon_path_dark