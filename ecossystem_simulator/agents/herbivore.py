from ecossystem_simulator.agents.base_agent import BaseAgent
from ecossystem_simulator.agents.plant import Plant
import random

class Herbivore(BaseAgent):
    def __init__(self, unique_id, pos, model, speed=1.0, reproduction_rate=0.5, hunger_threshold=10, max_age=70):
        super().__init__(unique_id, model, speed, reproduction_rate)
        self.age = 0
        self.max_age = max_age
        self.sex = random.choice(["male", "female"])
        self.is_aware = random.choice([False, True, False])
        self.hunger = 0
        self.hunger_threshold = hunger_threshold
        self.memory = []

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

        try:
            if self.is_aware:
                from ecossystem_simulator.agents.carnivore import Carnivore  # Importação absoluta dentro do método
                predator_pos = self.find_nearest_target(Carnivore)
                if predator_pos and self.get_distance(self.pos, predator_pos) < 5:
                    self.move_away(predator_pos)
                    print("Herbívoro consciente fugiu de um predador")
                    return

            if self.memory:
                target_pos = self.memory.pop(0)
                self.move_towards(target_pos)
                self.eat(Plant)
            else:
                self.move(prey_class=Plant)
                plant_pos = self.find_nearest_target(Plant)
                if plant_pos:
                    self.memory.append(plant_pos)
                self.eat(Plant)
        except Exception as e:
            print(e)

        self.reproduce(Herbivore, self.reproduction_rate, self.model.max_offspring)
        self.calculate_fitness()

    def die(self):
        try:
            pos_at_death = self.pos
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.increase_growth_chance(pos_at_death)
        except Exception as e:
            print(e)
