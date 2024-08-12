from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from ecossystem_simulator.models.data_collection import DataCollector
from ecossystem_simulator.agents.plant import Plant
from ecossystem_simulator.agents.herbivore import Herbivore
from ecossystem_simulator.agents.carnivore import Carnivore
from ecossystem_simulator.agents.polinator import Pollinator
from typing import Union

class EcosystemModel(Model):
    def __init__(self, width, height, initial_plants, initial_herbivores, initial_carnivores, initial_polinators, plant_reproduction_rate, herbivore_reproduction_rate, carnivore_reproduction_rate, max_offspring, steps_per_season):
        self.width = width
        self.height = height
        self.plant_reproduction_rate = plant_reproduction_rate
        self.herbivore_reproduction_rate = herbivore_reproduction_rate
        self.carnivore_reproduction_rate = carnivore_reproduction_rate
        self.max_offspring = max_offspring
        self.steps_per_season = steps_per_season
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, True)
        self.datacollector = DataCollector(
            {
                "Plantas": lambda m: self.count_type(m, Plant),
                "Herbívoros": lambda m: self.count_type(m, Herbivore),
                "Carnívoros": lambda m: self.count_type(m, Carnivore),
                "Polinizadores": lambda m: self.count_type(m, Pollinator),
            }
        )
        self.current_id = 0
        self.step_count = 0
        self.season = "Primavera"

        self.fertile_spots = {}

        self.generate(initial_plants, Plant)
        self.generate(initial_herbivores, Herbivore)
        self.generate(initial_carnivores, Carnivore)
        self.generate(initial_polinators, Pollinator)

        self.running = True
        self.datacollector.collect(self)

    def increase_growth_chance(self, pos):
        print(f"Posição fértil: {pos}")
        if pos in self.fertile_spots:
            self.fertile_spots[pos] += 0.2
        else:
            self.fertile_spots[pos] = 0.2

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.step_count += 1

        for pos, growth_bonus in self.fertile_spots.items():
            if pos is not None and self.random.random() < (self.plant_reproduction_rate + growth_bonus):
                if self.grid.is_cell_empty(pos):
                    new_plant = Plant(self.next_id(), pos, self)
                    self.grid.place_agent(new_plant, pos)
                    self.schedule.add(new_plant)

        self.fertile_spots.clear()

        if self.step_count % self.steps_per_season == 0:
            self.change_season()

    def change_season(self):
        if self.season == "Primavera":
            self.season = "Verão"
            self.plant_reproduction_rate *= 1
        elif self.season == "Verão":
            self.season = "Outono"
            self.plant_reproduction_rate *= 0.7
        elif self.season == "Outono":
            self.season = "Inverno"
            self.plant_reproduction_rate *= 0.3
        elif self.season == "Inverno":
            self.season = "Primavera"
            self.plant_reproduction_rate *= 2

        print(f"Estação atual: {self.season}")

    @staticmethod
    def count_type(model, agent_type):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, agent_type):
                count += 1
        return count

    def generate(self, agents_number: int, model: Union[Plant, Herbivore, Carnivore, Pollinator]):
        for _ in range(agents_number):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            if model == Herbivore:
                agent = model(self.next_id(), (x, y), self, reproduction_rate=self.herbivore_reproduction_rate)
            elif model == Carnivore:
                agent = model(self.next_id(), (x, y), self, reproduction_rate=self.carnivore_reproduction_rate)
            elif model == Pollinator:
                agent = model(self.next_id(),(x,y), self)
            else: 
                agent = model(self.next_id(), (x, y), self)

            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)
