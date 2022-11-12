import json

class Boug():
    def __init__(self, id, name, money):
        self.id = id
        self.name = name
        self.money = money

    def toJson(self):
        print(json.dumps(self, default=lambda o: o.__dict__))
        return json.dumps(self, default=lambda o: o.__dict__)
    
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_money(self):
        return self.money