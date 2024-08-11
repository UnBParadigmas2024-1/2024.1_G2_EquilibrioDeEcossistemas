from mesa.visualization.ModularVisualization import ModularServer
from ecossystem_simulator.server.visualization import agent_portrayal, create_sliders
from ecossystem_simulator.models.ecosystem_model import EcosystemModel
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.modules import TextElement

class SeasonTextElement(TextElement):
    def render(self, model):
        colors = {
            "Primavera": "green",
            "Verão": "orange",
            "Outono": "brown",
            "Inverno": "blue"
        }

        color = colors.get(model.season, "black")

        return (
            f'<span style="color: black; font-weight: bold; font-size: 20px;">Estação Atual:</span> '
            f'<span style="color: {color}; font-weight: bold; font-size: 20px;">{model.season}</span>'
        )

def run():
    grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
    chart = ChartModule(
        [{"Label": "Plantas", "Color": "green"},
         {"Label": "Herbívoros", "Color": "blue"},
         {"Label": "Carnívoros", "Color": "red"}]
    )

    season_text = SeasonTextElement()

    model_params = create_sliders()

    server = ModularServer(
        EcosystemModel,
        [season_text, grid, chart],
        "Simulador de Ecossistema",
        model_params
    )

    server.port = 8521
    server.launch()
