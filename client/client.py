from common import *
from rich import print
import socket
import json
import logging
from rich.logging import RichHandler

HOST = '127.0.0.1'
PORT = 5000

import os
os.system('cls' if os.name == 'nt' else 'clear')

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

log = logging.getLogger("rich")

def start_client():
    log.info("Searching a server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    log.info(f"Server found ({HOST}:{PORT})")
    log.info(f"Connected")

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

            log.info(f"You are {me}")
            log.info("Waiting for your turn...")

            print(game.render(me))

        elif msg.get('type') == 'your_turn':
            while True:
                log.info("It's your turn")

                me = game.player1 if player_id == "1" else game.player2

                selected_card = game.choose_card()
                from_pos = game.choose_piece()
                to_pos = game.choose_movement(selected_card, from_pos.pos, me)

                if not to_pos:
                    log.error("No move is possible with this card and this piece.\nPress enter to retry...")
                    input()
                else:
                    envoi(s, {"type": "move", "card": selected_card.to_dict(), "piece": from_pos.to_dict(), "move": to_pos.to_dict()})
                    log.info("Waiting for your turn...")
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
            log.error("This move is invalid. Please try again")

        elif msg.get('type') == 'game_over':
            winner = Player.from_dict(msg.get('winner'))
            log.info(f'Game over!\nWinner: {winner}')
            break

    log.info("Press enter to close...")
    input()
    s.close()

if __name__ == '__main__':
    start_client()