from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from typing import Union

from .agents import Plant, Herbivore, Carnivore

class EcosystemModel(Model):
    def __init__(self, width, height, initial_plants, initial_herbivores, initial_carnivores, plant_reproduction_rate, carnivore_reproduction_rate, max_offspring, steps_per_season):
        self.width = width
        self.height = height
        self.plant_reproduction_rate = plant_reproduction_rate
        self.carnivore_reproduction_rate = carnivore_reproduction_rate
        self.max_offspring = max_offspring
        self.steps_per_season = steps_per_season
        self.current_step = 0
        self.season = "Summer"
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, True)
        self.datacollector = DataCollector(
            {
                "Plantas": lambda m: self.count_type(m, Plant),
                "Herbívoros": lambda m: self.count_type(m, Herbivore),
                "Carnívoros": lambda m: self.count_type(m, Carnivore),
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
        self.current_step += 1

        # Alterar a estação após um número fixo de passos
        if self.current_step % self.steps_per_season == 0:
            self.change_season()

    def change_season(self):
        if self.season == "Summer":
            self.season = "Winter"
        else:
            self.season = "Summer"

        # Ajustar taxas baseadas na estação
        if self.season == "Summer":
            # Taxa de reprodução no verão
            self.plant_reproduction_rate = 0.1  
            self.carnivore_reproduction_rate = 0.05
        else:
            # Taxa de reprodução no inverno
            self.plant_reproduction_rate = 0.01  
            self.carnivore_reproduction_rate = 0.01 

    @staticmethod
    def count_type(model, agent_type):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, agent_type):
                count += 1
        return count

    def generate(self, agents_number: int, model: Union[Plant, Herbivore, Carnivore]):
        for _ in range(agents_number):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            agent = model(self.next_id(), (x, y), self)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

    def next_id(self):
        self.current_id += 1
        return self.current_id
