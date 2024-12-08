from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSpinBox, QLabel

class SpinBoxScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SpinBox")

        layout = QVBoxLayout(self)

        # Crear un spin box
        self.spin_box = QSpinBox(self)
        self.spin_box.setRange(1, 100)
        self.spin_box.setValue(1)

        # Crear una etiqueta
        self.label = QLabel(f"Valor seleccionado: {self.spin_box.value()}", self)
        self.spin_box.valueChanged.connect(self.update_label)

        layout.addWidget(self.spin_box)
        layout.addWidget(self.label)

    def update_label(self):
        self.label.setText(f"Valor seleccionado: {self.spin_box.value()}")

