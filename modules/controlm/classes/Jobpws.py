from modules.controlm.classes.Condition import Condition
from modules.controlm.classes.JobStatus import JobStatus

class Job:
    def __init__(self, json_object):
        self.id = json_object.get("id", "")
        self.type = json_object.get("type", "")
        self.prerequisites = [Condition(action) for action in json_object.get("prerequisites", [])]
        self.actions = [Condition(action) for action in json_object.get("actions", [])]
        self.status = JobStatus.WAITING
        self.log = None
        self.exit_code = None
        # self.holded = False  # Comentado según tu código original

    def Hold(self):
        self.status = JobStatus.HOLDED

    def Unhold(self):
        self.status = JobStatus.WAITING

    def Execute(self):
        pass #Integrar en los jobs especificos

    def Kill(self):
        pass  # Integrar en los jobs especificos