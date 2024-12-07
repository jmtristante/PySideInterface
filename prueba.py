from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

# Función para mostrar botones con iconos
def show_category(tab, category, content):
    layout = QVBoxLayout()  # Crear un layout vertical para los botones
    for screen in content:
        screen_button = QPushButton(screen['name'])
        icon_path = screen.get('icon', '')  # Obtener la ruta del icono
        if icon_path:
            icon = QIcon(icon_path)
            if icon.isNull():
                print(f"Icono no cargado correctamente: {icon_path}")
            else:
                screen_button.setIcon(icon)
                screen_button.setIconSize(QSize(32, 32))  # Establecer el tamaño del icono
        screen_button.setText(screen['name'])
        layout.addWidget(screen_button)
    tab.setLayout(layout)

# Crear aplicación de ejemplo
app = QApplication([])

# Crear un QWidget para mostrar los botones
window = QWidget()
window.setWindowTitle('Categorías con Iconos')

# Datos de ejemplo, puedes cargar estos desde un YAML
category_data = [
    {'name': 'Análisis', 'icon': 'icons/analysis_icon.png'},
    {'name': 'Ejecuciones', 'icon': 'icons/execution_icon.png'},
]

# Llamar a la función show_category para agregar botones a la ventana
show_category(window, 'Pruebas', category_data)

# Mostrar la ventana
window.show()

# Iniciar la aplicación
app.exec()
