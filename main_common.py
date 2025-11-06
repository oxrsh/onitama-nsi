from client import start_client
from server import start_server
import logging
import threading
import urllib.request
from rich import print
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.logging import RichHandler

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
    server_type = Prompt.ask("Do you want to play in local or online?", choices=["local", "online"], case_sensitive=False)
    port = IntPrompt.ask("Which port do you want to use?", default=9267)
    log.info("Starting server...")

    if server_type == 'local':
        x = threading.Thread(target=start_server, args=('0.0.0.0', port, True))
        x.start()
    elif server_type == 'online':
        confirmation = Confirm.ask(f"[yellow bold]WARNING! For online use, you MUST open port {port} TCP on your router. Please make sure it’s done.")
        if confirmation:
            external_ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
            x = threading.Thread(target=start_server, args=('0.0.0.0', port, True))
            x.start()

            log.info(f"Your IP: {external_ip} Port: {port}")
        else:
            log.info("Server started in local")
            x = threading.Thread(target=start_server, args=('127.0.0.1', port, True))
            x.start()

    start_client('127.0.0.1', port, False)

elif client_type == 'join':
    game_ip = Prompt.ask("Enter game IP address", default="127.0.0.1")
    game_port = Prompt.ask("Enter game port", default='9267')

    start_client(game_ip, int(game_port), False)