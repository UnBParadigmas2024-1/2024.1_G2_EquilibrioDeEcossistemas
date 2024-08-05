from mesa import Agent

class Plant(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass

class Herbivore(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
    
    def move(self):
        pass
    
    def eat(self):
        pass

    def step(self):
        self.move()
        self.eat(Plant)

class Carnivore(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

    def move(self):
        pass
    
    def eat(self):
        pass

    def step(self):
        self.move()
        self.eat(Herbivore)