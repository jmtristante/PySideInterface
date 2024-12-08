from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

class FileDialogScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diálogo de Archivos")

        layout = QVBoxLayout(self)

        # Crear un botón
        self.button = QPushButton("Seleccionar un archivo", self)
        self.button.clicked.connect(self.select_file)

        # Crear una etiqueta
        self.label = QLabel("No se ha seleccionado archivo", self)

        layout.addWidget(self.button)
        layout.addWidget(self.label)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo")
        if file_name:
            self.label.setText(f"Archivo seleccionado: {file_name}")

