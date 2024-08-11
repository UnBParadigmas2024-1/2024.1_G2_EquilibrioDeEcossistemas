from mesa import Agent
from functools import wraps
import math
import random
from .utils.decorators import check_pos

class BaseAgent(Agent):
    def __init__(self, unique_id, model, speed=1.0, reproduction_rate=0.5):
        super().__init__(unique_id, model)
        self.model = model
        self.speed = speed  # Velocidade do agente
        self.reproduction_rate = reproduction_rate  # Taxa de reprodução
        self.fitness = 0 

    def calculate_fitness(self):
        # Calcula a fitness com base nas características
        self.fitness = self.speed + self.reproduction_rate

    def inherit_traits(self, parent1, parent2):
        # Herdar características dos pais com mutação
        self.speed = (parent1.speed + parent2.speed) / 2 + random.uniform(-0.1, 0.1)
        self.reproduction_rate = (parent1.reproduction_rate + parent2.reproduction_rate) / 2 + random.uniform(-0.1, 0.1)

    def next_pos(self, dimension):
        return self.random.randrange(dimension)

    def get_distance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def find_nearest_target(self, prey_class):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        closest_target = None
        closest_distance = float('inf')

        for neighbor in neighbors:
            cell_contents = self.model.grid.get_cell_list_contents([neighbor])
            for obj in cell_contents:
                if isinstance(obj, prey_class):
                    distance = self.get_distance(self.pos, neighbor)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_target = neighbor

        return closest_target

    def move_towards(self, target_pos):
        # Movimenta o agente em direção à posição do alvo
        if target_pos:
            neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            next_pos = min(neighbors, key=lambda x: self.get_distance(x, target_pos))
            self.model.grid.move_agent(self, next_pos)
        else:
            # Caso não haja alvo próximo, move-se de forma aleatória
            self.move_random()

    def move_away(self, target_pos):
        # Movimenta o agente na direção oposta à posição do predator
        if target_pos:
            neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            next_pos = max(neighbors, key=lambda x: self.get_distance(x, target_pos))
            self.model.grid.move_agent(self, next_pos)

    def move_random(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    @check_pos
    def move(self, prey_class=None):
        if prey_class:
            target_pos = self.find_nearest_target(prey_class)
            self.move_towards(target_pos)
        else:
            self.move_random()

    @check_pos
    def eat(self, prey_model):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for mate in cellmates:
            if isinstance(mate, prey_model):
                self.model.grid.remove_agent(mate)
                self.model.schedule.remove(mate)
                self.hunger = 0

                from .plant import Plant # Importa localmente para evitar importação cíclica
                if isinstance(mate, Plant):
                    if mate.is_poisonous:
                        print("Herbívoro comeu planta venenosa e morreu")
                        self.die()

                break

    @check_pos
    def reproduce(self, mate_model, reproduction_rate, max_offspring):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for mate in cellmates:
            if isinstance(mate, mate_model) and mate != self:
                if self.random.random() < reproduction_rate:
                    num_offspring = self.random.randint(1, max_offspring)
                    for _ in range(num_offspring):
                        new_pos = self.random.choice(self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False))
                        new_agent = mate_model(self.model.next_id(), new_pos, self.model)
                        self.model.grid.place_agent(new_agent, new_pos)
                        self.model.schedule.add(new_agent)
                break

    def die(self):
        try:
            pos_at_death = self.pos
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.increase_growth_chance(pos_at_death)
        except Exception as e:
            print(e)
