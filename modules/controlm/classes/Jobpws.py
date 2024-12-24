class Job:
    def __init__(self, nombre, condiciones_entrada, condiciones_salida, activo):
        self.nombre = nombre
        self.condiciones_entrada = condiciones_entrada  # Lista de condiciones necesarias para activarse
        self.condiciones_salida = condiciones_salida  # Lista de condiciones generadas al finalizar
        self.activo = activo  # Instancia del Activo
        self.esta_activo = False

        # Suscribirse a las condiciones de entrada
        for condicion in self.condiciones_entrada:
            self.activo.suscribirse(condicion.name, self)

    def puede_activarse(self):
        """Verifica si todas las condiciones de entrada de tipo AND están disponibles,
           y al menos una de las condiciones de tipo OR."""
        if len(self.condiciones_entrada) == 0:
            return True
        and_conditions_met = [
            self.activo.verificar_condicion(condicion.name) for condicion in self.condiciones_entrada if
            condicion.operator == 'AND'
        ]

        or_conditions_met = any(
            self.activo.verificar_condicion(condicion.name) for condicion in self.condiciones_entrada if
            condicion.operator == 'OR'
        )

        # El Job solo puede activarse si todas las condiciones AND están disponibles
        # y al menos una condición OR está disponible
        return and_conditions_met and or_conditions_met

    def activar(self):
        """Activa el Job si puede activarse."""
        if self.puede_activarse():
            print(f"{self.nombre} activado.")
            # Consumir las condiciones de entrada
            for condicion in self.condiciones_entrada:
                self.activo.consumir_condicion(condicion)
            self.esta_activo = True
            self.ejecutar()
        else:
            print(f"{self.nombre} no puede activarse aún.")

    def ejecutar(self):
        """Simula la ejecución del Job."""
        print(f"{self.nombre} ejecutando...")
        # Aquí se coloca la lógica de ejecución del Job
        self.finalizar()

    def finalizar(self):
        """Notifica al Activo las condiciones de salida y marca el Job como finalizado."""
        print(f"{self.nombre} finalizado.")
        for condicion in self.condiciones_salida:
            self.activo.agregar_condicion(condicion.name)
        self.esta_activo = False

    def notificar(self, condicion):
        """Método llamado por el Activo cuando una condición se vuelve disponible."""
        print(f"{self.nombre} recibió notificación: {condicion} disponible.")
        self.activar()