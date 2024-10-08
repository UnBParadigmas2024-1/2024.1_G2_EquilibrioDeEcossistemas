from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization import Slider
from ecossystem_simulator.agents.plant import Plant
from ecossystem_simulator.agents.herbivore import Herbivore
from ecossystem_simulator.agents.carnivore import Carnivore
from ecossystem_simulator.agents.polinator import Pollinator

def agent_portrayal(agent):
    if isinstance(agent, Plant):
        if agent.is_poisonous:
            portrayal = {
                "Shape": "circle",
                "Color": "purple",  # Fundo roxo para plantas venenosas
                "r": 0.5,
                "Layer": 1,
                "text": "🍄",       # Emoji de cogumelo para plantas venenosas
                "text_color": "white"
            }
        else:
            portrayal = {
                "Shape": "circle",
                "Color": "green",  # Fundo verde para plantas normais
                "r": 0.5,
                "Layer": 1,
                "text": "🌱",       # Emoji de planta para plantas normais
                "text_color": "green"
            }
    elif isinstance(agent, Herbivore):
        portrayal = {
            "Shape": "circle",
            "Color": "blue",
            "r": 1,
            "Layer": 2,
            "text": "🐄",
            "text_color": "blue"
        }
    elif isinstance(agent, Carnivore):
        portrayal = {
            "Shape": "circle",
            "Color": "red",
            "r": 1,
            "Layer": 3,
            "text": "🦁",
            "text_color": "red"
        }
    elif isinstance(agent, Pollinator):
        portrayal = {
            "Shape": "circle",
            "Color": "yellow",
            "r": 1,
            "Layer": 4,
            "text": "🐝",
            "text_color": "yellow"
        }
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
        "initial_polinators": Slider(
            name="Número de Polinizadores",
            value=20,
            min_value=0,
            max_value=650,
            step=1,
            description="Escolha quantos polinizadores incluir no modelo",
        ),
        "plant_reproduction_rate": Slider(
            name="Taxa de Reprodução das Plantas",
            value=0.01,
            min_value=0,
            max_value=1,
            step=0.01,
            description="Escolha a taxa de reprodução das plantas",
        ),
        "herbivore_reproduction_rate": Slider(
            name="Taxa de Reprodução dos Herbívoros",
            value=0.5,
            min_value=0,
            max_value=10,
            step=0.1,
            description="Escolha a taxa de reprodução dos herbívoros",
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
