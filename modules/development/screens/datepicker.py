from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QDateTimeEdit, QLabel


class DateTimePickerScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selector de Fecha y Hora")

        layout = QVBoxLayout(self)

        # Crear un QDateTimeEdit
        self.date_time_picker = QDateTimeEdit(self)
        self.date_time_picker.setDateTime(self.date_time_picker.dateTime())

        # Crear una etiqueta
        self.label = QLabel(f"Fecha y Hora seleccionada: {self.date_time_picker.dateTime().toString()}", self)

        # Conectar el evento de cambio de valor
        self.date_time_picker.dateTimeChanged.connect(self.update_label)

        layout.addWidget(self.date_time_picker)
        layout.addWidget(self.label)

    def update_label(self):
        self.label.setText(f"Fecha y Hora seleccionada: {self.date_time_picker.dateTime().toString()}")
