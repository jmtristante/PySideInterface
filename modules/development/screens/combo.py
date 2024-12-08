from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel


class ComboBoxScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ComboBox")

        layout = QVBoxLayout(self)

        # Crear un combo box
        self.combo_box = QComboBox(self)
        self.combo_box.addItem("Selecciona una opción")
        self.combo_box.addItem("Opción A")
        self.combo_box.addItem("Opción B")
        self.combo_box.addItem("Opción C")

        # Crear un botón
        self.button = QPushButton("Mostrar Opción Seleccionada", self)
        self.button.clicked.connect(self.show_selected_option)

        # Crear una etiqueta
        self.label = QLabel("Selecciona una opción del ComboBox", self)

        layout.addWidget(self.combo_box)
        layout.addWidget(self.button)
        layout.addWidget(self.label)

    def show_selected_option(self):
        selected_option = self.combo_box.currentText()
        self.label.setText(f"Seleccionaste: {selected_option}")

