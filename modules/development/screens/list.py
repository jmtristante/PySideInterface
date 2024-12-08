from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget


class ListWidgetScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Crear el QListWidget
        list_widget = QListWidget()

        # Agregar elementos a la lista
        list_widget.addItem("Elemento 1")
        list_widget.addItem("Elemento 2")
        list_widget.addItem("Elemento 3")

        layout.addWidget(list_widget)
        self.setWindowTitle("QListWidget Example")
        self.setLayout(layout)

