from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
from PySide6.QtCore import Qt


class ResponsiveGrid(QWidget):
    def __init__(self, buttons, max_columns=5):
        """
        Crea un diseño responsivo para los botones dados.

        :param buttons: Lista de botones ya creados.
        :param max_columns: Número máximo de columnas permitidas.
        """
        super().__init__()
        self.buttons = buttons
        self.max_columns = max_columns
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)  # Espaciado entre botones
        self.setLayout(self.grid_layout)

        self.current_columns = None  # Número actual de columnas
        self.current_rows = None  # Número actual de filas

        # Agregar botones al layout inicial
        self.rearrange_buttons()

    def getLayout(self):
        return self.grid_layout

    def resizeEvent(self, event):
        """Reorganiza los botones cuando la ventana cambia de tamaño."""
        super().resizeEvent(event)
        self.rearrange_buttons()

    def rearrange_buttons(self):
        """Organiza los botones en un diseño responsivo."""
        # Calcular el número de columnas basado en el ancho de la ventana
        widget_width = self.width()
        button_width = 120  # Estimación del ancho de un botón + espaciado
        columns = max(1, min(self.max_columns, widget_width // button_width))
        rows = (len(self.buttons) + columns - 1) // columns

        # Verificar si las filas y columnas actuales ya son correctas
        if self.current_columns == columns and self.current_rows == rows:
            return  # No es necesario actualizar el layout

        # Actualizar el estado actual
        self.current_columns = columns
        self.current_rows = rows

        # Limpiar el layout existente
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        # Reagregar botones en la nueva disposición
        for index, button in enumerate(self.buttons):
            row = index // columns
            col = index % columns
            self.grid_layout.addWidget(button, row, col)


if __name__ == "__main__":
    app = QApplication([])

    # Crear algunos botones
    buttons = [QPushButton(f"Botón {i + 1}") for i in range(20)]

    # Crear la ventana con los botones
    window = ResponsiveGrid(buttons)
    window.resize(800, 600)
    window.show()

    app.exec()
