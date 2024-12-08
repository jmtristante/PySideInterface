from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton


class MessageBoxScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Crear un botón para mostrar el mensaje
        button = QPushButton("Mostrar mensaje", self)
        button.clicked.connect(self.show_message)

        self.setWindowTitle("QMessageBox Example")
        button.resize(200, 100)
        button.move(50, 50)

    def show_message(self):
        # Crear un QMessageBox
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Información")
        msg_box.setText("Este es un mensaje de ejemplo.")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()


if __name__ == "__main__":
    app = QApplication([])
    window = MessageBoxScreen()
    window.show()
    app.exec()
