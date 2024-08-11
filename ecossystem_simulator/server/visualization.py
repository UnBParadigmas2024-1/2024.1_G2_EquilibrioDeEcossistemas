from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization import Slider
from ecossystem_simulator.agents.plant import Plant
from ecossystem_simulator.agents.herbivore import Herbivore
from ecossystem_simulator.agents.carnivore import Carnivore

def agent_portrayal(agent):
    if isinstance(agent, Plant):
        portrayal = {"Shape": "circle", "Color": "green", "Filled": "true", "r": 0.5, "Layer": 1}
    elif isinstance(agent, Herbivore):
        portrayal = {"Shape": "circle", "Color": "blue", "Filled": "true", "r": 1, "Layer": 1}
    elif isinstance(agent, Carnivore):
        portrayal = {"Shape": "circle", "Color": "red", "Filled": "true", "r": 1, "Layer": 1}
    return portrayal

def create_sliders():
    return {
        "initial_plants": Slider(
            name="Número de Plantas",
            value=60,
            min_value=0,
            max_value=600,
            step=1,
            description="Escolha quantas plantas incluir no modelo",
        ),
        "initial_carnivores": Slider(
            name="Número de Carnívoros",
            value=30,
            min_value=0,
            max_value=500,
            step=1,
            description="Escolha quantos carnívoros incluir no modelo",
        ),
        "initial_herbivores": Slider(
            name="Número de Herbívoros",
            value=65,
            min_value=0,
            max_value=650,
            step=1,
            description="Escolha quantos herbívoros incluir no modelo",
        ),
        "plant_reproduction_rate": Slider(
            name="Taxa de Reprodução das Plantas",
            value=0.01,
            min_value=0,
            max_value=1,
            step=0.01,
            description="Escolha a taxa de reprodução das plantas",
        ),
        "carnivore_reproduction_rate": Slider(
            name="Taxa de Reprodução dos Carnívoros",
            value=0.5,
            min_value=0,
            max_value=10,
            step=0.1,
            description="Escolha a taxa de reprodução dos carnívoros",
        ),
        "max_offspring": Slider(
            name="Número Máximo de Descendentes",
            value=2,
            min_value=1,
            max_value=5,
            step=1,
            description="Escolha o número máximo de descendentes gerados na reprodução",
        ),
        "steps_per_season": Slider(
            name="Passos por Estação",
            value=100,
            min_value=10,
            max_value=1000,
            step=10,
            description="Número de passos antes de mudar a estação",
        ),
        "width": 50,
        "height": 50,
    }
