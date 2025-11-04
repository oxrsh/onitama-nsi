from .pos import Pos
from .piece import Piece
from .card import Card
from .board import Board
from rich.prompt import Prompt
from rich.panel import Panel
from rich.columns import Columns
import json

class Player:
    """Représente un joueur de la partie"""
    def __init__(self, id: int, conn, addr, cards = []):
        if id not in [1, 2]:
            raise Exception("Player id must be 1 or 2")
        
        self.id = id
        self.conn = conn
        self.addr = addr
        self.cards = cards
    
    def __str__(self) -> str:
        return f"Player {self.id}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "cards": [c.to_dict() for c in self.cards]
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data.get('id'), None, None, [Card.from_dict(c) for c in data.get('cards')])
    
    def set_cards(self, *cards: Card):
        """Définit les cartes du joueur"""
        self.cards = list(cards)

    def get_pieces(self, board: Board) -> list[Piece]:
        """Récupère les pions de ce joueur depuis le plateau"""
        return board.get_pieces_by_player_id(self.id)

    def can_play(self, board: Board, card: Card, from_: Pos, to: Pos) -> tuple[bool, str]:
        """Vérifie si le coup demandé est légal"""
        if card not in self.cards:
            return False, "illegal_card" # Le joueur n'a pas la carte donnée en sa possession

        if not card.check_if_possible(from_, to, True if self.id == 2 else False):
            return False, "illegal_move" # Le coup n'est pas possible avec la carte donnée
        
        piece = board.get_piece(from_)
        to_value = board.get_piece(to)

        if not piece//10 == self.id:
            return False, "piece_not_owned" # La case de départ n'est pas possédée par le joueur
        if not to_value//10 != self.id:
            return False, "destination_occupied" # La case d'arrivée est déjà prise par un pion allié

        return True, ""
    
    def play(self, board: Board, card: Card, from_: Pos, to: Pos) -> tuple[bool, str]:
        """Effectue un coup (validation + exécution)"""
        valid, msg = self.can_play(board, card, from_, to)
        if not valid:
            return False, msg
        
        board.move_piece(from_, to)
        return True, "success"
    
    def ask(self, question:str, choices: list):
        """Demande une entrée au joueur (inutile si sur même appareil, utile pour jeu en ligne)"""
        return Prompt.ask(question, choices=choices, case_sensitive=False)
    
    def render_cards(self, opponent=False):
        """Effectue le rendu des cartes"""
        rendered = []
        for c in self.cards:
            rendered.append(c.render(opponent))

        color = 'red' if opponent else 'green'

        return Panel.fit(Columns(rendered), title=f"[{color} bold]{self}'s cards", border_style=color)
    
    def json_send(self, msg) -> bool:
        """Envoie un message JSON à une connexion. True si envoyé, False si echec"""
        try:
            self.conn.sendall(json.dumps(msg).encode())
            return True
        except:
            return False
        
    def json_recv(self) -> object | None:
        """Reçoit un message JSON. Renvoie l'objet ou None si echec/msg vide"""
        try:
            mdata = self.conn.recv(2048)
            if not mdata:
                return None
            msg = json.loads(mdata.decode())
            return msg
        except:
            return None