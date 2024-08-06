from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from .agents import Plant, Herbivore, Carnivore

class EcosystemModel(Model):
    def __init__(self, width, height, initial_plants, initial_herbivores, initial_carnivores):
        self.width = width
        self.height = height
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, True)
        self.datacollector = DataCollector(
            {
                "Plants": lambda m: self.count_type(m, Plant),
                "Herbivores": lambda m: self.count_type(m, Herbivore),
                "Carnivores": lambda m: self.count_type(m, Carnivore),
            }
        )
        self.current_id = 0

        # Criando as plantas
        self.generate(initial_plants, Plant)
        # Criando os herbívoros
        self.generate(initial_herbivores, Herbivore)
        # Criando os carnívoros
        self.generate(initial_carnivores, Carnivore)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    @staticmethod
    def count_type(model, agent_type):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, agent_type):
                count += 1
        return count

    def generate(self, agents_number: int, model: Plant | Herbivore | Carnivore):
        for _ in range(agents_number):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            agent = model(self.next_id(), (x, y), self)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)