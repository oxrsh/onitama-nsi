from client import start_client
from server import start_server
from rich import print
from rich.prompt import Prompt
from rich.panel import Panel
import logging
import threading
from rich.logging import RichHandler
import urllib.request

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

log = logging.getLogger("rich")

client_type = Prompt.ask("Do you want to host or join a game?", case_sensitive=False, choices=["host", "join"])
if client_type == 'host':
    log.info("Hosting game...")
    log.info("Starting server...")
    x = threading.Thread(target=start_server, args=(True,))
    x.start()

    external_ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
    port = 9267

    log.info(f"Your IP: {external_ip} Port: {port}")

    start_client('127.0.0.1', port)

elif client_type == 'join':
    game_ip = Prompt.ask("Enter game IP address", default="127.0.0.1")
    game_port = Prompt.ask("Enter game port", default='9267')

    start_client(game_ip, int(game_port))