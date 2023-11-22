from fastautomata import Agents

# TODO hacer que todos los agentes se pongan juntos de un jalon

class Road(Agents.StaticAgent):
    roads: list['Road'] = []

class Destination(Agents.StaticAgent):
    pass

class Building(Agents.StaticAgent):
    pass

class Stoplight(Agents.simulatedAgent):
    def step(self):
        pass

class Car(Agents.simulatedAgent):
    def step(self):
        pass