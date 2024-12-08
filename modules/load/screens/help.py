import os
import mistune
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QLabel
from PySide6.QtCore import QUrl

class HelpScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Crear el QTextBrowser para mostrar el índice y el contenido
        self.text_browser = QTextBrowser(self)
        layout.addWidget(self.text_browser)

        # Cargar el índice de los módulos al principio
        self.load_index()

    def load_index(self):
        """Genera y carga el índice de los módulos."""
        modules = {
            "Análisis": "analysis_help.md",
            "Configuración": "settings_help.md",
            "Otra Pantalla": "another_screen_help.md"
        }

        # Crear un índice con enlaces a los archivos help.md
        index_html = "<h3>Índice de módulos:</h3><ul>"
        for module_name, file_name in modules.items():
            index_html += f'<li><a href="{file_name}">{module_name}</a></li>'
        index_html += "</ul>"

        # Establecer el HTML con el índice
        self.text_browser.setHtml(index_html)

        # Conectar la señal de clic en el ancla
        self.text_browser.anchorClicked.connect(self.handle_anchor_clicked)

    def load_help_file(self, file_name):
        """Carga el archivo help.md correspondiente al módulo seleccionado."""
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                markdown_content = file.read()
                html_content = mistune.create_markdown()(markdown_content)
                styled_html = f"""
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
                    {html_content}
                </body>
                </html>
                """
                self.text_browser.setHtml(styled_html)
        except FileNotFoundError:
            self.text_browser.setText(f"Archivo de ayuda {file_name} no encontrado.")
        except Exception as e:
            self.text_browser.setText(f"Error al cargar el archivo: {e}")

    def handle_anchor_clicked(self, url: QUrl):
        """Maneja el clic en el índice y carga el archivo help.md correspondiente."""
        file_name = url.toString()  # Obtener el nombre del archivo al que se hace clic
        self.load_help_file(file_name)

