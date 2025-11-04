from .pos import Pos
from .piece import Piece
from rich import print
from rich.panel import Panel
from rich.table import Table


class Board:
    """Représente un plateau de jeu 5x5"""
    def __init__(self, grid = None):
        self.grid = [
            [20, 20, 21, 20, 20],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [10, 10, 11, 10, 10]
        ] if grid == None else grid

    def to_dict(self):
        return {
            "grid": self.grid,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["grid"])

    def get_piece(self, pos: Pos) -> int:
        """Obtenir une pièce à des coordonnées"""
        return self.grid[pos.li][pos.co]
    
    def set_piece(self, pos: Pos, value: int):
        """Définir une pièce à des coordonnées"""
        self.grid[pos.li][pos.co] = value
        
    def move_piece(self, from_: Pos, to: Pos):
        """Déplace une pièce sur le plateau"""
        piece = self.get_piece(from_)
        self.set_piece(from_, 0)
        self.set_piece(to, piece)

    def get_pieces_by_player_id(self, playerid: int) -> list[Piece]:
        """Obtenir toutes les pièces d'un joueur"""
        pieces = []
        for i, li in enumerate(self.grid):
            for j, co in enumerate(li):
                if co // 10 == playerid:
                    pieces.append(Piece(Pos(i, j), co%10))
        return pieces

    def render(self, invert=False, movements=[]) -> Panel:
        """Effectue le rendu du plateau"""
        table = Table(
            show_header=False, 
            show_edge=True, 
            show_lines=True,
            box=__import__('rich.box').box.SQUARE,
            padding=0
        )
        
        for _ in range(5):
            table.add_column(justify="center", width=3)

        grid = reversed(self.grid) if invert else self.grid
        
        for i, li in enumerate(grid):
            row = []
            rli = reversed(li) if invert else li
            for j, co in enumerate(rli):
                char = ""
                if Pos(4-i if invert else i, 4-j if invert else j) in movements:
                    char += "[on green]"
                
                match co:
                    case 0:
                        if Pos(4-i if invert else i, 4-j if invert else j) in movements:
                            char += "[green].[/]"
                    case 10:
                        char += "[blue]o[/]"
                    case 11:
                        char += "[blue bold]O[/]"
                    case 20:
                        char += "[red]x[/]"
                    case 21:
                        char += "[red bold]X[/]"

                row.append(char)
            table.add_row(*row)
        return Panel.fit(table, title="[tan bold]Board", border_style="tan")