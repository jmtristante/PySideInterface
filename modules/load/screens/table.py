from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class TableScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("This is the Table screen.")
        layout.addWidget(label)
