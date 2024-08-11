from .base_agent import BaseAgent
import random

class Plant(BaseAgent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.is_poisonous = random.choice([True, False, False]) # inicializa planta venenosa aleatoriamente

    def step(self):
        if self.random.random() < self.model.plant_reproduction_rate:
            new_pos = (self.next_pos(self.model.grid.width), self.next_pos(self.model.grid.height))
            new_plant = Plant(self.model.next_id(), new_pos, self.model)
            self.model.grid.place_agent(new_plant, new_pos)
            self.model.schedule.add(new_plant)
