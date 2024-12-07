from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel("Pantalla de Configuración", self)
