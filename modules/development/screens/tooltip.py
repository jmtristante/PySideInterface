from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QToolTip
from PySide6.QtCore import Qt

class ToolTipScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToolTip Ejemplo")

        layout = QVBoxLayout(self)

        # Crear el botón
        self.button = QPushButton("Haz clic en mí", self)
        self.button.clicked.connect(self.show_tooltip)

        layout.addWidget(self.button)

    def show_tooltip(self):
        # Muestra el tooltip en la posición actual del botón cuando se hace clic
        QToolTip.showText(self.button.mapToGlobal(self.button.rect().center()), "Este es un tooltip mostrado al hacer clic.", self.button)

