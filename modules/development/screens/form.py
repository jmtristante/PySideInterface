from PySide6.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, QLabel


class FormLayoutScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout(self)

        # Crear los campos del formulario
        layout.addRow(QLabel("Nombre:"), QLineEdit())
        layout.addRow(QLabel("Edad:"), QLineEdit())
        layout.addRow(QLabel("Correo:"), QLineEdit())

        self.setWindowTitle("QFormLayout Example")
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = FormLayoutScreen()
    window.show()
    app.exec()
