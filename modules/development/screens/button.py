from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit


class ButtonScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Botones y Cuadros de Texto")

        layout = QVBoxLayout(self)

        # Crear un cuadro de texto
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Escribe algo aquí...")

        # Crear una etiqueta
        self.label = QLabel("Texto ingresado aparecerá aquí:", self)

        # Crear un botón
        self.button = QPushButton("Mostrar Texto", self)
        self.button.clicked.connect(self.show_text)

        layout.addWidget(self.text_input)
        layout.addWidget(self.button)
        layout.addWidget(self.label)

    def show_text(self):
        entered_text = self.text_input.text()
        self.label.setText(f"Texto ingresado: {entered_text}")






