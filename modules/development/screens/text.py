from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton


class TextEditScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cuadro de Texto")

        layout = QVBoxLayout(self)

        # Crear un QTextEdit
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Escribe algo aquí...")

        # Crear un botón
        self.button = QPushButton("Mostrar Texto", self)
        self.button.clicked.connect(self.show_text)

        layout.addWidget(self.text_edit)
        layout.addWidget(self.button)

    def show_text(self):
        entered_text = self.text_edit.toPlainText()
        print("Texto ingresado:", entered_text)

