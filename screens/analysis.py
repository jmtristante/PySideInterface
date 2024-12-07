from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AnalysisScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("This is the Analysis screen.")
        layout.addWidget(label)
