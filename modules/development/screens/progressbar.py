from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QPushButton
from PySide6.QtCore import Qt, QThread, Signal
import time

# Clase para el hilo de trabajo que actualizará la barra de progreso
class ProgressThread(QThread):
    progress_updated = Signal(int)  # Señal para actualizar la barra de progreso

    def run(self):
        for i in range(101):
            time.sleep(0.05)  # Simula un proceso largo
            self.progress_updated.emit(i)  # Emite la señal con el nuevo valor

class ProgressBarScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Barra de Progreso")

        layout = QVBoxLayout(self)

        # Crear la barra de progreso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        # Crear el botón para iniciar el progreso
        self.button = QPushButton("Iniciar Progreso", self)
        self.button.clicked.connect(self.start_progress)

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.button)

        self.thread = ProgressThread()  # Crear una instancia del hilo
        self.thread.progress_updated.connect(self.update_progress)  # Conectar la señal

    def start_progress(self):
        # Iniciar el hilo
        self.thread.start()

    def update_progress(self, value):
        # Actualizar la barra de progreso con el valor recibido
        self.progress_bar.setValue(value)
