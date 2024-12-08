import yaml
import importlib
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PySide6.QtGui import QIcon
from functools import partial

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton
from functools import partial
from PySide6.QtCore import QSize

import math

from utils.layout.responsive_layout import ResponsiveGrid


def get_icon(icon_name):
    icon = QIcon('icons/' + icon_name)
    if icon.isNull():
        print(f"Icono no cargado correctamente")
    else:
        return icon


# Función que cambia el nombre de la pestaña
def update_tab_name(tab_widget, tab_index, new_name):
    """
    Actualiza el nombre de la pestaña (tab) en el QTabWidget.

    :param tab_widget: El widget que contiene las pestañas.
    :param tab_index: El índice de la pestaña que se va a actualizar.
    :param new_name: El nuevo nombre que tendrá la pestaña.
    """
    tab_widget.setTabText(tab_index, new_name)


def load_screen_config(file_path="screens.yaml"):
    """
    Carga la configuración de pantallas desde un archivo YAML.
    Devuelve un diccionario que refleja la jerarquía de categorías y subcategorías.
    """
    try:
        with open(file_path, "r") as config_file:
            categories=yaml.safe_load(config_file)
            if not isinstance(categories, dict):
                raise ValueError("1- La configuración cargada no es válida. Verifica el archivo screens.yaml.")
            return categories
    except FileNotFoundError:
        print(f"El archivo de configuración {file_path} no se encontró.")
        return {}

def create_tab_content(tab, config_path="screens.yaml"):
    """
    Crea y devuelve un widget inicial con botones para las categorías.
    """
    content = QWidget()
    layout = QGridLayout(content)

    # Cargar configuración de categorías
    categories = load_screen_config(config_path)



    buttons=[]
    # Crear botones para las categorías
    for category in categories.keys():
        button = QPushButton(category)
        button.clicked.connect(lambda _, c=category, d=categories[category]: show_category(tab, c, d))
        buttons.append(button)


    content2=ResponsiveGrid(buttons)

    return content2



def show_category(tab, category, content):
    """
    Muestra las pantallas disponibles en la categoría seleccionada en la pestaña,
    con iconos de categorías y subcategorías.
    """
    # Limpiar el contenido actual de la pestaña
    layout = tab.layout()
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        if widget is not None:
            widget.deleteLater()

    buttons=[] #Array de botones para mostrar

    # Verificar si la categoría tiene subcategorías
    if isinstance(content, dict):
        # Crear botones para las subcategorías con icono de carpeta
        for subcategory, subcategory_screens in content.items():
            subcategory_button = QPushButton(subcategory)
            # Asignar el icono de una carpeta a los botones de subcategorías
            icon = get_icon('folder_icon')
            subcategory_button.setIcon(icon)
            subcategory_button.setIconSize(QSize(20, 20))  # Establecer el tamaño del icono
            # Conectar el botón con el evento de mostrar las pantallas de la subcategoría
            subcategory_button.clicked.connect(partial(show_category, tab, subcategory, subcategory_screens))
            buttons.append(subcategory_button)

    elif isinstance(content, list):
        # Crear botones para las pantallas dentro de la categoría con icono personalizado
        for screen in content:
            screen_button = QPushButton(screen['name'])
            # Asignar el icono personalizado a cada botón de pantalla, si está definido en el YAML
            if 'icon' in screen:
                icon = get_icon(screen['icon'])
                screen_button.setIcon(icon)
                screen_button.setIconSize(QSize(20, 20))  # Establecer el tamaño del icono
            # Llamar a switch_to_screen con el módulo correspondiente
            screen_button.clicked.connect(partial(switch_to_screen, tab, screen['module']))
            buttons.append(screen_button)

    layout.addWidget(ResponsiveGrid(buttons))
    # Asegúrate de que el contenido esté visible después de actualizar
    tab.setLayout(layout)






def reset_tab_content(tab):
    """
    Restablece el contenido de la pestaña a la vista de categorías principales.
    """
    for i in reversed(range(tab.layout().count())):
        tab.layout().itemAt(i).widget().deleteLater()
    tab.layout().addWidget(create_tab_content(tab))

def switch_to_screen(tab, module_path):
    """
    Cambia el contenido de la pestaña a la pantalla seleccionada.
    """
    try:
        module = importlib.import_module(module_path)
        screen_class = getattr(module, [cls for cls in dir(module) if cls.endswith("Screen")][0])
        screen_instance = screen_class()
    except (ImportError, AttributeError, IndexError) as e:
        print(f"Error al cargar el módulo {module_path}: {e}")
        return

    # Reemplazar el contenido de la pestaña
    for i in reversed(range(tab.layout().count())):
        tab.layout().itemAt(i).widget().deleteLater()
    tab.layout().addWidget(screen_instance)
