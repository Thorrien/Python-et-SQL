from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.table import Table
from datetime import datetime
from time import sleep
import re
from rich.columns import Columns
import calendar
import locale


class View :

    def ascii(self):
        rprint("[bold green]      ___           ___                     ___           ___                        ___           ___                 [/bold green]")
        rprint("[bold green]     /  /\         /  /\      ___          /  /\         /  /\          ___         /  /\         /__/\          ___   [/bold green]")
        rprint("[bold green]    /  /:/_       /  /::\    /  /\        /  /:/        /  /:/_        /__/\       /  /:/_        \  \:\        /  /\  [/bold green]")
        rprint("[bold green]   /  /:/ /\     /  /:/\:\  /  /:/       /  /:/        /  /:/ /\       \  \:\     /  /:/ /\        \  \:\      /  /:/  [/bold green]")
        rprint("[bold green]  /  /:/ /:/_   /  /:/~/:/ /__/::\      /  /:/  ___   /  /:/ /:/_       \  \:\   /  /:/ /:/_   _____\__\:\    /  /:/   [/bold green]")
        rprint("[bold green] /__/:/ /:/ /\ /__/:/ /:/  \__\/\:\__  /__/:/  /  /\ /__/:/ /:/ /\  ___  \__\:\ /__/:/ /:/ /\ /__/::::::::\  /  /::\   [/bold green]")
        rprint("[bold green] \  \:\/:/ /:/ \  \:\/:/      \  \:\/\ \  \:\ /  /:/ \  \:\/:/ /:/ /__/\ |  |:| \  \:\/:/ /:/ \  \:\~~\~~\/ /__/:/\:\  [/bold green]")
        rprint("[bold green]  \  \::/ /:/   \  \::/        \__\::/  \  \:\  /:/   \  \::/ /:/  \  \:\|  |:|  \  \::/ /:/   \  \:\  ~~~  \__\/  \:\ [/bold green]")
        rprint("[bold green]   \  \:\/:/     \  \:\        /__/:/    \  \:\/:/     \  \:\/:/    \  \:\__|:|   \  \:\/:/     \  \:\           \  \:\ [/bold green]")
        rprint("[bold green]    \  \::/       \  \:\       \__\/      \  \::/       \  \::/      \__\::::/     \  \::/       \  \:\           \__\/[/bold green]")
        rprint("[bold green]     \__\/         \__\/                   \__\/         \__\/           ~~~~       \__\/         \__\/                [/bold green]")
        print("")
        print("")
        print("")

    def title(self, user):
        console = Console()
        title_text = Text("EpicEvent", style="bold white on green", justify="center")
        title_panel = Panel(Align.center(title_text), style="bold")
        console.print(title_panel)
        current_date = datetime.now().strftime("%d/%m/%Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        first_line = f"id : 12564{' ' * (console.width - len('id : 12564') - len(current_date))}{current_date}"
        console.print(first_line)
        second_line = f"[bold green]{user.email}[/bold green]{' ' * (console.width - len(user.email) - len(current_time))}{current_time}"
        console.print(second_line)

    def logtrue(self, user, text):
        self.title(user)
        console = Console()
        console.rule(f"Bienvenue {user.nom}")
        console.print("")
        console.print(f"Message de la direction : {text}")
        console.print("")
        sleep(3)
        
    #def logcontrats(self, user):
     #   self.title(user)
     #   console = Console()
     #   console.rule("Gestion des contrats")
     #   console.print("")
    #  console.print("")

    def menuprincipalgestion(self, user):
        console = Console()
        console.rule("Menu principal")
        console.print("")
        table = Table(box=None)
        table.add_column("Choix", justify="center", style="green", no_wrap=True)
        table.add_column("Description", justify="left", style="white")
        
        table.add_row("", "")
        if user.authorisation('Admin') or user.authorisation('Gestion'):
            table.add_row("US", "Gérer les comptes utilisateurs")
        else:
            table.add_row("[red][strike]US[/strike][/red]", "[red]Gérer les comptes utilisateurs[/red]🔒")
        if user.authorisation('Admin') or user.authorisation('Gestion') or user.authorisation('Sale') or user.authorisation('Support'):
            table.add_row("CL", "Gérer les clients")
        else:
            table.add_row("[red][strike]CL[/red][/strike]", "[red]Gérer les clients[/red]🔒")
        if user.authorisation('Admin') or user.authorisation('Gestion') or user.authorisation('Sale') or user.authorisation('Support'):
            table.add_row("CO", "Gérer les contrats")
        else:
            table.add_row("[red][strike]CO[/red][/strike]", "[red]Gérer les contrats[/red]🔒")
        if user.authorisation('Admin') or user.authorisation('Gestion') or user.authorisation('Sale') or user.authorisation('Support'):
            table.add_row("EV", "Gérer les Events")
        else:
            table.add_row("[red][strike]EV[/red][/strike]", "[red]Gérer les Events[/red]🔒")
        if  user.authorisation('Gestion'):
            table.add_row("MO", "Modifier le message d'accueil")
        else:
            table.add_row("[red][strike]MO[/strike][/red]", "[red]Modifier le message d'accueil[/red]🔒")
        if  user.authorisation('Gestion'):
            table.add_row("SU", "Gestion des éléments non attribués")
        else:
            table.add_row("[red][strike]SU[/strike][/red]", "[red]Gestion des éléments non attribués[/red]🔒")
        table.add_row("QUIT", "Quitter")
        console.print(table)
        if user.authorisation('Gestion') :
            invalid_choix = []
            valid_choix = ["US", "CO", "EV", "CL", "MO", "SU", "QUIT"]
        elif user.authorisation('Admin') :
            invalid_choix = [ "MO", "SU"]
            valid_choix = ["US", "CO", "EV", "CL", "QUIT"]
        else:
            invalid_choix = ["US", "MO", "SU"]
            valid_choix = ["CO", "EV", "CL", "QUIT"]
            
        while True:
            choix = input('Votre choix : ')
            if choix in valid_choix:
                return choix
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")

    def notautorized(self, user):
        console = Console()
        console.rule(f"[red] {user.nom}, vous n'avez pas les droits permettant d'utiliser cette fonctionnalité[/red]")
        sleep(2)

    def base(self):
        console = Console()
        console.rule("Fin de la page")

    def getText(self, user) :
        if user.authorisation("Gestion"):
            console = Console()
            console.rule(f"Création d'un nouveau message de la direction")
            console.print("")
            console.print("Votre message de la direction : ")
            data = str(input('==>'))
            return data
