from common import *
import socket
import logging
import threading

PORT = 5000

def log_init():
    global lg
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


def handle_game(game_id, player_1, player_2, game_cards, l):
    log(l, f"Game {game_id} | Started with {player_1.addr} and {player_2.addr}")
    game = Game(player_1, player_2, game_cards)
    game.start()
    log(l, f"Game {game_id} | Ended")

def start_server(l:bool = True):
    if l: log_init()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", PORT))
    s.listen()

    connections = []
    slots = 2
    game_id_incr = 0

    log(l, "Server started")

    while True:
        log(l, f"Game {game_id_incr} | Waiting for new connections... ({len(connections)}/{slots})")
        while len(connections) < slots:
            conn, addr = s.accept()
            connections.append((conn, addr))
            log(l, f"Game {game_id_incr} | Waiting for new connections... ({len(connections)}/{slots})")
        
        log(l, f"Game {game_id_incr} | Full")

        game_cards = Cards()
        player_1 = Player(1, *connections[0])
        player_2 = Player(2, *connections[1])

        thread = threading.Thread(target=handle_game, args=(game_id_incr, player_1, player_2, game_cards, l))
        thread.start()

        connections = []
        game_id_incr += 1

if __name__ == '__main__':
    start_server()