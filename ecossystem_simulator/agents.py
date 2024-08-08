from mesa import Agent
from functools import wraps
import math

def check_pos(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.pos is not None:
            return func(*args, **kwargs)
        return
    return wrapper

class BaseAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model = model

    def next_pos(self, dimension):
        return self.random.randrange(dimension)

    def get_distance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def find_nearest_target(self, target_class):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        closest_target = None
        closest_distance = float('inf')

        for neighbor in neighbors:
            cell_contents = self.model.grid.get_cell_list_contents([neighbor])
            for obj in cell_contents:
                if isinstance(obj, target_class):
                    distance = self.get_distance(self.pos, neighbor)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_target = neighbor

        return closest_target

    def move_towards(self, target_pos):
        # Movimenta o agente em direção à posição do alvo
        if target_pos:
            # Pega os vizinhos da célula atual
            neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            # Seleciona o vizinho mais próximo da posição alvo
            next_pos = min(neighbors, key=lambda x: self.get_distance(x, target_pos))
            self.model.grid.move_agent(self, next_pos)
        else:
            # Caso não haja alvo próximo, move-se de forma aleatória
            self.move_random()

    def move_random(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    @check_pos
    def move(self, target_class=None):
        if target_class:
            target_pos = self.find_nearest_target(target_class)
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

class Plant(BaseAgent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)

    def step(self):
        if self.random.random() < self.model.plant_reproduction_rate:
            new_pos = (self.next_pos(self.model.grid.width), self.next_pos(self.model.grid.height))
            new_plant = Plant(self.model.next_id(), new_pos, self.model)
            self.model.grid.place_agent(new_plant, new_pos)
            self.model.schedule.add(new_plant)

class Herbivore(BaseAgent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)

    def step(self):
        self.move(target_class=Plant)
        self.eat(Plant)

class Carnivore(BaseAgent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)

    def step(self):
        self.move(target_class=Herbivore)
        self.eat(Herbivore)
        self.reproduce(Carnivore, self.model.carnivore_reproduction_rate, self.model.max_offspring)
