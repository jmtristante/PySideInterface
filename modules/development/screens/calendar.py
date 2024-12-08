from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCalendarWidget


class CalendarWidgetScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Crear el QCalendarWidget
        calendar = QCalendarWidget()
        layout.addWidget(calendar)

        self.setWindowTitle("QCalendarWidget Example")
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = CalendarWidgetScreen()
    window.show()
    app.exec()
