from PySide6.QtWidgets import QApplication, QWidget


def center_on_screen(widget: QWidget):
    """
    Zentriert das übergebene Widget auf dem primären Bildschirm.

    Diese Funktion berechnet die Mitte des verfügbaren Bereichs des primären Bildschirms
    und verschiebt das Widget so, dass es zentriert angezeigt wird.

    :param widget: Das Widget, das auf dem Bildschirm zentriert werden soll.
    """
    screen = QApplication.primaryScreen()
    screen_geometry = screen.availableGeometry()
    dialog_geometry = widget.frameGeometry()
    dialog_geometry.moveCenter(screen_geometry.center())
    widget.move(dialog_geometry.topLeft())


def center_on_parent(widget: QWidget):
    """
    Zentriert das übergebene Widget relativ zu seinem Elternelement.

    Falls das Widget ein übergeordnetes Widget hat, wird dessen Geometrie verwendet,
    um das übergebene Widget zentriert darüber anzuordnen.

    :param widget: Das Widget, das relativ zu seinem Elternelement zentriert werden soll.
    """
    if widget.parent():
        parent_geometry = widget.parent().frameGeometry()
        dialog_geometry = widget.frameGeometry()
        dialog_geometry.moveCenter(parent_geometry.center())
        widget.move(dialog_geometry.topLeft())
