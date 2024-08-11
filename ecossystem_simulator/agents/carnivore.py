from .base_agent import BaseAgent
import random

class Carnivore(BaseAgent):
    def __init__(self, unique_id, pos, model, speed=1.5, reproduction_rate=0.5, min_age_for_reproduction=12, max_age=100, hunger_threshold=50):
        super().__init__(unique_id, model, speed, reproduction_rate)
        self.age = 0  # Inicializa a idade do carnívoro
        self.min_age_for_reproduction = min_age_for_reproduction  # Idade mínima para reprodução
        self.max_age = max_age  # Idade máxima antes de morrer
        self.sex = random.choice(["male", "female"])  # Atribui aleatoriamente o sexo
        self.hunger = 0  # Inicializa o nível de fome
        self.hunger_threshold = hunger_threshold  # Limite de fome para morte
        self.is_ill = False # Todos animais são inicializados saudáveis

    def is_old(self):
        return (self.age / self.max_age) >= 0.75
    
    def step(self):
        if self.is_ill and self.is_old():
            print("Animal idoso ficou doente e morreu")
            self.die()
            return

        if self.hunger >= (self.hunger_threshold * 0.8) and self.is_old():
            print("Animal idoso morreu de fome")
            self.die()
            return

        if self.hunger >= self.hunger_threshold:
            self.die()
            return

        self.hunger += 1

        if self.age >= self.max_age:
            if self.random.random() < 0.5:
                self.die()
            return

        self.age += 1  # Incrementa a idade do carnívoro a cada passo

        if self.random.random() < 0.001:
            self.die()
            return

        from .herbivore import Herbivore  # Importa localmente para evitar importação cíclica
        self.move(prey_class=Herbivore)
        self.eat(Herbivore)
        self.reproduce(Carnivore, self.reproduction_rate, self.model.max_offspring)
        self.calculate_fitness()

    def reproduce(self, mate_model, reproduction_rate, max_offspring):
        # Verifica se a idade do agente é suficiente para reprodução
        if self.age < self.min_age_for_reproduction:
            return  # Se a idade é menor que a mínima, não se reproduz
        
        # Código de reprodução modificado para considerar sexo
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for mate in cellmates:
            if isinstance(mate, mate_model) and mate != self:
                if self.sex != mate.sex:  # Somente se os sexos forem opostos
                    if self.random.random() < reproduction_rate:
                        num_offspring = self.random.randint(1, max_offspring)
                        for _ in range(num_offspring):
                            new_pos = self.random.choice(self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False))
                            new_agent = mate_model(self.model.next_id(), new_pos, self.model)
                            self.model.grid.place_agent(new_agent, new_pos)
                            self.model.schedule.add(new_agent)
                break
