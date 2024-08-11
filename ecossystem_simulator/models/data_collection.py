from mesa.datacollection import DataCollector as BaseDataCollector

class DataCollector(BaseDataCollector):
    def __init__(self, model_reporters=None, agent_reporters=None):
        super().__init__(model_reporters=model_reporters, agent_reporters=agent_reporters)
