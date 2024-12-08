from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QToolButton, QSizePolicy, QFrame, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QFile
import yaml
import importlib

from styles.styles import load_styles


class ModernInterface(QMainWindow):
    def __init__(self, menu_config):
        super().__init__()
        self.setWindowTitle("Interfaz Moderna con Menú Retráctil")
        self.setMinimumSize(800, 600)

        self.menu_config = menu_config
        self.menu_expanded = True
        self.active_button_index = -1  # Inicialmente no hay botón activo

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Menú lateral
        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_widget)
        self.menu_layout.setContentsMargins(10, 0, 0, 0)  # Agregar margen a la izquierda
        self.menu_layout.setSpacing(10)

        # Botón de colapso
        self.toggle_button = QPushButton("⮜")
        self.toggle_button.setFixedSize(40, 40)
        self.toggle_button.clicked.connect(self.toggle_menu)
        self.toggle_button.setStyleSheet(load_styles("styles\menu_button.qss"))
        self.menu_layout.addWidget(self.toggle_button, alignment=Qt.AlignLeft)

        # Botones dinámicos
        self.menu_buttons = []
        for i, item in enumerate(self.menu_config):
            button = QToolButton()
            button.setIcon(QIcon(item["icon"]))
            button.setText(item["category"])
            button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setFixedHeight(50)
            button.clicked.connect(lambda _, i=i: self.change_screen(i))
            button.setStyleSheet(load_styles("styles\menu_button.qss"))
            self.menu_buttons.append(button)
            self.menu_layout.addWidget(button)

        # Agregar un espacio invisible para empujar los botones de "Ayuda" y "Configuración" hacia abajo
        self.menu_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botones fijos
        self.add_fixed_button("Ayuda", "icons/help.png", self.change_screen_to_help)
        self.add_fixed_button("Configuración", "icons/settings.png", self.change_screen_to_settings)

        # Separador
        self.menu_separator = QFrame()
        self.menu_separator.setFrameShape(QFrame.VLine)
        self.menu_separator.setFrameShadow(QFrame.Sunken)

        # Contenedor para pantallas
        self.screen_container = QStackedWidget()

        # Cargar pantallas definidas en el YAML
        for item in self.menu_config:
            module_name = item["screen"]
            try:
                module = importlib.import_module(module_name)
                screen_class = getattr(module, f"{module_name.split('.')[-1].capitalize()}Screen")
                self.screen_container.addWidget(screen_class())
            except Exception as e:
                print(f"Error al cargar el módulo {module_name}: {e}")

        # Cargar las pantallas fijas de Ayuda y Configuración
        from screens import help, settings
        self.help_screen = help.HelpScreen()
        self.settings_screen = settings.SettingsScreen()

        # Agregar las pantallas fijas al QStackedWidget
        self.screen_container.addWidget(self.help_screen)
        self.screen_container.addWidget(self.settings_screen)

        # Establecer pantalla por defecto
        self.screen_container.setCurrentIndex(0)

        main_layout.addWidget(self.menu_widget)
        main_layout.addWidget(self.menu_separator)
        main_layout.addWidget(self.screen_container)

        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 0)
        main_layout.setStretch(2, 5)

        self.setCentralWidget(main_widget)
        self.update_menu_layout()

    def add_fixed_button(self, text, icon_path, callback):
        """Agrega un botón fijo al final del menú."""
        button = QToolButton()
        button.setIcon(QIcon(icon_path))
        button.setText(text)
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button.setFixedHeight(50)
        button.clicked.connect(callback)
        button.setStyleSheet(load_styles("styles\menu_button.qss"))
        self.menu_layout.addWidget(button, alignment=Qt.AlignBottom)
        self.menu_buttons.append(button)

    def toggle_menu(self):
        self.menu_expanded = not self.menu_expanded
        self.update_menu_layout()

    def update_menu_layout(self):
        """Actualiza el diseño del menú."""
        if self.menu_expanded:
            self.menu_widget.setFixedWidth(200)
            self.toggle_button.setText("⮜")
            for button in self.menu_buttons:
                button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        else:
            self.menu_widget.setFixedWidth(60)
            self.toggle_button.setText("⮞")
            for button in self.menu_buttons:
                button.setToolButtonStyle(Qt.ToolButtonIconOnly)

    def change_screen(self, index):
        """Cambia a la pantalla correspondiente."""
        # Actualizamos el índice de los botones especiales
        if index == "help":
            index = len(self.menu_buttons) - 2
        if index == "settings":
            index = len(self.menu_buttons) - 1

        # Primero, restablecer el estilo de todos los botones
        for i, button in enumerate(self.menu_buttons):
            if i == index:
                button.setStyleSheet(load_styles("styles\menu_button_active.qss"))
            else:
                button.setStyleSheet(load_styles("styles\menu_button.qss"))

        try:
            self.screen_container.setCurrentIndex(index)
        except ValueError:
            print(f"Error: No se encontró la pantalla {index}")

    def change_screen_to_help(self):
        """Cambia a la pantalla de ayuda."""
        self.change_screen("help")

    def change_screen_to_settings(self):
        """Cambia a la pantalla de configuración."""
        self.change_screen("settings")


if __name__ == "__main__":
    import sys

    # Leer configuración del menú desde un archivo YAML
    with open("menu_config.yaml", "r", encoding="utf-8") as yaml_file:
        config = yaml.safe_load(yaml_file)["menu"]

    app = QApplication(sys.argv)

    # Preprocesar y aplicar estilos
    app.setStyleSheet(load_styles("styles\styles.qss"))


    window = ModernInterface(config)
    window.change_screen(0) # Mostramos la primera pantalla al arrancar
    window.show()
    sys.exit(app.exec())
