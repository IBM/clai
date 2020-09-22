# pylint: disable=too-few-public-methods
class OrchestratorDescriptor:
    def __init__(self, name: str, exclude: bool, description: str):
        self.name = name
        self.exclude = exclude
        self.description = description
