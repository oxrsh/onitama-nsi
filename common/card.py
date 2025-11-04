from .pos import Pos
from .board import Board
from rich import print
from rich.panel import Panel
from rich.table import Table

class Card:
    """Représente une carte de jeu"""
    def __init__(self, name: str, movements: list[Pos]):
        self.name = name
        self.movements = movements

    def __eq__(self, other):
        return (
            isinstance(other, Card)
            and self.name == other.name
            and self.movements == other.movements
        )

    def to_dict(self):
        return {
            "name": self.name,
            "movements": [m.to_dict() for m in self.movements]
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], [Pos.from_dict(m) for m in data["movements"]])

    def check_if_possible(self, from_: Pos, to: Pos, inverted: bool = False) -> bool:
        """Vérifie si un mouvement donné est possible avec une carte donnée"""
        delta_li = to.li - from_.li
        delta_co = to.co - from_.co

        if inverted:
            delta_li *= -1
            delta_co *= -1

        return Pos(delta_li, delta_co) in self.movements
    
    def get_possible_movements(self, board: Board, playerid: int, position: Pos) -> list[Pos]:
        """Donne une liste de mouvements possibles avec une carte et selon la position du joueur et la situation du jeu"""
        if playerid == 1: all_pos = [position + m for m in self.movements]
        elif playerid == 2: all_pos = [position + m.invert() for m in self.movements]
        
        existing_pos = list(filter(lambda x: x.exists(), all_pos))
        possible_pos = list(filter(lambda x: board.get_piece(x)//10 != playerid, existing_pos))
        return possible_pos

    def render(self, inverted=False) -> Panel:
        """Effectue le rendu de la carte (affichage dans la console)"""
        grid = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

        for m in self.movements:
            if -2 <= m.li <= 2 and -2 <= m.co <= 2 and not (m.li == 0 and m.co == 0):
                x = 4-(m.li+2) if inverted else (m.li+2)
                y = 4-(m.co+2) if inverted else (m.co+2)
                grid[x][y] = 1

        table = Table(
            show_header=False, 
            show_edge=True, 
            show_lines=True,
            box=__import__('rich.box').box.SQUARE,
            padding=0
        )
        
        for _ in range(5):
            table.add_column(justify="center", width=3)
        
        for li in grid:
            row = []
            for co in li:
                match co:
                    case 0:
                        char = ""
                    case 1:
                        char = "[green]O[/green]"
                    case 2:
                        char = "[yellow bold]X[/yellow bold]"
                row.append(char)
            table.add_row(*row)

        return Panel.fit(table, title=f"[white bold]{self.name}", border_style="white")