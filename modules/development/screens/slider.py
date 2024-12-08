from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PySide6.QtCore import Qt


class SliderScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Slider")

        layout = QVBoxLayout(self)

        # Crear un slider
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.update_label)

        # Crear una etiqueta
        self.label = QLabel(f"Valor seleccionado: {self.slider.value()}", self)

        layout.addWidget(self.slider)
        layout.addWidget(self.label)

    def update_label(self):
        self.label.setText(f"Valor seleccionado: {self.slider.value()}")

