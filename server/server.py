from common import *
import socket
import logging
import threading
from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

log = logging.getLogger("rich")

PORT = 5000

def handle_game(game_id, player_1, player_2, game_cards):
    log.info(f"Game {game_id} | Started with {player_1.addr} and {player_2.addr}")
    game = Game(player_1, player_2, game_cards)
    game.start()
    log.info(f"Game {game_id} | Ended")

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", PORT))
    s.listen()

    connections = []
    slots = 2
    game_id_incr = 0

    log.info("Server started")

    while True:
        log.info(f"Game {game_id_incr} | Waiting for new connections... ({len(connections)}/{slots})")
        while len(connections) < slots:
            conn, addr = s.accept()
            connections.append((conn, addr))
            log.info(f"Game {game_id_incr} | Waiting for new connections... ({len(connections)}/{slots})")
        
        log.info(f"Game {game_id_incr} | Full")

        game_cards = Cards()
        player_1 = Player(1, *connections[0])
        player_2 = Player(2, *connections[1])

        thread = threading.Thread(target=handle_game, args=(game_id_incr, player_1, player_2, game_cards))
        thread.start()

        connections = []
        game_id_incr += 1

if __name__ == '__main__':
    start_server()