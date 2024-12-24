import threading
import queue
import time
from datetime import datetime

from modules.controlm.classes.JobStatus import JobStatus


class Condition:
    def __init__(self, name, operator="AND"):
        self.name = name
        self.operator = operator


class Activo(threading.Thread):
    def __init__(self):
        super().__init__()
        self.condiciones = []  # Lista de condiciones activas
        self.suscriptores = {}  # Mapeo de condiciones a una lista de Jobs suscritos
        self.jobs = []  # Lista de jobs
        self.lock = threading.Lock()  # Bloqueo para acceso concurrente
        self._detener = threading.Event()  # Evento para detener el hilo del activo
        self.ui_observadores = []

    def run(self):
        """Método principal del hilo Activo."""
        while not self._detener.is_set():
            # Aquí puedes agregar la lógica de monitoreo de condiciones y activar Jobs si es necesario
            time.sleep(1)

    # def ciclo(self):
    #     """Ejecuta una iteración del ciclo principal para verificar y activar Jobs."""
    #     with self.lock:
    #         for job in self.jobs:
    #             if not job.esta_activo and job.puede_activarse():
    #                 job.activar()  # Activa el Job si cumple sus condiciones

    def agregar_condicion(self, condicion):
        """Añadir una condición para que sea procesada por los jobs."""
        with self.lock:
            if condicion not in self.condiciones:
                self.condiciones.append(condicion)

    def consumir_condicion(self, condicion):
        """Consume una condición si existe."""
        with self.lock:
            if condicion in self.condiciones:
                self.condiciones.remove(condicion)
                return True
            return False

    def suscribirse(self, condicion, job):
        """Permite que un Job se suscriba a una condición."""
        with self.lock:
            if condicion not in self.suscriptores:
                self.suscriptores[condicion] = []
            self.suscriptores[condicion].append(job)

    def verificar_condicion(self, condicion):
        with self.lock:
            return condicion in self.condiciones

    def agregar_job(self, job):
        """Agrega un Job a la lista de jobs y lo inicia automáticamente."""
        self.jobs.append(job)
        job.start()  # Inicia el Job automáticamente al agregarlo al Activo

    def detener(self):
        """Detiene el hilo principal del Activo y todos los Jobs asociados."""
        self._detener.set()
        for job in self.jobs:
            job.detener()  # Detener todos los Jobs de manera ordenada
        print("Activo detenido.")

    def suscribirse_a_ui(self, observador):
        """Permite que la interfaz se suscriba a las actualizaciones."""
        self.ui_observadores.append(observador)

    def notificar_ui(self, evento, datos):
        """Notifica a todos los observadores (la interfaz) de un cambio."""
        for observador in self.ui_observadores:
            observador.actualizar(evento, datos)


class Job(threading.Thread):
    def __init__(self, name, condiciones_entrada, condiciones_salida, activo,status=JobStatus.WAITING, start_date=None, end_date=None):
        super().__init__()
        self.name = name
        self.condiciones_entrada = condiciones_entrada  # Condiciones necesarias para activarse
        self.condiciones_salida = condiciones_salida  # Condiciones generadas al finalizar
        self.activo = activo  # Instancia del Activo
        self._detener = threading.Event()  # Evento de detención para este Job
        self._esperando_condiciones = threading.Event()  # Evento para esperar condiciones
        self.esta_activo = False
        self.status = status
        self.start_date = start_date
        self.end_date = end_date


    def run(self):
        """Método que se ejecuta en el hilo del Job."""

        while not self._detener.is_set():

            if self.puede_activarse():
                print("Entrando al metodo run")
                self.activar()
                time.sleep(1)  # Simula la ejecución del Job
                self.finalizar()
            else:
                self._esperando_condiciones.wait(timeout=1)  # Espera las condiciones necesarias

    def puede_activarse(self):
        """Verifica si todas las condiciones de entrada están disponibles."""
        print(len(self.condiciones_entrada))
        if len(self.condiciones_entrada) == 0:
            return True

        and_conditions_met = all(
            self.activo.verificar_condicion(condicion) for condicion in self.condiciones_entrada if condicion.operator == 'AND'
        )
        or_conditions_met = any(
            self.activo.verificar_condicion(condicion) for condicion in self.condiciones_entrada if condicion.operator == 'OR'
        )

        # El Job solo se activa si las condiciones AND están disponibles y alguna condición OR lo está
        return and_conditions_met and or_conditions_met

    def activar(self):
        """Activa el Job cuando todas las condiciones se cumplan."""
        if self.puede_activarse():
            print(f"{self.name} activado.")
            for condicion in self.condiciones_entrada:
                self.activo.consumir_condicion(condicion)
            self.esta_activo = True
            self.ejecutar()

    def ejecutar(self):
        """Simula la ejecución del Job."""
        self.start_date = datetime.now()
        self.status = JobStatus.RUNNING
        print(f"{self.name} ejecutando...")

    def finalizar(self):
        """Finaliza el Job y notifica las condiciones de salida."""
        print(f"{self.name} finalizado.")
        for condicion in self.condiciones_salida:
            self.activo.agregar_condicion(condicion)
        self.esta_activo = False
        self.end_date = datetime.now()
        self.status = JobStatus.OK

    def notificar(self, condicion):
        """Método llamado por el Activo cuando una condición se vuelve disponible."""
        print(f"{self.name} recibió notificación: {condicion} disponible.")
        self.activar()

    def detener(self):
        """Detiene el Job, activando el evento de detención."""
        print(f"{self.name} detenido.")
        self.end_date = datetime.now()
        self.status = JobStatus.KO
        self._detener.set()  # Señala que el Job debe detenerse
        self._esperando_condiciones.set()  # Asegura que no quede esperando condiciones




if __name__ == "__main__":
    activo = Activo()
    activo.start()

    cond1 = Condition("condicion1", "AND")
    cond2 = Condition("condicion2", "OR")

    job1 = Job("Job1", [cond1, cond2], [Condition("condicion3")], activo)
    job2 = Job("Job2", [Condition("condicion3")], [], activo)

    job1.start()
    job2.start()

    activo.agregar_condicion("condicion1")
    time.sleep(1)
    activo.agregar_condicion("condicion2")

    time.sleep(5)  # Esperar a que los Jobs finalicen sus tareas
    activo.detener()

    job1.join()
    job2.join()
    activo.join()
