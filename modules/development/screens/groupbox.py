from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QRadioButton, QCheckBox, QLabel


class GroupBoxScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Group Box")

        layout = QVBoxLayout(self)

        # Crear un group box
        group_box = QGroupBox("Opciones de configuración", self)

        # Crear botones de radio dentro del group box
        radio_button_1 = QRadioButton("Opción A", self)
        radio_button_2 = QRadioButton("Opción B", self)

        # Crear un checkbox dentro del group box
        check_box = QCheckBox("Activar configuración", self)

        group_box_layout = QVBoxLayout()
        group_box_layout.addWidget(radio_button_1)
        group_box_layout.addWidget(radio_button_2)
        group_box_layout.addWidget(check_box)

        group_box.setLayout(group_box_layout)

        # Crear una etiqueta para mostrar la opción seleccionada
        self.label = QLabel("Selecciona una opción", self)

        layout.addWidget(group_box)
        layout.addWidget(self.label)
