from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox, QLabel


class CheckboxScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Checkbox y Botón")

        layout = QVBoxLayout(self)

        # Crear un checkbox
        self.checkbox = QCheckBox("Aceptar términos y condiciones", self)

        # Crear una etiqueta
        self.label = QLabel("El checkbox no ha sido marcado", self)

        # Crear un botón
        self.button = QPushButton("Verificar Estado", self)
        self.button.clicked.connect(self.check_status)

        layout.addWidget(self.checkbox)
        layout.addWidget(self.button)
        layout.addWidget(self.label)

    def check_status(self):
        if self.checkbox.isChecked():
            self.label.setText("El checkbox ha sido marcado")
        else:
            self.label.setText("El checkbox no ha sido marcado")

