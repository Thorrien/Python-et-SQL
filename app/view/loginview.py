import getpass
from app.controllers.security import validate_email
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from datetime import datetime
from time import sleep
from rich.live import Live
import time

class Loginview:
    def __init__(self):
        pass

    def log(self):
        """
        Affiche l'interface d'authentification, recueille l'identifiant (email) et le mot de passe de l'utilisateur.
        Valide l'email avant de retourner les informations de connexion.

        Retourne:
        - Tuple (username, password): L'identifiant (email) et le mot de passe de l'utilisateur.

        Si l'email n'est pas valide, le programme se termine.
        """
        console = Console()
        title_text = Text("EpicEvent", style="bold white on green", justify="center")
        title_panel = Panel(Align.center(title_text), style="bold")
        console.print(title_panel)
        current_date = datetime.now().strftime("%d/%m/%Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        first_line = f"Service : -----{' ' * (console.width - len('Service : -----') - len(current_date))}{current_date}"
        console.print(first_line)
        second_line = f"[bold green]-----------@---------[/bold green]{' ' * (console.width - len("-----------@---------") - len(current_time))}{current_time}"
        console.print(second_line)
        console.rule("Authentification")
        console.print('Quel est votre Identifiant ? ')
        username = None
        username = input('email : ')
        if validate_email(username):
            password = getpass.getpass("Mot de passe: ")
            return username, password
        else:
            print("format d'email invalide")
            exit()
            
    def logtrue(self):
        """
        Affiche une animation indiquant que la connexion a été autorisée et que le chargement est en cours.
        Utilise une animation en temps réel pour centrer et faire défiler le texte sur l'écran.
        """
        console = Console()
        text = "Connection autorisé - Chargement en cours"
        console_width = console.width

        def aesthetic_animation(text, console_width):
            padding = " " * ((console_width - len(text)) // 2)
            aesthetic_text = padding + text
            return aesthetic_text

        with Live(console=console, refresh_per_second=20) as live:
            for i in range(len(text) + console_width):
                display_text = text[max(0, i - console_width):i]
                animated_text = aesthetic_animation(display_text, console_width)
                live.update(Text(animated_text, style="bold green"))
                time.sleep(0.01)

    def logfalse(self):
        """
        Affiche une animation indiquant que la connexion a été refusée et que le logiciel se ferme.
        Utilise une animation en temps réel pour centrer et faire défiler le texte sur l'écran.
        """
        console = Console()
        text = "Connection Refusée - Fermeture du logiciel"
        console_width = console.width

        def aesthetic_animation(text, console_width):
            padding = " " * ((console_width - len(text)) // 2)
            aesthetic_text = padding + text
            return aesthetic_text

        with Live(console=console, refresh_per_second=20) as live:
            for i in range(len(text) + console_width):
                display_text = text[max(0, i - console_width):i]
                animated_text = aesthetic_animation(display_text, console_width)
                live.update(Text(animated_text, style="bold red"))
                time.sleep(0.01)