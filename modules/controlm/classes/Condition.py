class Condition:
    def __init__(self, json_object):
        self.name = json_object.get("name", "")
        self.exit = json_object.get("exit", "")
        self.sign = json_object.get("sign", "")
        self.operator = json_object.get("operator", "AND")

    def __init__(self, name, operator):
        self.name = name
        self.operator = operator