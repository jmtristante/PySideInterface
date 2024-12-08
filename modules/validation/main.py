from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("This is the Validation screen.")
        layout.addWidget(label)
