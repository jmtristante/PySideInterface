from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QPushButton, QLabel


class RadioButtonScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Radio Buttons")

        layout = QVBoxLayout(self)

        # Crear radio buttons
        self.radio_button_1 = QRadioButton("Opción 1", self)
        self.radio_button_2 = QRadioButton("Opción 2", self)

        # Crear un botón
        self.button = QPushButton("Seleccionar Opción", self)
        self.button.clicked.connect(self.show_selected_option)

        # Crear una etiqueta
        self.label = QLabel("Selecciona una opción", self)

        layout.addWidget(self.radio_button_1)
        layout.addWidget(self.radio_button_2)
        layout.addWidget(self.button)
        layout.addWidget(self.label)

    def show_selected_option(self):
        if self.radio_button_1.isChecked():
            self.label.setText("Opción 1 seleccionada")
        elif self.radio_button_2.isChecked():
            self.label.setText("Opción 2 seleccionada")
        else:
            self.label.setText("Ninguna opción seleccionada")

