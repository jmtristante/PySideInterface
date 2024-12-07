from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ViewerScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("This is the Viewer screen.")
        layout.addWidget(label)
