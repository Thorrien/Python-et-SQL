from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from datetime import datetime
from time import sleep
from rich.columns import Columns


class View :
    def __init__(self):
        pass
    
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
        
    def login(self):
       pass
   
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

    
    def logtrue(self, user):
        self.title(user)
        console = Console()
        console.rule(f"Bienvenue {user.nom}")
        console.print("")
        console.print("Message de la direction : Nous vous informons que le pot de départ de M. Chauvin aura lieu le 19 septembre 2024 en salle 25A. À cette occasion, la direction présentera son successeur, M. Martin. Nous comptons sur votre présence pour partager ce moment convivial.")
        console.print("")
        sleep(3)
        
    def logcontrats(self, user):
        self.title(user)
        console = Console()
        console.rule("Gestion des contrats")
        console.print("")
        console.print("")

    def menuprincipalgestion(self, user):
        console = Console()
        console.rule("Menu principal")
        console.print("")
        table = Table(box=None)
        table.add_column("Choix", justify="center", style="green", no_wrap=True)
        table.add_column("Description", justify="left", style="white")
        
        table.add_row("", "")
        table.add_row("US", "Gérer les comptes utilisateurs")
        table.add_row("CO", "Gérer les contrats")
        table.add_row("EV", "Gérer les Events")
        table.add_row("MO", "Modifier le message d'accueil")
        table.add_row("QUIT", "Quitter")
        console.print(table)
        valid_choix = ["US", "CO", "EV", "MO", "QUIT"]
        while True:
            choix = input('Votre choix : ')
            if choix in valid_choix:
                return choix
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")
    
    def logutilisateurs(self, user, users):
        console = Console()
        console.rule("Comptes utilisateurs")
        console.print("") 

        third = len(users) // 3
        first_third = users[:third]
        second_third = users[third:2*third]
        third_third = users[2*third:]
        liste_choix = []
        
        def create_table(users):
            table = Table(box=None)
            table.add_column("Id", justify="center", style="green", no_wrap=True)
            table.add_column("Nom", justify="left", style="white")
            table.add_column("Role", justify="left", style="white")
            table.add_row("", "")
            for usersolo in users:
                table.add_row(str(usersolo['user_id']), usersolo['user_name'], usersolo['role_name'])
                liste_choix.append(str(usersolo['user_id']))
            
            return table

        table1 = create_table(first_third)
        table2 = create_table(second_third)
        table3 = create_table(third_third)

        console.print(Columns([table1, table2, table3], padding=(0, 10)))
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))
        
        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="center", style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        
        tablechoix.add_row("", "")
        tablechoix.add_row("CR", "Créer un nouvel utilisateur")
        tablechoix.add_row("A<id>", "Afficher le détail d'un utilisateur <id>")
        tablechoix.add_row("M<id>", "Modifier un élément d'un utilisateur <id>")
        tablechoix.add_row("S<id>", "[red] Suprimer définitivement [/red] l'utilisateur <id>")
        tablechoix.add_row("RET", "Retour au menu principal")
        console.print("")
        console.print(tablechoix)
        console.print("")
        valid_choices = ["CR", "RET"]
        console.print("")
        for element in liste_choix:
            valid_choices.append(f"A{element}")
            valid_choices.append(f"M{element}")
            valid_choices.append(f"S{element}")
        
        while True:
            console.print("Votre choix [grey]( CR, A18, D9 ...)[/grey] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")

    def soloUserView(self, user, affiche):
        console = Console()
        console.rule(f"Données de l'utilisateur {affiche.nom} ")
        console.print("")
        tabledonneessolo = Table(box=None)
        tabledonneessolo.add_column("Type", justify="left", style="green", no_wrap=True)
        tabledonneessolo.add_column("Information", justify="left", style="white")
        tabledonneessolo.add_row("", "")
        tabledonneessolo.add_row("Id", f"{affiche.id}")
        tabledonneessolo.add_row("Nom", f"{affiche.nom}")
        tabledonneessolo.add_row("Email", f"{affiche.email}")
        tabledonneessolo.add_row("Service", f"{affiche.role_id}")
        tabledonneessolo.add_row("Date de création", f"{affiche.date_creation}")
        
        console.print(tabledonneessolo)
        
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))
        
        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left", style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        
        tablechoix.add_row("", "")
        tablechoix.add_row("NO <Nouvelle Donnée>", "Modifier le nom de l'utilisateur par <Nouvelle Donnée>")
        tablechoix.add_row("EM <Nouvelle Donnée>", "Modifier l'Email de l'utilisateur par <Nouvelle Donnée>")
        tablechoix.add_row("SE <AD/VE/GE/SU>", "Modifier le Service de l'utilisateur par AD = Admin, VE = Ventes, GE = Gestion et SU = Support")
        tablechoix.add_row("SUPPRIMER", "[red]Supprime définitivement[/red] l'utilisateur de la base de donnée")
        tablechoix.add_row("LIST", "Retour à la liste des utilisateurs")
        tablechoix.add_row("RET", "Retour au menu principal")
        tablechoix.add_row("QUIT", "quitter l'application")
        console.print("")
        console.print(tablechoix)
        console.print("")
        valid_choices = ["CR", "SUPPRIMER", "LIST", "RET", "QUIT", "SE AD", "SE SU", "SE VE", "SE GE"]
        valid_choices_with_id = ["NO", "EM"]
        console.print("")
        while True:
            console.print("Votre choix [grey]( SE AD, NO Eric, EM martin@tot.fr ...)[/grey] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif any(choix.startswith(c) for c in valid_choices_with_id):
                return choix
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")

    def base(self):
        console = Console()
        console.rule("Fin de la page")
        
        
    def createuserview(self):
        console = Console()
        console.rule(f"Création d'un nouvel utilisateur ")
        console.print("")
        console.print("[green] Le nom de l'utilisateur [/green]")
        nom = str(input('==>'))
        console.print("[green] L'Email de l'utilisateur [/green]")
        email = str(input('==>'))
        console.print("[green] Le Mot de passe de l'utilisateur [/green]")
        mot_de_passe = str(input('==>'))
        console.print("[green] Le service de l'utilisateur : 1 (Admin), 2 (Gestion), 3 (Vente), 4 (Support) [/green]")
        role = None
        valid_role = ["1", "2", "3", "4"]
        while True:
            role = input('==>')
            if role in valid_role:
                break
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")
        
        
        console.rule(f"Résumé de votre saisie pour confirmation")
        console.print("")
        tableconfirmation = Table(box=None)
        tableconfirmation.add_column("Type", justify="left", style="green", no_wrap=True)
        tableconfirmation.add_column("Vos saisies", justify="left", style="white")
        tableconfirmation.add_row("", "")
        tableconfirmation.add_row("Nom", f"{nom}")
        tableconfirmation.add_row("Email", f"{email}")
        tableconfirmation.add_row("Mot de passe", f"{mot_de_passe}")
        tableconfirmation.add_row("Service", f"{role}")
        
        console.print(tableconfirmation)
        
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Confirmez vous votre saisie ?", style="bold green")
        console.print(Align.center(centered_text))
        
        console.print("[green] Oui ou Non [/green]")
        valid_role = ["Oui", "Non"]
        while True:
            choix = input('==>')
            if choix == "Oui":
                return nom, email, mot_de_passe, role
            else:
                break