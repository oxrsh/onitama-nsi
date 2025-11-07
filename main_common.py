from client import start_client
from server import start_server
import threading
import urllib.request
from rich import print
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.console import Console
console = Console()
console.screen()

def main():
    client_type = Prompt.ask("Do you want to host or join a game?", case_sensitive=False, choices=["host", "join"])
    if client_type == 'host':
        print("Hosting game...")
        server_type = Prompt.ask("Do you want to play in local or online?", choices=["local", "online"], case_sensitive=False)
        port = IntPrompt.ask("Which port do you want to use?", default=9267)
        print("Starting server...")

        if server_type == 'online':
            confirmation = Confirm.ask(f"[yellow bold]WARNING! For online use, you MUST open port {port} TCP on your router. Please make sure it’s done.")
            if not confirmation: return
            external_ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
            print(f"Your IP: {external_ip} Port: {port}")

        play_again = True
        while play_again:
            x = threading.Thread(target=start_server, args=('0.0.0.0', port, True, True))
            x.start()
            start_client('127.0.0.1', port, False)
            play_again = Confirm.ask("Play again?")

    elif client_type == 'join':
        game_ip = Prompt.ask("Enter game IP address", default="127.0.0.1")
        game_port = IntPrompt.ask("Enter game port", default=9267)

        play_again = True
        while play_again:
            x = threading.Thread(target=start_server, args=('0.0.0.0', port, True, True))
            x.start()
            start_client(game_ip, game_port, False)
            play_again = Confirm.ask("Play again?")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[bold red]Stopped succesfully.')