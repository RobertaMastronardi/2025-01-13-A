from dataclasses import dataclass


@dataclass
class Node:
    GeneID: str
    Localization: str
    Essential: str

    def __hash__(self):
        return hash(self.GeneID)

    def __str__(self):
        return f'{self.GeneID}'



