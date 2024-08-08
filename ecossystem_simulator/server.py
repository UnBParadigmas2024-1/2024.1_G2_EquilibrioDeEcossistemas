from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from .model import EcosystemModel
from .agents import Plant, Herbivore, Carnivore

import mesa

def agent_portrayal(agent):
    if isinstance(agent, Plant):
        portrayal = {"Shape": "circle", "Color": "green", "Filled": "true", "r": 0.5, "Layer": 1}
    elif isinstance(agent, Herbivore):
        portrayal = {"Shape": "circle", "Color": "blue", "Filled": "true", "r": 0.5, "Layer": 1}
    elif isinstance(agent, Carnivore):
        portrayal = {"Shape": "circle", "Color": "red", "Filled": "true", "r": 0.5, "Layer": 1}
    return portrayal

def run():
    grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
    chart = ChartModule(
        [{"Label": "Plantas", "Color": "green"},
         {"Label": "Herbívoros", "Color": "blue"},
         {"Label": "Carnívoros", "Color": "red"}]
    )

    model_params = {
        "initial_plants": mesa.visualization.Slider(
            name="Número de Plantas",
            value=30,
            min_value=0,
            max_value=100,
            step=1,
            description="Escolha quantas plantas incluir no modelo",
        ),
        "initial_carnivores": mesa.visualization.Slider(
            name="Número de Carnívoros",
            value=5,
            min_value=0,
            max_value=100,
            step=1,
            description="Escollha quantos carnívoros incluir no modelo",
        ),
        "initial_herbivores": mesa.visualization.Slider(
            name="Número de Herbívoros",
            value=15,
            min_value=0,
            max_value=100,
            step=1,
            description="Escollha quantos herbívoros incluir no modelo",
        ),
        "plant_reproduction_rate": mesa.visualization.Slider(
            name="Taxa de Reprodução das Plantas",
            value=0.01,
            min_value=0,
            max_value=1,
            step=0.01,
            description="Escolha a taxa de reprodução das plantas",
        ),
        "carnivore_reproduction_rate": mesa.visualization.Slider(
            name="Taxa de Reprodução dos Carnívoros",
            value=0.5,
            min_value=0,
            max_value=10,
            step=0.1,
            description="Escolha a taxa de reprodução dos carnívoros",
        ),
        "max_offspring": mesa.visualization.Slider(
            name="Número Máximo de Descendentes",
            value=2,
            min_value=1,
            max_value=5,
            step=1,
            description="Escolha o número máximo de descendentes gerados na reprodução",
        ),
        "width": 50,
        "height": 50,
    }

    server = ModularServer(
        EcosystemModel,
        [grid, chart],
        "Simulador de Ecossistema",
        model_params
    )

    server.port = 8521
    server.launch()