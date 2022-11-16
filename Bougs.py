import json


class Boug:
    def __init__(self, id, name, money, last_connected):
        self.id = id
        self.name = name
        self.money = money
        self.last_connected = last_connected

    def toJson(self):
        print(json.dumps(self, default=lambda o: o.__dict__))
        return json.dumps(self, default=lambda o: o.__dict__)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_money(self):
        return self.money

    def get_last_connected(self):
        return self.last_connected
