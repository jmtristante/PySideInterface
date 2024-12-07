from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ExecutionScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("This is the Execution screen.")
        layout.addWidget(label)
