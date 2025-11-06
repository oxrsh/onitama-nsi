from common import *
from rich import print
import socket
import json

import os
os.system('cls' if os.name == 'nt' else 'clear')

def log_init():
    global lg
    import logging
    from rich.logging import RichHandler

    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()]
    )

    lg = logging.getLogger("rich")

def log(logging, msg, level='info'):
    if logging:
        if level=='info':
            lg.info(msg)
        elif level=='error':
            lg.error(msg)

def start_client(game_ip, game_port, l:bool=True):
    if l: log_init()

    log(l, "Searching a server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((game_ip, game_port))
    log(l, f"Server found ({game_ip}:{game_port})")
    log(l, f"Connected")

    game = None
    me = None
    player_id = "0"

    def envoi(conn, msg):
        conn.sendall(json.dumps(msg).encode())

    while True:
        data = s.recv(2048)
        if not data:
            break

        msg = json.loads(data.decode())

        if msg.get('type') == 'init':
            game = Game.from_dict(msg.get("game"))
            player_id = msg.get('player')

            me = game.player1 if player_id == "1" else game.player2

            log(l, f"You are {me}")
            log(l, "Waiting for your turn...")

            print(game.render(me))

        elif msg.get('type') == 'your_turn':
            while True:
                log(l, "It's your turn")

                me = game.player1 if player_id == "1" else game.player2

                selected_card = game.choose_card()
                from_pos = game.choose_piece()
                to_pos = game.choose_movement(selected_card, from_pos.pos, me)

                if not to_pos:
                    log(l, "No move is possible with this card and this piece.\nPress enter to retry...", 'error')
                    input()
                else:
                    envoi(s, {"type": "move", "card": selected_card.to_dict(), "piece": from_pos.to_dict(), "move": to_pos.to_dict()})
                    log(l, "Waiting for your turn...")
                    break

        elif msg.get('type') == 'update':
            # played = msg.get('played')

            # selected_card = Card.from_dict(played.get('card'))
            # selected_piece = Piece.from_dict(played.get('piece'))
            # selected_move = Pos.from_dict(played.get('move'))

            game = Game.from_dict(msg.get("game"))
            me = game.player1 if player_id == "1" else game.player2
            print(game.render(me))

        elif msg.get('type') == 'invalid_move':
            log(l, "This move is invalid. Please try again", 'error')

        elif msg.get('type') == 'game_over':
            winner = Player.from_dict(msg.get('winner'))
            log(l, f'Game over!\nWinner: {winner}')
            break

    log(l, "Press enter to close...")
    input()
    s.close()

if __name__ == '__main__':
    start_client()