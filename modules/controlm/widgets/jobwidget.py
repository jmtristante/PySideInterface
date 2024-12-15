from datetime import datetime

from modules.controlm.classes.job import Job
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, \
    QGraphicsTextItem, QGraphicsItem, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QPen, QColor, QFont, QAction
from PySide6.QtCore import Signal, QObject, QRectF

class JobSignalEmitter(QObject):
    job_selected = Signal(Job)  # Señal que emite un Job

class JobWidget(QGraphicsItem):
    # Definir la señal correctamente

    job_selected = Signal(Job)

    def __init__(self, x, y, job, parent=None):
        super().__init__(parent)
        self.job = job
        self.rect = QRectF(x, y, 200, 120)  # Dimensiones del widget
        self.job_name = job.name
        self.status = job.status
        self.start_date = job.start_date.strftime("%m/%d/%Y, %H:%M:%S") if job.start_date else ''
        self.end_date = job.end_date.strftime("%m/%d/%Y, %H:%M:%S") if job.end_date else ''
        self.default_pen = QPen(QColor("gray"))
        self.clicked_pen = QPen(QColor("blue"), 4)
        self.focused = False
        self.signal_emitter = JobSignalEmitter()
        # Habilitar que este item pueda recibir foco
        self.setFlag(QGraphicsItem.ItemIsFocusable)

        # Borde como un QGraphicsRectItem
        self.border_item = QGraphicsRectItem(self.rect, self)
        self.border_item.setPen(self.default_pen)
        self.border_item.setZValue(10)  # Asegurar que el borde esté siempre por encima (z-value alto)

    def boundingRect(self):
        """Define los límites del JobWidget."""
        return self.rect

    def paint(self, painter, option, widget=None):
        """Dibuja el JobWidget."""
        # Cambiar el borde según el estado de enfoque
        if self.focused:
            self.border_item.setPen(self.clicked_pen)
        else:
            self.border_item.setPen(self.default_pen)

        # Dibujar el borde sobre el JobWidget
        self.border_item.setRect(self.rect)

        painter.setPen(self.default_pen)
        painter.setBrush(Qt.white)
        painter.drawRect(self.rect)

        # Dibujar el texto del nombre del job
        painter.setPen(QColor("black"))
        font = QFont()
        font.setBold(True)
        font.setPointSize(15)
        painter.setFont(font)
        painter.drawText(self.rect.adjusted(10, 5, -10, 0), Qt.AlignLeft, self.job_name)

        # Dibujar la barra de estado
        status_color = self.get_status_color()
        painter.setBrush(status_color)
        painter.setPen(Qt.NoPen)
        bar_rect = QRectF(self.rect.x(), self.rect.y() + self.rect.height() * 0.35, self.rect.width(), 5)
        painter.drawRect(bar_rect)

        # Dibujar la barra de separacion
        status_color = self.get_status_color()
        painter.setBrush(QColor("darkGray"))
        painter.setPen(Qt.NoPen)
        line_rect = QRectF(self.rect.x(), self.rect.y() + self.rect.height() * 0.6, self.rect.width(), 1)
        painter.drawRect(line_rect)

        # Dibujar los textos de horas
        painter.setPen(QColor("darkGray"))
        painter.setFont(QFont("Arial", 9))
        painter.drawText(self.rect.adjusted(10, 80, -10, 0), Qt.AlignLeft, f"Start:")
        painter.drawText(self.rect.adjusted(10, 100, -10, 0), Qt.AlignLeft, f"End:")

        # Dibujar las horas de inicio y fin
        painter.setPen(QColor("gray"))
        painter.setFont(QFont("Arial", 9))
        painter.drawText(self.rect.adjusted(70, 80, -10, 0), Qt.AlignLeft, f"{self.start_date}")
        painter.drawText(self.rect.adjusted(70, 100, -10, 0), Qt.AlignLeft, f"{self.end_date}")

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
        #print(f"Left click on job: {self.job_name}")
        #self.setPen(self.clicked_pen)  # Cambiar el borde a azul
        #self.signal_emitter.job_selected.emit(self.job)  # Emitir la señal
        #self.setFocus()  # Establecer el enfoque en el widget

        super().mousePressEvent(event)

    def focusInEvent(self, event):
        print(f"Focus on job: {self.job_name}")
        self.focused = True
        self.signal_emitter.job_selected.emit(self.job)
        self.update()  # Redibujar para reflejar el cambio de borde


    def focusOutEvent(self, event):
        """Eliminar el borde azul al perder el foco."""
        print(f"Focus lost on job: {self.job_name}")
#        self.setPen(self.default_pen)  # Restaurar el borde al color gris
        self.focused = False
        self.update()  # Redibujar para reflejar el cambio de borde
        super().focusOutEvent(event)

    def contextMenuEvent(self, event):
        """Mostrar el menú al hacer clic derecho."""
        menu = QMenu(self.parentItem())  # O usar self.scene() si lo prefieres

        action1 = QAction('Acción 1')
        action2 = QAction('Acción 2')
        action_ok = QAction('Poner a OK')  # Nueva acción para poner a OK

        action_ok.triggered.connect(self.set_job_complete)  # Conectamos la acción "Poner a OK"

        # Añadir las acciones al menú
        menu.addAction(action1)
        menu.addAction(action2)
        menu.addAction(action_ok)  # Añadimos la opción "Poner a OK"

        # Ejecutar el menú
        menu.exec(event.screenPos())

        # Actualizamos la escena
        self.scene().update()

    def set_job_complete(self):
        """Cambiar el estado del Job a 'complete'."""
        self.job.set_status("complete")  # Cambiamos el estado del Job
        self.job.set_end_date(datetime.now())
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
        #self.name_item.setPlainText(self.job_name)
        #self.start_time_item.setPlainText(self.start_date)
        #self.end_time_item.setPlainText(self.end_date)

        # Actualizar el color de la barra de estado
        #self.dividing_line.setBrush(self.get_status_color())
        self.update()

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
