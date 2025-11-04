from .pos import Pos
from .piece import Piece
from .card import Card
from .cards import Cards
from .player import Player
from .board import Board
from rich import print
from rich.panel import Panel
from rich.console import Group
from rich.columns import Columns

class Game:
    """Représente une partie"""
    def __init__(self, player1: Player, player2: Player, cards: Cards):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.cards = cards

        import random
        all_cards = list(cards.cards)
        random.shuffle(all_cards)
        player1.set_cards(*all_cards[:2])
        player2.set_cards(*all_cards[2:4])

        self.neutral_card = all_cards[4]

    def to_dict(self):
        return {
            "board": self.board.to_dict(),
            "player_1": self.player1.to_dict(),
            "player_2": self.player2.to_dict(),
            "current_player": self.current_player.to_dict(),
            "neutral_card": self.neutral_card.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data):
        instance = cls.__new__(cls)

        instance.board = Board.from_dict(data["board"])
        instance.player1 = Player.from_dict(data["player_1"])
        instance.player2 = Player.from_dict(data["player_2"])
        instance.current_player = Player.from_dict(data["current_player"])
        instance.neutral_card = Card.from_dict(data["neutral_card"])
        instance.cards = Cards()

        return instance

    def switch_turn(self):
        """Change le joueur qui joue (changement de tour)"""
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def is_game_over(self) -> tuple[bool, Player | None]:
        """Vérifie victoire (Master capturé ou atteint temple adverse)"""
        # Vérifier si un Master a été capturé
        p1_pieces = self.board.get_pieces_by_player_id(self.player1.id)
        p2_pieces = self.board.get_pieces_by_player_id(self.player2.id)
        
        p1_has_master = any(p.level == 1 for p in p1_pieces)
        p2_has_master = any(p.level == 1 for p in p1_pieces)
        
        if not p1_has_master:
            return True, self.player2
        if not p2_has_master:
            return True, self.player1
        
        # Vérifier si un Master a atteint le temple adverse
        for piece in p1_pieces:
            if piece.level == 1 and piece.pos.li == 0 and piece.pos.co == 2:  # Temple P2
                return True, self.player1
        
        for piece in p2_pieces:
            if piece.level == 1 and piece.pos.li == 4 and piece.pos.co == 2:  # Temple P1
                return True, self.player2
        
        return False, None
    
    def exchange_card(self, used_card: Card):
        """Effectue l'échange de carte après avoir joué (entre joueur et milieu)"""
        self.current_player.cards.remove(used_card)
        self.current_player.cards.append(self.neutral_card)
        self.neutral_card = used_card

    def choose_card(self) -> Card:
        """Demande à l'utilisateur de choisir une carte"""
        card_names = [c.name for c in self.current_player.cards]
        card_name = self.current_player.ask("Which card are you using?", card_names)
        selected_card = next(c for c in self.current_player.cards if c.name == card_name)
        return selected_card
    
    def choose_piece(self) -> Piece:
        """Demande à l'utilisateur de choisir une pièce"""
        pieces = self.current_player.get_pieces(self.board)
        pieces_txt = "\n".join([
                f"  {i+1}. {'Master' if piece.level == 1 else 'Pawn'}: {piece.pos}"
                for i, piece in enumerate(pieces)
            ])

        from_input = self.current_player.ask(f"{self.current_player}'s pieces:\n{pieces_txt}\nWhich piece?", [str(i+1) for i in range(len(pieces))])
        from_pos = pieces[int(from_input)-1]
        return from_pos
    
    def choose_movement(self, selected_card: Card, from_pos: Pos, player: Player) -> Pos | None:
        """Demande à l'utilisateur de choisir un mouvement de sa carte"""
        possible_pos = selected_card.get_possible_movements(self.board, self.current_player.id, from_pos)

        if len(possible_pos) == 0:
            return None
        elif len(possible_pos) == 1:
            return possible_pos[0]

        possible_txt = "\n".join([
                f"  {i+1}. {movement}" for i, movement in enumerate(possible_pos)
            ])
        rendered_board = self.board.render(True if player == self.player2 else False, possible_pos)
        print(rendered_board)
        to_input = self.current_player.ask(f"\n{possible_txt}\n", [str(i+1) for i in range(len(possible_pos))])
        to_pos = possible_pos[int(to_input)-1]
        return to_pos

    def check_movement(self, selected_card: Card, from_pos: Pos, to_pos: Pos) -> bool:
        possible_pos = selected_card.get_possible_movements(self.board, self.current_player.id, from_pos)
        return to_pos in possible_pos

    def play_turn(self, card: Card, from_: Pos, to: Pos) -> tuple[bool, str]:
        """Joue un tour"""
        success, msg = self.current_player.play(self.board, card, from_, to)

        if success:
            self.exchange_card(card)
            game_over, winner = self.is_game_over()
            if game_over:
                return True, f"{winner} wins!"
            
            self.switch_turn()
            return True, "success"
        
        return False, msg
    
    def render(self, player: Player, possible_movements: list[Pos] = []) -> Panel:
        """Effectue un rendu du jeu (plateau + cartes)"""
        board_rendered = self.board.render(True if player == self.player2 else False, possible_movements)
        player_cards_rendered = player.render_cards(False)
        opponent_cards_rendered = self.player1.render_cards(True) if player == self.player2 else self.player2.render_cards(True)
        neutral_card_rendered = self.neutral_card.render()

        group = Group(opponent_cards_rendered, Panel.fit(Columns([board_rendered, neutral_card_rendered])), player_cards_rendered)

        return Panel.fit(
            group,
            title="[white bold]Game",
            subtitle=f"{self.current_player}'s turn",
            border_style="white"
        )

    def start(self):
        msg_p1 = {
            "type": "init",
            "player": '1',
            "game": self.to_dict()
        }

        msg_p2 = {
            "type": "init",
            "player": '2',
            "game": self.to_dict()
        }

        self.player1.json_send(msg_p1)
        self.player2.json_send(msg_p2)

        try:
            while True:
                self.current_player.json_send({"type": "your_turn"})
                msg = self.current_player.json_recv()
                if not msg:
                    break

                if msg.get('type') == 'move':
                    selected_card = Card.from_dict(msg.get('card'))
                    selected_piece = Piece.from_dict(msg.get('piece'))
                    selected_move = Pos.from_dict(msg.get('move'))

                    success, msg = self.play_turn(selected_card, selected_piece.pos, selected_move)

                    if success:
                        reply = {
                            "type": "update",
                            "played": {"card": selected_card.to_dict(), "piece": selected_piece.to_dict(), "move": selected_move.to_dict()},
                            "game": self.to_dict()
                        }
                        for player in [self.player1, self.player2]:
                            player.json_send(reply)

                    else:
                        self.current_player.json_send({"type": "invalid_move", "msg": msg})

                game_over, winner = self.is_game_over()
                if game_over:
                    for player in [self.player1, self.player2]:
                        player.json_send({"type": "game_over", "winner": winner.to_dict()})
                    break
        except KeyboardInterrupt:
            print("\n[bold red]Game stopped.")

        for player in [self.player1, self.player2]:
            player.conn.close()
