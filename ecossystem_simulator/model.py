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
        self.step_count = 0
        self.season = "Primavera"  # Iniciar na Primavera

        # Criando a matriz de nutrientes
        self.nutrient_grid = [[0 for _ in range(height)] for _ in range(width)]

        # Criando as plantas
        self.generate(initial_plants, Plant)
        # Criando os herbívoros
        self.generate(initial_herbivores, Herbivore)
        # Criando os carnívoros
        self.generate(initial_carnivores, Carnivore)

        self.running = True
        self.datacollector.collect(self)

    def add_nutrient(self, pos, amount):
        x, y = pos
        self.nutrient_grid[x][y] += amount

    def get_nutrient(self, pos):
        x, y = pos
        return self.nutrient_grid[x][y]

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.step_count += 1

        # Mudar de estação após um número específico de passos
        if self.step_count % self.steps_per_season == 0:
            self.change_season()

        # Reduzir nutrientes gradualmente
        for x in range(self.width):
            for y in range(self.height):
                if self.nutrient_grid[x][y] > 0:
                    self.nutrient_grid[x][y] -= 1  # Nutrientes diminuem ao longo do tempo

