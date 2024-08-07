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
    grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
    chart = ChartModule(
        [{"Label": "Plants", "Color": "green"},
         {"Label": "Herbivores", "Color": "blue"},
         {"Label": "Carnivores", "Color": "red"}]
    )

    model_params = {
        "initial_plants": mesa.visualization.Slider(
            name="Número de Plantas",
            value=10,
            min_value=0,
            max_value=100,
            step=1,
            description="Escolha quantas plantas incluir no modelo",
        ),
        "initial_carnivores": mesa.visualization.Slider(
            name="Número de Carnívoros",
            value=10,
            min_value=0,
            max_value=100,
            step=1,
            description="Escollha quantos carnívoros incluir no modelo",
        ),
        "initial_herbivores": mesa.visualization.Slider(
            name="Número de Herbívoros",
            value=10,
            min_value=0,
            max_value=100,
            step=1,
            description="Escollha quantos herbívoros incluir no modelo",
        ),
        "width": 20,
        "height": 20,
    }

    server = ModularServer(
        EcosystemModel,
        [grid, chart],
        "Ecosystem Simulation",
        model_params
    )

    server.port = 8521
    server.launch()