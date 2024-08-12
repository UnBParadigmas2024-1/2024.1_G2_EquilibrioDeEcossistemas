from .base_agent import BaseAgent
from .plant import Plant
import random

class Pollinator(BaseAgent):
    def __init__(self, unique_id, pos, model, polen_count, max_age=random.randrange(0, 15)):
        super().__init__(unique_id, model)
        self.carrying_pollen = False  # Indica se o polinizador está carregando pólen
        self.age = 0
        self.max_age = max_age
        self.polen_count = 0

    def step(self):
        if self.age >= self.max_age:
            if random.random() < 0.5:
                self.die()
                return
        else:
            self.age += 1

        from .plant import Plant
    
        if not self.carrying_pollen:
            # Move até a planta mais próxima
            self.move(prey_class=Plant)            
            self.collect_pollen() 
        else:
            # Move para uma posição aleatória e planta uma nova planta
            if self.polen_count < 5:
                self.move_random()
                self.polen_count += 1
            else:                
                neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
                for neighbor in neighbors:
                    cell_contents = self.model.grid.get_cell_list_contents([neighbor])
                    for obj in cell_contents:
                        if not isinstance(obj, Plant):
                            self.plant_new_plant()
                            self.polen_count = 0
                        else:
                            self.move_random()

    def is_old(self):
        return (self.age / self.max_age) >= 0.75

    def collect_pollen(self):
        # Verifica se o polinizador está em uma célula com uma planta
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for mate in cellmates:
            if isinstance(mate, Plant):
                self.carrying_pollen = True  # Agora o polinizador está carregando pólen
                print(f"Polinizador {self.unique_id} coletou pólen em {self.pos}")
                return

    def plant_new_plant(self):
        if self.carrying_pollen:
            new_plant = Plant(self.model.next_id(), self.pos, self.model)
            self.model.grid.place_agent(new_plant, self.pos)
            self.model.schedule.add(new_plant)
            self.carrying_pollen = False  # Polinizador plantou e não está mais carregando pólen
            print(f"Polinizador {self.unique_id} plantou uma nova planta em {self.pos}")
