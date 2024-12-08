import os
import mistune
import yaml
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QPushButton
from PySide6.QtCore import QUrl


class HelpScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Crear el QTextBrowser para mostrar el índice y el contenido
        self.text_browser = QTextBrowser(self)

        # Crear el botón de "Volver al índice"
        self.back_button = QPushButton("Volver al índice", self)
        self.back_button.setVisible(False)  # Inicialmente no visible
        self.back_button.clicked.connect(self.show_index)

        # Layout para mostrar el índice y el contenido
        layout.addWidget(self.text_browser)
        layout.addWidget(self.back_button)

        # Cargar el contenido de help.md principal y luego cargar el índice
        self.load_help_and_index()

    def load_help_and_index(self):
        """Carga primero el contenido de help.md y luego el índice de los módulos."""

        # Cargar el contenido del archivo help.md principal
        help_file_path = "help.md"
        main_help_content = self.load_help_file(help_file_path)

        # Leer el archivo YAML para obtener los módulos
        try:
            with open("menu_config.yaml", "r", encoding="utf-8") as file:
                menu_data = yaml.safe_load(file)

            # Crear un índice con enlaces a los archivos help.md
            index_html = "<h3>Índice de módulos:</h3><ul>"
            for item in menu_data.get("menu", []):
                module_name = item["category"]
                module_folder = item["screen"].split(".")[1]  # Utiliza el nombre del módulo
                help_file = f"modules/{module_folder}/help.md"  # Ruta del archivo help.md
                index_html += f'<li><a href="{help_file}">{module_name}</a></li>'
            index_html += "</ul>"

            # Concatenar primero el contenido de help.md principal, luego el índice
            full_html_content = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        margin: 20px;
                    }}
                    h1, h2, h3 {{
                        color: #2C3E50;
                        margin-top: 20px;
                    }}
                    ul {{
                        margin: 10px 0;
                        padding-left: 20px;
                    }}
                    li {{
                        margin-bottom: 5px;
                    }}
                    a {{
                        color: #16A085;
                        text-decoration: none;
                    }}
                    a:hover {{
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                {main_help_content}
                {index_html}
            </body>
            </html>
            """
            self.text_browser.setHtml(full_html_content)

            # Conectar la señal de clic en el ancla
            self.text_browser.anchorClicked.connect(self.handle_anchor_clicked)

            # Asegurar que el botón "Volver al índice" no esté visible al mostrar el índice
            self.back_button.setVisible(False)

        except FileNotFoundError:
            self.text_browser.setText("Archivo menu.yaml no encontrado.")
        except Exception as e:
            self.text_browser.setText(f"Error al cargar el índice: {e}")

    def load_help_file(self, file_name):
        """Carga el archivo help.md principal o el específico del módulo."""
        try:
            # Intentamos abrir el archivo help.md correspondiente
            if not os.path.exists(file_name):
                raise FileNotFoundError(f"El archivo {file_name} no se encuentra.")

            with open(file_name, "r", encoding="utf-8") as file:
                markdown_content = file.read()
                html_content = mistune.create_markdown()(markdown_content)
                return html_content

        except FileNotFoundError:
            return f"Error: El archivo {file_name} no se encontró."
        except Exception as e:
            return f"Error al cargar el archivo de ayuda: {e}"

    def handle_anchor_clicked(self, url: QUrl):
        """Maneja el clic en el índice y carga el archivo help.md correspondiente."""
        file_name = url.toString()  # Obtener el nombre del archivo al que se hace clic
        self.load_help_file(file_name)

        # Mostrar el botón "Volver al índice" cuando se hace clic en un enlace
        self.back_button.setVisible(True)

    def show_index(self):
        """Muestra el índice de módulos y oculta el botón 'Volver al índice'."""
        self.load_help_and_index()

        # Asegurarse de que el botón "Volver al índice" esté oculto cuando se muestra el índice
        self.back_button.setVisible(False)
