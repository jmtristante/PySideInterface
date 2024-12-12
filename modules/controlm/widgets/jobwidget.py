from datetime import datetime

from modules.controlm.classes.job import Job
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, \
    QGraphicsTextItem, QGraphicsItem, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QPen, QColor, QFont, QAction


class JobWidget(QGraphicsRectItem):
    def __init__(self, x, y, job, parent=None):
        width = 200
        height = 120
        super().__init__(x, y, width, height)

        self.job = job


        # Cambiar el color del borde a gris
        self.setBrush(Qt.white)
        self.default_pen = QPen(QColor("gray"))  # Guardar el color predeterminado del borde
        self.clicked_pen = QPen(QColor("blue"), 4)  # Color azul más grueso para el borde
        self.setPen(self.default_pen)
        self.setZValue(1)

        # Habilitar enfoque en el widget
        self.setFlag(QGraphicsItem.ItemIsFocusable)

        self.job_name = job.name
        self.status = job.status
        self.start_date = job.start_date.strftime("%m/%d/%Y, %H:%M:%S") if job.start_date else ''
        self.end_date = job.end_date.strftime("%m/%d/%Y, %H:%M:%S") if job.end_date else ''

        # Añadir el texto del nombre del trabajo con color gris
        self.name_item = QGraphicsTextItem(self.job_name, parent=self)
        self.name_item.setDefaultTextColor(QColor("black"))  # Texto negro
        font = QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.name_item.setFont(font)
        self.name_item.setPos(x + 10, y + 5)

        # Divisiones: 40-20-40 sobre la altura
        first_section_height = height * 0.40
        second_section_height = height * 0.25
        third_section_height = height * 0.35

        # Añadir la primera línea divisoria con más grosor
        self.dividing_line = QGraphicsRectItem(x, y + first_section_height, width, 5,
                                               parent=self)  # Grosor aumentado a 5
        self.dividing_line.setBrush(self.get_status_color())
        self.dividing_line.setPen(Qt.NoPen)
        self.dividing_line.setZValue(-999)

        # Espacio vacío (segundo tercio 20%)
        self.empty_section = QGraphicsRectItem(x, y + first_section_height + 5, width, second_section_height,
                                               parent=self)
        self.empty_section.setBrush(Qt.transparent)  # Espacio vacío
        self.empty_section.setPen(Qt.NoPen)

        # Añadir la segunda línea divisoria (delgada y gris)
        self.second_line = QGraphicsRectItem(x, y + first_section_height + second_section_height, width, 1, parent=self)
        self.second_line.setBrush(QColor("gray"))
        self.second_line.setPen(Qt.NoPen)

        # Añadir las horas de inicio con texto gris
        self.start_item = QGraphicsTextItem(f"Start", parent=self)
        self.start_item.setDefaultTextColor(QColor("darkGray"))  # Texto gris
        self.start_item.setFont(QFont("Arial", 9))
        self.start_item.setPos(x + 10, y + first_section_height + second_section_height + 5)

        self.start_time_item = QGraphicsTextItem(self.start_date, parent=self)
        self.start_time_item.setDefaultTextColor(QColor("gray"))  # Texto gris
        self.start_time_item.setFont(QFont("Arial", 9))
        time_rect = self.start_time_item.boundingRect()
        self.start_time_item.setPos(x + width - time_rect.width() - 10,
                                    y + first_section_height + second_section_height + 5)

        # Añadir las horas de fin con texto gris
        self.end_item = QGraphicsTextItem(f"End", parent=self)
        self.end_item.setDefaultTextColor(QColor("darkGray"))  # Texto gris
        self.end_item.setFont(QFont("Arial", 9))
        self.end_item.setPos(x + 10,
                             y + first_section_height + second_section_height + 20)  # Ajuste de posición

        self.end_time_item = QGraphicsTextItem(self.end_date, parent=self)
        self.end_time_item.setDefaultTextColor(QColor("gray"))  # Texto gris
        self.end_time_item.setFont(QFont("Arial", 9))
        end_rect = self.end_time_item.boundingRect()
        self.end_time_item.setPos(x + width - end_rect.width() - 10,
                                  y + first_section_height + second_section_height + 20)

    def get_status_color(self):
        """Retornar el color asociado con el estado del trabajo."""
        status_colors = {
            "complete": QColor("green"),
            "running": QColor("yellow"),
            "failed": QColor("red"),
            "waiting": QColor("gray")
        }
        return status_colors.get(self.status, QColor("black"))

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            print(f"Left click on job: {self.job_name}")
            self.setPen(self.clicked_pen)  # Cambiar el borde a azul
            self.setFocus()  # Establecer el enfoque en el widget



    def focusOutEvent(self, event):
        """Eliminar el borde azul al perder el foco."""
        print(f"Focus lost on job: {self.job_name}")
        self.setPen(self.default_pen)  # Restaurar el borde al color gris
        super().focusOutEvent(event)

    def contextMenuEvent(self, event):
        """Mostrar el menú al hacer clic derecho."""
        menu = QMenu(self.parentItem())  # O usar self.scene() si lo prefieres

        action1 = QAction('Acción 1', self.parentItem())
        action2 = QAction('Acción 2', self.parentItem())
        action_ok = QAction('Poner a OK', self.parentItem())  # Nueva acción para poner a OK

        # Conectar las acciones a sus métodos

        action_ok.triggered.connect(self.set_job_complete)  # Conectamos la acción "Poner a OK"

        # Añadir las acciones al menú
        menu.addAction(action1)
        menu.addAction(action2)
        menu.addAction(action_ok)  # Añadimos la opción "Poner a OK"

        # Ejecutar el menú
        menu.exec(event.screenPos())

    def set_job_complete(self):
        """Cambiar el estado del Job a 'complete'."""
        self.job.set_status("complete")  # Cambiamos el estado del Job
        print(f"Estado del Job '{self.job.name}' cambiado a 'complete'")

        # Actualizar la visualización del job
        self.update_job_info()  # Ahora se llama a este método para actualizar el widget

    def update_job_info(self):
        """Actualizar la información mostrada en el JobWidget."""
        self.job_name = self.job.name
        self.status = self.job.status
        self.start_date = self.job.start_date.strftime("%m/%d/%Y, %H:%M:%S") if self.job.start_date else ''
        self.end_date = self.job.end_date.strftime("%m/%d/%Y, %H:%M:%S") if self.job.end_date else ''

        # Actualizar los textos
        self.name_item.setPlainText(self.job_name)
        self.start_time_item.setPlainText(self.start_date)
        self.end_time_item.setPlainText(self.end_date)

        # Actualizar el color de la barra de estado
        self.dividing_line.setBrush(self.get_status_color())
        self.scene().update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Job Viewer")

        # Crear una escena de gráficos y vista
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        # Create a new job
        job = Job(name="Data Extraction")

        # Set start date
        job.set_start_date(datetime.now())

        # Update status to Running
        job.set_status("running")

        # Añadir un JobWidget a la escena
        job_widget = JobWidget(50, 50, job)
        self.scene.addItem(job_widget)

        # Create a new job
        job2 = Job(name="ICIRITA001D")

        # Set start date
        job2.set_start_date(datetime.now())

        # Update status to Running
        job2.set_status("failed")

        # Añadir un JobWidget a la escena
        job_widget2 = JobWidget(450, 50, job2)
        self.scene.addItem(job_widget2)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()






