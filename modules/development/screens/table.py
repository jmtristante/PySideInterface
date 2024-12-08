from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton


class TableScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabla de Datos")

        layout = QVBoxLayout(self)

        # Crear una tabla
        self.table = QTableWidget(self)
        self.table.setRowCount(5)  # Filas
        self.table.setColumnCount(3)  # Columnas
        self.table.setHorizontalHeaderLabels(["Nombre", "Edad", "Ciudad"])

        # Poner datos de ejemplo en la tabla
        data = [
            ("Juan", 30, "Madrid"),
            ("Ana", 25, "Barcelona"),
            ("Pedro", 35, "Sevilla"),
            ("Luis", 28, "Valencia"),
            ("Carlos", 40, "Bilbao")
        ]

        for row, (name, age, city) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(str(age)))
            self.table.setItem(row, 2, QTableWidgetItem(city))

        # Crear un botón para mostrar los datos de la tabla
        self.button = QPushButton("Mostrar Datos", self)
        self.button.clicked.connect(self.show_data)

        layout.addWidget(self.table)
        layout.addWidget(self.button)

    def show_data(self):
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            print(row_data)

