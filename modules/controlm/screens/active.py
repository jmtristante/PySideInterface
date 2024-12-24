from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem, QVBoxLayout, QWidget, \
    QApplication, QDockWidget, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QStackedWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from modules.controlm.widgets.jobwidget import JobWidget  # Asegúrate de que tienes la clase JobWidget
#from modules.controlm.classes.job import Job
from modules.controlm.classes.pruebas import Activo
from modules.controlm.classes.pruebas import Job
from modules.controlm.classes.pruebas import Condition


class ActiveScreen(QMainWindow):
    # def __init__(self):
    #     super().__init__()
    #     self.setWindowTitle("Pantalla Activo")
    #
    #     # Creamos el QStackedWidget
    #     self.stacked_widget = QStackedWidget()
    #     self.setCentralWidget(self.stacked_widget)
    #
    #     # Creamos las pantallas
    #     self.screen_principal = QWidget()
    #     self.screen_opciones = QWidget()
    #
    #     # Inicializamos el Activo
    #     self.activo = None
    #     self.activo_iniciado = False
    #
    #     # Pantalla Principal (con el botón de "Levantar Activo")
    #     self.init_screen_principal()
    #
    #     # Pantalla de Opciones (cuando el activo está levantado)
    #     self.init_screen_opciones()
    #
    #     # Inicializamos el QStackedWidget
    #     self.stacked_widget.addWidget(self.screen_principal)
    #     self.stacked_widget.addWidget(self.screen_opciones)

    def inicializar_jobs(self):
        cond1 = Condition("condicion1", "AND")
        cond2 = Condition("condicion2", "OR")

        job1 = Job("Job1", [cond1, cond2], [Condition("condicion3")], self.activo)
        job2 = Job("Job2", [Condition("condicion3")], [], self.activo)

        # Agregar los jobs al Activo, se inician automáticamente
        self.activo.agregar_job(job1)
        self.activo.agregar_job(job2)

        self.activo.agregar_condicion("condicion1")
        import time
        time.sleep(1)
        self.activo.agregar_condicion("condicion2")

    def init_screen_principal(self):
        """Configura la pantalla principal con el botón de "Levantar Activo"."""
        layout = QVBoxLayout(self.screen_principal)
        self.btn_levantar_activo = QPushButton("Levantar Activo")
        self.btn_levantar_activo.clicked.connect(self.levantar_activo)
        layout.addWidget(self.btn_levantar_activo, alignment=Qt.AlignCenter)

    def init_screen_opciones(self):
        """Configura la pantalla de opciones cuando el activo está levantado."""
        layout = QVBoxLayout(self.screen_opciones)

        # Botones para las opciones de trabajo
        self.btn_agregar_job = QPushButton("Agregar Job")
        self.btn_agregar_job.clicked.connect(self.agregar_job)
        layout.addWidget(self.btn_agregar_job, alignment=Qt.AlignCenter)

        self.btn_visualizar_jobs = QPushButton("Visualizar Jobs")
        self.btn_visualizar_jobs.clicked.connect(self.visualizar_jobs)
        layout.addWidget(self.btn_visualizar_jobs, alignment=Qt.AlignCenter)

        self.btn_apagar_activo = QPushButton("Apagar Activo")
        self.btn_apagar_activo.clicked.connect(self.apagar_activo)
        layout.addWidget(self.btn_apagar_activo, alignment=Qt.AlignCenter)

    def levantar_activo(self):
        """Levanta el activo y cambia la pantalla a las opciones."""
        if not self.activo_iniciado:
            self.activo = Activo()
            self.activo.start()
            self.activo_iniciado = True
            print("El activo se ha lanzado")

            # Cambiar la pantalla al widget de opciones
            self.stacked_widget.setCurrentWidget(self.screen_opciones)
            self.inicializar_jobs()

    def apagar_activo(self):
        """Apaga el activo y vuelve a la pantalla principal."""
        if self.activo_iniciado:
            self.activo.detener()
            self.activo.join()
            self.activo_iniciado = False
            print("El activo se ha detenido")

            # Volver a la pantalla principal
            self.stacked_widget.setCurrentWidget(self.screen_principal)

    def agregar_job(self):
        """Agrega un nuevo job dinámicamente."""
        cond1 = Condition("condicion1", "AND")
        cond2 = Condition("condicion2", "OR")
        new_job = Job(f"Job{len(self.activo.jobs) + 1}", [cond1, cond2], [], self.activo)
        new_job.start()
        self.activo.agregar_job(new_job)
        print(f"Nuevo Job agregado: {new_job.name}")

    def visualizar_jobs(self):
        """Muestra los jobs activos en una tabla."""
        self.job_table = QTableWidget()
        self.job_table.setColumnCount(1)
        self.job_table.setHorizontalHeaderLabels(["Nombre del Job"])
        self.job_table.setRowCount(len(self.activo.jobs))

        for i, job in enumerate(self.activo.jobs):
            self.job_table.setItem(i, 0, QTableWidgetItem(job.name))

        self.screen_opciones.layout().addWidget(self.job_table)

    def closeEvent(self, event):
        """Sobrescribe el evento de cierre de la ventana."""
        print("Cerrando ventana...")
        if self.activo_iniciado:
            self.activo.detener()
            self.activo.join()
        print("Todos los hilos detenidos.")
        super().closeEvent(event)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación de Gestión de Jobs")
        self.activo = Activo()
        self.activo.start()

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
        job = Job("Data Extraction",[],[],self.activo)  # Asegúrate de que tienes una clase Job
        #job.set_status("running")
        job_widget = JobWidget(50, 50, job)

        # Añadir el JobWidget a la escena
        self.scene.addItem(job_widget)

        # Crear otro JobWidget para demostrar
        job2 = Job("ICIRITA001D",[],[],self.activo)  # Otro Job
        #job2.set_status("failed")
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
