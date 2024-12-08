from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser
from markdown2 import markdown  # Librería para convertir Markdown a HTML
import mistune

class HelpScreen(QWidget):
    def __init__(self, help_file="help.md"):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Texto renderizado con QTextBrowser
        self.text_browser = QTextBrowser()
        self.layout.addWidget(self.text_browser)

        # Cargar contenido del archivo Markdown
        self.load_markdown(help_file)

    def load_markdown(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                markdown_content = file.read()
                html_content = mistune.create_markdown()(markdown_content)  # Convertir a HTML
                self.text_browser.setHtml(html_content)  # Renderizar en el QTextBrowser
        except FileNotFoundError:
            self.text_browser.setText("Archivo de ayuda no encontrado.")
        except Exception as e:
            self.text_browser.setText(f"Error al cargar el archivo: {e}")

