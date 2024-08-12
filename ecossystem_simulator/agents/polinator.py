from .base_agent import BaseAgent
from .plant import Plant

class Pollinator(BaseAgent):
    def __init__(self, unique_id, pos, model, polen_count):
        super().__init__(unique_id, model,polen_count)
        self.carrying_pollen = False  # Indica se o polinizador está carregando pólen
        self.polen_count = 0

    def step(self):
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
