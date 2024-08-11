from ecossystem_simulator.agents.base_agent import BaseAgent
import random

class Carnivore(BaseAgent):
    def __init__(self, unique_id, pos, model, speed=1.5, reproduction_rate=0.5, min_age_for_reproduction=20, max_age=70, hunger_threshold=10):
        super().__init__(unique_id, model, speed, reproduction_rate)
        self.age = 0
        self.min_age_for_reproduction = min_age_for_reproduction
        self.max_age = max_age
        self.sex = random.choice(["male", "female"])
        self.hunger = 0
        self.hunger_threshold = hunger_threshold

    def step(self):
        if self.hunger >= self.hunger_threshold:
            self.die()
            return

        self.hunger += 1

        if self.age >= self.max_age:
            self.die()
            return

        self.age += 1

        if self.random.random() < 0.001:
            self.die()
            return

        from .herbivore import Herbivore  # Importação movida para dentro do método
        self.move(prey_class=Herbivore)
        self.eat(Herbivore)
        self.reproduce(Carnivore, self.reproduction_rate, self.model.max_offspring)
        self.calculate_fitness()
