from Condition import Condition
from Activo import Activo
from Jobpws import Job
# Crear condiciones
condicion1 = Condition("condicion1", "AND")
condicion2 = Condition("condicion2", "AND")
condicion3 = Condition("condicion3", "AND")

# Crear una instancia del Activo
activo = Activo()

# Crear Jobs con condiciones de entrada y salida
job1 = Job("Job1", [], [condicion1], activo)  # Necesita 'condicion1' (AND)
job2 = Job("Job2", [condicion1], [condicion2], activo)  # Necesita 'condicion1' (AND) y al menos una 'OR'
job3 = Job("Job3", [condicion1], [condicion3], activo)  # Necesita al menos una 'OR'

# Activar el primer Job (que genera condiciones)
job1.activar()  # Genera 'condicion1'

# Ahora los demás Jobs pueden activarse si las condiciones están disponibles