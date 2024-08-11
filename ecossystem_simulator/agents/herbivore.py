from .base_agent import BaseAgent
from .plant import Plant
import random

class Herbivore(BaseAgent):
    def __init__(self, unique_id, pos, model, speed=1.0, reproduction_rate=0.5, hunger_threshold=10, max_age=70):
        super().__init__(unique_id, model, speed, reproduction_rate)
        self.age = 0
        self.max_age = max_age
        self.sex = random.choice(["male", "female"])  # Atribui aleatoriamente o sexo
        self.is_aware = random.choice([False, True, False])  # Define aleatoriamente se o herbívoro é consciente com maiores chances de não ser
        self.hunger = 0  # Inicializa o nível de fome
        self.hunger_threshold = hunger_threshold  # Limite de fome para morte
        self.memory = []  # Lista de memória para guardar posições de plantas
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
            self.die()
            return

        self.age += 1  # Incrementa a idade do herbívoro a cada passo

        if self.random.random() < 0.001:
            self.die()
            return

        try:
            # Verifica se o herbívoro é consciente e se há predadores por perto
            if self.is_aware and not self.is_old and not self.is_ill:
                from .carnivore import Carnivore  # Importa localmente para evitar importação cíclica
                predator_pos = self.find_nearest_target(Carnivore)
                if predator_pos and self.get_distance(self.pos, predator_pos) < 5:  # Foge se o predador estiver a uma distância menor que 5
                    self.move_away(predator_pos)
                    print("Herbívoro consciente fugiu de um predador")
                    return

            # Verifica se há plantas na memória e se move em direção a elas
            if self.memory:
                target_pos = self.memory.pop(0)
                self.move_towards(target_pos)
                self.eat(Plant)
            else:
                # Movimento padrão do herbívoro
                self.move(prey_class=Plant)
                plant_pos = self.find_nearest_target(Plant)
                if plant_pos:
                    self.memory.append(plant_pos)  # Armazena a posição da planta na memória
                self.eat(Plant)
        except Exception as e:
            print(e)

        self.reproduce(Herbivore, self.reproduction_rate, self.model.max_offspring)
        self.calculate_fitness()

    def reproduce(self, mate_model, reproduction_rate, max_offspring):
        print(f"Reproduzindo na posição {self.pos}")
        if self.pos is None:
            print("Erro: posição do agente é None.")
            return
        
        if not hasattr(self.model, 'grid') or self.model.grid is None:
            print("Erro: grid não está definida no modelo.")
            return
        
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
