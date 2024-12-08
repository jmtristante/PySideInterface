from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit
from PySide6.QtGui import QClipboard


class ClipboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.text_edit = QLineEdit(self)
        layout.addWidget(self.text_edit)

        # Crear botón para copiar al portapapeles
        copy_button = QPushButton("Copiar al portapapeles", self)
        copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(copy_button)

        # Crear botón para pegar desde el portapapeles
        paste_button = QPushButton("Pegar del portapapeles", self)
        paste_button.clicked.connect(self.paste_from_clipboard)
        layout.addWidget(paste_button)

        self.setWindowTitle("QClipboard Example")
        self.setLayout(layout)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.text())

    def paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        self.text_edit.setText(clipboard.text())


if __name__ == "__main__":
    app = QApplication([])
    window = ClipboardScreen()
    window.show()
    app.exec()
