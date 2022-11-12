import json

class Boug():
    def __init__(self, id, name, money):
        self.id = id
        self.name = name
        self.money = money

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)