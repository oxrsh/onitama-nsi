from .card import Card
from .pos import Pos
from rich import print
from typing import Iterator

class Cards:
    """Représente un paquet de cartes"""
    def __init__(self):
        self.cards = [
            Card("Boeuf",       [Pos(-1, 0), Pos(0, 1), Pos(1, 0)]),
            Card("Cheval",      [Pos(-1, 0), Pos(0, -1), Pos(1, 0)]),

            Card("Coq",         [Pos(-1, 1), Pos(0, -1), Pos(0, 1), Pos(1, -1)]),
            Card("Oie",         [Pos(-1, -1), Pos(0, -1), Pos(0, 1), Pos(1, 1)]),

            Card("Cobra",       [Pos(-1, 1), Pos(1, 1), Pos(0, -1)]),
            Card("Anguille",    [Pos(-1, -1), Pos(1, -1), Pos(0, 1)]),

            Card("Lapin",       [Pos(1, -1), Pos(-1, 1), Pos(0, 2)]),
            Card("Grenouille",  [Pos(1, 1), Pos(-1, -1), Pos(0, -2)]),

            Card("Renard",      [Pos(-1, 1), Pos(0, 1), Pos(1, 1)]),
            Card("Chien",       [Pos(-1, -1), Pos(0, -1), Pos(1, -1)]),

            Card("Panda",       [Pos(-1, 0), Pos(-1, 1), Pos(1, -1)]),
            Card("Ours",        [Pos(-1, 0), Pos(-1, -1), Pos(1, 1)]),

            Card("Souris",      [Pos(-1, 0), Pos(0, 1), Pos(1, -1)]),
            Card("Rat",         [Pos(0, -1), Pos(-1, 0), Pos(1, 1)]),

            Card("Elephant",    [Pos(-1, -1), Pos(0, -1), Pos(-1, 1), Pos(0, 1)]),
            Card("Crabe",       [Pos(-1, 0), Pos(0, 2), Pos(0, -2)]),
            Card("Dragon",      [Pos(-1, -2), Pos(1, -1), Pos(1, 1), Pos(-1, 2)]),
            Card("Singe",       [Pos(1, 1), Pos(1, -1), Pos(-1, -1), Pos(-1, 1)]),
            Card("Kirin",       [Pos(-2, -1), Pos(2, 0), Pos(-2, 1)]),
            Card("Phenix",      [Pos(0, -2), Pos(-1, -1), Pos(-1, 1), Pos(0, 2)]),
            Card("Tortue",      [Pos(0, -2), Pos(1, -1), Pos(1, 1), Pos(0, 2)]),
        ]

        self.cards_default = [
            Card("Boeuf",       [Pos(-1, 0), Pos(0, 1), Pos(1, 0)]),
            Card("Cheval",      [Pos(-1, 0), Pos(0, -1), Pos(1, 0)]),

            Card("Coq",         [Pos(-1, 1), Pos(0, -1), Pos(0, 1), Pos(1, -1)]),
            Card("Oie",         [Pos(-1, -1), Pos(0, -1), Pos(0, 1), Pos(1, 1)]),

            Card("Cobra",       [Pos(-1, 1), Pos(1, 1), Pos(0, -1)]),
            Card("Anguille",    [Pos(-1, -1), Pos(1, -1), Pos(0, 1)]),

            Card("Lapin",       [Pos(1, -1), Pos(-1, 1), Pos(0, 2)]),
            Card("Grenouille",  [Pos(1, 1), Pos(-1, -1), Pos(0, -2)]),

            Card("Elephant",    [Pos(-1, -1), Pos(0, -1), Pos(-1, 1), Pos(0, 1)]),
            Card("Grue",        [Pos(1, -1), Pos(1, 1), Pos(-1, 0)]),

            Card("Crabe",       [Pos(-1, 0), Pos(0, 2), Pos(0, -2)]),
            Card("Sanglier",    [Pos(-1, 0), Pos(0, 1), Pos(0, -1)]),
            Card("Dragon",      [Pos(-1, -2), Pos(1, -1), Pos(1, 1), Pos(-1, 2)]),
            Card("Singe",       [Pos(1, 1), Pos(1, -1), Pos(-1, -1), Pos(-1, 1)]),
            Card("Mante",       [Pos(-1, -1), Pos(1, 0), Pos(-1, 1)]),
            Card("Tigre",       [Pos(-2, 0), Pos(1, 0)]),
        ]

        self.extension_cards = [
            Card("Renard",      [Pos(-1, 0), Pos(-1, 1), Pos(1, -1)]), ###
            Card("Chien",       [Pos(-1, 0), Pos(-1, 1), Pos(1, -1)]), ###

            Card("Panda",       [Pos(-1, 0), Pos(-1, 1), Pos(1, -1)]),
            Card("Ours",        [Pos(-1, 0), Pos(-1, -1), Pos(1, 1)]),

            Card("Hydrophinae", [Pos(-1, 0), Pos(0, 2), Pos(1, -1)]),
            Card("Vipere",      [Pos(0, -2), Pos(-1, 0), Pos(1, 1)]),

            Card("Souris",      [Pos(-1, 0), Pos(0, 1), Pos(1, -1)]),
            Card("Rat",         [Pos(0, -1), Pos(-1, 0), Pos(1, 1)]),

            Card("Tanuki",      [Pos(-1, -2), Pos(-1, 0), Pos(1, 1)]), ### 
            Card("Iguane",      [Pos(-1, -2), Pos(-1, 0), Pos(1, 1)]),

            Card("Zibeline",    [Pos(0, -2), Pos(1, -1), Pos(-1, 1)]),
            Card("Loutre",      [Pos(0, -2), Pos(1, -1), Pos(-1, 1)]), ###

            Card("Chèvre",      [Pos(-1, -1), Pos(0, 1), Pos(1, 0)]), ###
            Card("Mouton",      [Pos(-1, -1), Pos(0, 1), Pos(1, 0)]),

            Card("Girafe",      [Pos(-2, -1), Pos(2, 0), Pos(-2, 1)]), ###
            Card("Kirin",       [Pos(-2, -1), Pos(2, 0), Pos(-2, 1)]),
            Card("Phenix",      [Pos(0, -2), Pos(-1, -1), Pos(-1, 1), Pos(0, 2)]),
            Card("Tortue",      [Pos(-2, -1), Pos(2, 0), Pos(-2, 1)]), ###
        ]

    def __iter__(self) -> Iterator[Card]:
        return iter(self.cards)

    def get_by_name(self, name: str) -> Card | None:
        """Obtenir une carte par son nom"""
        return next((c for c in self.cards if c.name == name), None)
    
    def render_all(self):
        """Effectuer le rendu de toutes les cartes (debug)"""
        for card in self.cards:
            print(card.render())