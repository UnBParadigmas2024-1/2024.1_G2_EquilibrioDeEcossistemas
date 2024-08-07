from mesa import Agent
from functools import wraps

def check_pos(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.pos != None:
            return func(*args, **kwargs)
        return
    return wrapper

class BaseAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model = model

    def next_pos(self, dimension):
        return self.random.randrange(dimension)

    @check_pos
    def move(self):
        # print(self.pos)
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        # print(possible_steps, new_position)
        self.model.grid.move_agent(self, new_position)
    
    @check_pos
    def eat(self, prey_model):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for mate in cellmates:
            if isinstance(mate, prey_model):
                self.model.grid.remove_agent(mate)
                self.model.schedule.remove(mate)
                break

class Plant(BaseAgent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        # self.pos = pos

    def step(self):
        if self.random.random() < 0.01:  # 1% chance de reprodução a cada passo
            new_pos = (self.next_pos(self.model.grid.width), self.next_pos(self.model.grid.height))
            new_plant = Plant(self.model.next_id(), new_pos, self.model)
            self.model.grid.place_agent(new_plant, new_pos)
            self.model.schedule.add(new_plant)

class Herbivore(BaseAgent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        # self.pos = pos

    def step(self):
        self.move()
        self.eat(Plant)

class Carnivore(BaseAgent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        # self.pos = pos

    def step(self):
        self.move()
        self.eat(Herbivore)