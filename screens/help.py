from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class HelpScreen(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel("Pantalla de Ayuda", self)
