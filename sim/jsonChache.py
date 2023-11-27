import json, os
from fastautomata.ClassTypes import Pos, PosJSON

class JsonSave:
    data: dict[str, dict[str, list[Pos]]]
    path: str

    def __init__(self, path):
        self.path = path
        self.data = {}
        self.load()

    def getRoute(self, road: Pos, destination: Pos) -> None | list[Pos]:
        if road.toString() not in self.data:
            return None
        if destination.toString() not in self.data[road.toString()]:
            return None
        
        return self.data[road.toString()][destination.toString()]
    
    def addRoute(self, road: Pos, destination: Pos, route: list[Pos]) -> None:
        if road.toString() not in self.data:
            self.data[road.toString()] = {}
        self.data[road.toString()][destination.toString()] = route

    def save(self):
        # check if the folder exists
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))

        with open(self.path, 'w') as outfile:
            json.dump(self.data, outfile, cls=PosJSON)

    def load(self):
        # test if the file exists
        try:
            with open(self.path) as json_file:
                data = json_file.read()
                data = json.loads(data)#, object_pairs_hook=PosJSON.decode)
                for road in data.keys():
                    self.data[road] = {}
                    for destination in data[road].keys():
                        self.data[road][destination] = []
                        for pos in data[road][destination]:
                            self.data[road][destination].append(Pos.from_array(pos))
        except FileNotFoundError:
            return