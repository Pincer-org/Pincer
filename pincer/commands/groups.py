# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

class Group:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __hash__(self):
        return hash(self.name)


class SubGroup:
    def __init__(self, name: str, description: str, parent: Group):
        self.name = name
        self.description = description
        self.parent = parent

    def __hash__(self):
        return hash(self.name)
