from threading import Lock

class SingletonMeta(type):
    """Metaclase para implementar el patrón Singleton."""
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Activo(metaclass=SingletonMeta):
    def __init__(self):
        self.condiciones = []  # Lista para almacenar condiciones activas
        self.suscriptores = {}  # Mapeo de condiciones a una lista de Jobs suscritos
        self.lock = Lock()  # Bloqueo para acceso concurrente

    def agregar_condicion(self, condicion):
        """Añade o incrementa el contador de una condición."""
        with self.lock:
            if condicion not in self.condiciones:
                self.condiciones.append(condicion)

            # Notificar a los Jobs suscritos
            if condicion in self.suscriptores:
                for job in self.suscriptores[condicion]:
                    job.notificar(condicion)

    def consumir_condicion(self, condicion):
        """Consume una condición si existe y reduce su contador."""
        with self.lock:
            if condicion in self.condiciones:
                self.condiciones.remove(condicion)
                return True
            return False  # La condición no estaba disponible

    def verificar_condicion(self, condicion):
        """Verifica si una condición está disponible."""
        with self.lock:
            return condicion in self.condiciones

    def suscribirse(self, condicion, job):
        """Permite que un Job se suscriba a una condición."""
        with self.lock:
            if condicion not in self.suscriptores:
                self.suscriptores[condicion] = []
            self.suscriptores[condicion].append(job)