from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem, QVBoxLayout, QWidget, \
    QApplication, QDockWidget, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from modules.controlm.widgets.jobwidget import JobWidget  # Asegúrate de que tienes la clase JobWidget
from modules.controlm.classes.job import Job


class ActiveScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplicación de Gestión de Jobs")

        # Crear la escena y la vista de la escena
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        # Crear un panel a la derecha para mostrar la información del Job
        self.right_panel = QDockWidget("Detalles del Job", self)
        self.right_panel.setAllowedAreas(Qt.RightDockWidgetArea)
        self.right_panel.setWidget(QWidget())  # Placeholder
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_panel)

        # Crear un layout para el panel de la derecha
        self.panel_layout = QVBoxLayout(self.right_panel.widget())
        self.info_label = QLabel("Seleccione un Job para ver la información", self.right_panel.widget())
        self.panel_layout.addWidget(self.info_label)

        # Crear un JobWidget para demostrar
        job = Job("Data Extraction")  # Asegúrate de que tienes una clase Job
        job.set_status("running")
        job_widget = JobWidget(50, 50, job)

        # Añadir el JobWidget a la escena
        self.scene.addItem(job_widget)

        # Crear otro JobWidget para demostrar
        job2 = Job("ICIRITA001D")  # Otro Job
        job2.set_status("failed")
        job_widget2 = JobWidget(550, 50, job2)
        self.scene.addItem(job_widget2)

        # Conectar la señal job_selected con el método update_info_panel
        job_widget.signal_emitter.job_selected.connect(self.update_info_panel)
        job_widget2.signal_emitter.job_selected.connect(self.update_info_panel)

    def update_info_panel(self, job):
        """Actualizar la información en el panel derecho cuando se seleccione un job"""
        job_info = f"Job Name: {job.name}\nStatus: {job.status}\nStart Date: {job.start_date}\nEnd Date: {job.end_date}"
        self.info_label.setText(job_info)


if __name__ == "__main__":
    app = QApplication([])

    window = ActiveScreen()
    window.show()

    app.exec()
