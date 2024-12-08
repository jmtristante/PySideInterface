from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class AnalysisScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.label2 = QLabel("Ventana de analysis")
        self.layout.addWidget(self.label2)

        # Etiqueta para mostrar el tiempo transcurrido
        self.label = QLabel("Tiempo transcurrido: 0")
        self.layout.addWidget(self.label)

        # Botón para ejecutar la tarea
        self.button = QPushButton("Ejecutar")
        self.button.clicked.connect(self.start_task)
        self.layout.addWidget(self.button)

        # Hilo del trabajador inicializado como None
        self.worker_thread = None

    def start_task(self):
        self.button.setEnabled(False)  # Deshabilita el botón durante la tarea
        self.worker_thread = WorkerThread()
        self.worker_thread.progress.connect(self.update_label)
        self.worker_thread.finished.connect(self.task_finished)
        self.worker_thread.start()  # Inicia el hilo

    def update_label(self, value):
        self.label.setText(f"Tiempo transcurrido: {value}")

    def task_finished(self):
        self.label.setText("Tarea completada")
        self.button.setEnabled(True)  # Habilita el botón al finalizar

from PySide6.QtCore import QThread, Signal

class WorkerThread(QThread):
    progress = Signal(int)  # Señal para enviar actualizaciones
    finished = Signal()     # Señal para indicar que terminó

    def run(self):
        # Ejemplo de tarea intensiva
        for i in range(10):  # Simula 10 pasos de trabajo
            self.sleep(1)  # Pausa de 1 segundo por paso
            self.progress.emit(i + 1)  # Envía el progreso actualizado
        self.finished.emit()  # Señal cuando se completa

