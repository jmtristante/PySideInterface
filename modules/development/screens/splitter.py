from PySide6.QtWidgets import QApplication, QWidget, QSplitter, QTextEdit, QVBoxLayout


class SplitterScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Crear el QSplitter
        splitter = QSplitter(self)

        # Crear dos paneles con QTextEdit
        text_edit1 = QTextEdit("Panel 1")
        text_edit2 = QTextEdit("Panel 2")

        # Agregar los widgets al splitter
        splitter.addWidget(text_edit1)
        splitter.addWidget(text_edit2)

        layout.addWidget(splitter)
        self.setWindowTitle("QSplitter Example")
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = SplitterScreen()
    window.show()
    app.exec()
